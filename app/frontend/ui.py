import gradio as gr
import requests
from app.common.logger import get_logger

logger = get_logger(__name__)

API_URL = "http://127.0.0.1:9999/medicalchat"

def medical_response(message, history):
    try:
        payload={
            "question":message
        }
        response = requests.post(API_URL,json=payload)
        if response.status_code==200:
            model_response = response.json().get("response","")
            return model_response
        else:
            logger.error(f"API returned status code: {response.status_code}")
            return "Sorry, I'm experiencing technical difficulties. Please try again."
    except Exception as e:
            logger.error(f"Error connecting to API: {str(e)}")
            return "Unable to connect to the medical assistant. Please check if the backend is running."

demo = gr.ChatInterface(
    medical_response, 
    type="messages", 
    submit_btn="Send Medical Query",
    theme="soft",
    title="🏥 Medical AI Assistant",
    description="Get instant answers to medical questions",
    examples=["What are symptoms of diabetes?", "How to treat fever?"],
    autofocus=False)
demo.launch()