from google import genai
print('Client attrs:', [a for a in dir(genai.Client) if not a.startswith('_')])
print('genai module attrs:', [a for a in dir(genai) if not a.startswith('_')])
print('Has models attr on genai.Client?', hasattr(genai.Client, 'models'))
