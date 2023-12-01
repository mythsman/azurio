import os
import requests
import json
import gradio as gr
import io
import numpy as np
import random
import time


class GPT:
    def __init__(self, api_key,end_point):
        self.api_key = api_key
        self.end_point=end_point
        self.chatbot = gr.Chatbot(label="GPT-4", height=700)
        self.msg = gr.Textbox(label="ChatBox")

    def load(self, app):
        with gr.Row():
            with gr.Column(scale=1):
                temperature = gr.Slider(
                    label="Temperature", minimum=0, maximum=2, value=0.9
                )
                max_tokens = gr.Slider(
                    label="Max Tokens", minimum=1, maximum=4096, step=1, value=1024
                )
                prompt = gr.TextArea(
                    label="Prompt",
                    value="You are an AI assistant that helps people find information.",
                    lines=5,
                )
                clear = gr.ClearButton([self.msg, self.chatbot], value="Clear History")
            with gr.Column(scale=3):
                self.chatbot.render()
                self.msg.render()

            self.msg.submit(
                self.__submit,
                [self.msg, self.chatbot],
                [self.msg, self.chatbot],
                queue=False,
            ).then(
                self.__respond,
                [self.msg, self.chatbot, temperature, max_tokens, prompt],
                self.chatbot,
            )

    def __submit(self, message, chat_history):
        return "", chat_history + [[message, None]]

    def __respond(self, message, chat_history, temperature, max_tokens, prompt):
        format_messages = []
        format_messages.append({"role": "system", "content": prompt})
        for history in chat_history:
            format_messages.append({"role": "user", "content": history[0]})
            if history[1]:
                format_messages.append({"role": "assistant", "content": history[1]})
        format_messages.append({"role": "user", "content": message})

        # https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?source=recommendations&tabs=command-line
        response = requests.post(
            url=f"https://{self.end_point}/openai/deployments/gpt4/chat/completions?api-version=2023-07-01-preview",
            headers={
                "Content-Type": "application/json",
                "api-key": self.api_key,
            },
            json={
                "messages": format_messages,
                "temperature": temperature,
                "n": 1,
                "max_tokens": max_tokens,
                "stream": True,
            },
            stream=True,
        )

        chat_history[-1][1] = ""

        for data in response.iter_lines():
            data = data.decode("utf-8")
            if data == "data: [DONE]":
                break
            if data:
                resp = json.loads(data.strip("data:"))
                if resp["choices"] and resp["choices"][0]["delta"].get("content"):
                    chat_history[-1][1] += resp["choices"][0]["delta"]["content"]
                    time.sleep(0.05)
                    yield chat_history