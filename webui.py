import logging
import os

import gradio as gr
import toml

from gpt import GPT
from tts import TTS

logging.basicConfig(level=logging.INFO)


def run():
    if not os.path.exists(".cache/"):
        os.mkdir(".cache/")

    config = toml.load('config.toml')

    proxy = config['global']['proxy_server']
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy
        }
    else:
        proxies = {}

    tabs = []

    if config['gpt']:
        for cfg in config['gpt']:
            gpt = GPT(
                config=cfg,
                proxies=proxies
            )
            tabs.append({
                'name': cfg['name'],
                'tab': gpt
            })

    if config['tts']:
        for cfg in config['tts']:
            tts = TTS(
                config=cfg,
                proxies=proxies
            )
            tabs.append({
                'name': cfg['name'],
                'tab': tts
            })

    with gr.Blocks() as app:
        for tab in tabs:
            with gr.Tab(tab['name']):
                tab['tab'].load(app)

    app.queue()

    server_name = config['global']['server_name']
    server_port = config['global']['server_port']
    auth_list = config['global']['auth_list']

    app.launch(
        server_name=server_name,
        server_port=int(server_port),
        share=False,
        auth=[(item.split(':')[0], item.split(':')[1])
              for item in filter(None, auth_list.split(";"))],
    )


if __name__ == "__main__":
    run()
