from flask import Flask
from openai import OpenAI
import google.generativeai as genai
import os

openai_client = None
gemini_model = None

def init_extensions(app: Flask) -> None:
    global openai_client, gemini_model
    model_name = app.config.get("MODEL_NAME", os.environ.get("MODEL_NAME", "openai")).lower()
    gemini_api_key = app.config.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    open_api_key = app.config.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY"))

    if model_name == "gemini":
        genai.configure(api_key=gemini_api_key)
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    if model_name == "opnai":
        openai_client = OpenAI(api_key=open_api_key)

    if openai_client == None and gemini_model is None:
        openai_client = OpenAI(api_key=open_api_key)