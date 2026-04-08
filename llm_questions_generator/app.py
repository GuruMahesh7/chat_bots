import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

personalities = {
    "HR": "give question like hr",
    "MENTOR": "give question like you are my personal mentor"
}

client = genai.Client(api_key=GEMINI_API_KEY)

def question_generator(user_prompt, persona):
    prompt = personalities[persona]
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=prompt,
            )
        )
        return response.text
    except Exception as exc:
        # You can narrow this to google.genai.errors.ClientError if needed
        msg = str(exc)
        if "RESOURCE_EXHAUSTED" in msg or "429" in msg:
            return "⚠️ Quota exhausted. Please wait a moment or upgrade your Gemini plan."
        return f"Error: {msg}"

demo=gr.Interface(
    fn=question_generator,
    inputs=[
        gr.Textbox(lines=4,placeholder="topic",label="topic"),
        gr.Radio(choices=list(personalities.keys()), value="HR", label="Personality")
    ],
   outputs=gr.Textbox(lines=10, label="Response"),
    title="Question Generator",
    description="Ask a question and get an answer from your AI study assistant with a chosen personality."
)

demo.launch(debug=True)