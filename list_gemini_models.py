"""List available Gemini models"""
import google.generativeai as genai
from config import settings

genai.configure(api_key=settings.google_api_key)

print("Available Gemini models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")
        print(f"    Display name: {model.display_name}")
        print(f"    Description: {model.description[:100]}...")
        print()
