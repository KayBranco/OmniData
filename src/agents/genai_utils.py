import time
import random
import logging
from typing import List, Any

logger = logging.getLogger("omnidata.genai")
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def generate_with_retry(
    client,
    model_names: List[str],
    contents: List[Any],
    max_attempts: int = 4,
    base_delay: float = 1.0,
):
    """Try generating content using a list of models with exponential backoff and jitter.

    Args:
        client: genai.Client instance
        model_names: ordered list of model ids to try
        contents: contents arg to pass to client.models.generate_content
        max_attempts: number of attempts per model
        base_delay: base delay in seconds for backoff

    Returns:
        The successful response object from client.models.generate_content

    Raises:
        Exception from last failed attempt if all attempts and fallbacks fail.
    """
    # Normalize contents to a list of strings accepted by the SDK.
    # SDK expects contents as list[str] or Content objects; older code sometimes passed
    # dicts like {"type":"text","text":...}. Coerce those to strings here.
    if contents is None:
        normalized = []
    elif isinstance(contents, (str, bytes)):
        normalized = [str(contents)]
    else:
        normalized = []
        for c in contents:
            if isinstance(c, str):
                normalized.append(c)
            elif isinstance(c, dict):
                # common dict shape: {"type":"text", "text":"..."}
                if "text" in c:
                    normalized.append(str(c["text"]))
                elif "content" in c and isinstance(c["content"], str):
                    normalized.append(c["content"])
                else:
                    # fallback to string repr
                    normalized.append(str(c))
            else:
                # object with .text attribute
                txt = getattr(c, "text", None)
                if txt is not None:
                    normalized.append(str(txt))
                else:
                    normalized.append(str(c))

    last_exc = None
    for model in model_names:
        # Normalize model id: genai expects ids like "models/<name>" in many places
        model_id = model if str(model).startswith("models/") else f"models/{model}"
        logger.info("Trying model %s", model_id)
        attempt = 0
        while attempt < max_attempts:
            try:
                resp = client.models.generate_content(model=model_id, contents=normalized)
                logger.info("Success with model %s on attempt %d", model_id, attempt + 1)
                return resp
            except Exception as e:
                last_exc = e
                msg = str(e).lower()
                # consider retryable cases
                if "503" in msg or "unavailable" in msg or "high demand" in msg:
                    attempt += 1
                    delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.5)
                    logger.warning(
                        "Model %s unavailable (attempt %d/%d). Retrying in %.2fs: %s",
                        model,
                        attempt,
                        max_attempts,
                        delay,
                        e,
                    )
                    time.sleep(delay)
                    continue
                # non-retryable: break out and try next model
                logger.error("Non-retryable error for model %s: %s", model, e)
                break
        logger.info("Falling back from model %s to next model", model)
    # all models exhausted
    logger.error("All models/exhausted retries failed. Last error: %s", last_exc)
    raise last_exc
