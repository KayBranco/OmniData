from google import genai
print('genai.models.Models attrs:', [a for a in dir(genai.models.Models) if not a.startswith('_')])
