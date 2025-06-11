# app/utils/llm.py
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
llm = genai.GenerativeModel("gemini-2.0-flash")

def get_gemini_response(prompt: str) -> str:
    response = llm.generate_content(prompt)
    return response.text