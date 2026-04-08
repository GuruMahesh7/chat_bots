from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import gradio as gr

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

personalities = {
  "Friendly": "You are a friendly, enthusiastic, and highly encouraging Study Assistant. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding.",
  "Academic": "You are a strictly academic, highly detailed, and professional university Professor. Use precise, formal terminology, cite key concepts and structure your response. Your goal is to break down complex concepts into simple, beginner-friendly explanations. Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding."
}

client = genai.Client()

def study_assiatent(user_prompt,persona):
    prompt=personalities[persona]
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=prompt,
        )
    )
    return response.text

demo=gr.Interface(
    fn=study_assiatent,
    inputs=[
        gr.Textbox(lines=4,placeholder="ask a quetion", label="Question"),
        gr.Radio(choices=list(personalities.keys()), value="Friendly", label="Personality")
    ],
    outputs=gr.Textbox(lines=10, label="Response"),
    title="Study-Assistent",
    description="Ask a question and get an answer from your AI study assistant with a chosen personality."
)


demo.launch(debug=True)
