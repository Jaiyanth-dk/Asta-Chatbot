import requests
import gradio as gr

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "asta"

def chat(message, history):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": message,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]

demo = gr.ChatInterface(
    fn=chat,
    title="Asta AI",
    description="Local Ollama-powered AI Assistant"
)

demo.launch()