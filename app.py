import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("api key not found")
else:
    print("api key found")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    try:
        response = model.generate_content("How are you?")
        print(response.text)
    except Exception as e:
        print(e)