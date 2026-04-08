import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client=genai.configure(api_key=GEMINI_API_KEY)

def language_translator(user_prompt):
    model=genai.GenerativeModel('gemini-2.5-flash')
    response=model.generate_content(user_prompt)
    return response.text

user_question="what is your name transulate in hindi give me a sentance"
output=language_translator(user_question)
print(output)
    
    