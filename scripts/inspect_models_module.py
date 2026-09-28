from google import genai
print('genai.models attrs:', [a for a in dir(genai.models) if not a.startswith('_')])
print('genai.models.list exists?', hasattr(genai.models, 'list'))
print('genai.Client().models has attrs:', [a for a in dir(genai.Client().models) if not a.startswith('_')])
