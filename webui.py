import io
import os

import gradio as gr
import numpy as np
import requests

from gpt import GPT
from tts import TTS
from dotenv import load_dotenv


def run():
    if not os.path.exists(".cache/"):
        os.mkdir(".cache/")
        
    tts_tab = TTS(
        speech_key=os.environ.get('AZURE_SPEECH_KEY', ""), 
        end_point=os.environ.get('AZURE_SPEECH_ENDPOINT', "")
    )
    gpt_tab = GPT(
        api_key=os.environ.get('AZURE_GPT_KEY', ""),
        end_point=os.environ.get('AZURE_GPT_ENDPOINT', "")
    )

    with gr.Blocks() as app:
        with gr.Tab("Azure GPT-4"):
            gpt_tab.load(app)
        with gr.Tab("Azure TTS"):
            tts_tab.load(app)

    app.queue()

    auth_list = os.environ.get('GRADIO_AUTH_LIST', "")
    
    app.launch(
        server_name=os.environ.get('GRADIO_SERVER_NAME', "172.17.0.1"),
        server_port=int(os.environ.get('GRADIO_SERVER_PORT', '8888')),
        share=False,
        auth=[(item.split(':')[0],item.split(':')[1]) for item in filter(None,auth_list.split(";"))],
    )


if __name__ == "__main__":
    load_dotenv()
    run()
