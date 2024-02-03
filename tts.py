import os
import requests
import json
import gradio as gr
import io
import numpy as np
from scipy.io.wavfile import write, read


class TTS:
    def __init__(self, config, proxies):
        self.speech_key = config['key']
        self.end_point = config['endpoint']
        self.proxies = proxies

        speech_list = self.__get_speech_list()

        # gender , locale , local_name -> short_name
        self.data_map = {}

        # short_name -> styles
        self.style_map = {}

        for item in speech_list:
            gender = item["Gender"]
            locale = item["Locale"]
            local_name = item["LocalName"]
            short_name = item["ShortName"]
            style_list = item.get("StyleList")

            if gender not in self.data_map:
                self.data_map[gender] = {}
            if locale not in self.data_map[gender]:
                self.data_map[gender][locale] = {}
            if local_name not in self.data_map[gender][locale]:
                self.data_map[gender][locale][local_name] = short_name

            if style_list:
                self.style_map[short_name] = style_list
            else:
                self.style_map[short_name] = []

    def load(self, app):
        with gr.Row():
            with gr.Column(scale=1):
                gender = gr.Radio(
                    choices=["Male", "Female"],
                    value="Male",
                    label="Gender",
                    interactive=True,
                )
                locale = gr.Dropdown(
                    choices=[],
                    label="Locale",
                    interactive=True
                )
                name = gr.Dropdown(
                    choices=[],
                    label="Name",
                    interactive=True
                )
                style = gr.Dropdown(
                    choices=[],
                    label="Style",
                    interactive=True
                )

            with gr.Column(scale=3):
                text = gr.TextArea(label="Input Text", lines=4)
                btn = gr.Button("Generate")
                output = gr.Audio(label="Output")

        gender.change(self.__gender_change, gender, locale).then(
            self.__locale_change, [gender, locale], name
        )

        locale.change(self.__locale_change, [gender, locale], name).then(
            self.__name_change, [gender, locale, name], style
        )

        name.change(self.__name_change, [gender, locale, name], style)

        btn.click(self.__do_tts, [gender, locale, name, style, text], output)

        app.load(self.__gender_change, gender, locale)

    def __get_speech_list(self):
        cache_file = ".cache/tts_speech_list.json"

        if not os.path.exists(cache_file):
            response = requests.get(
                url=f"{self.end_point}/voices/list",
                headers={"Ocp-Apim-Subscription-Key": self.speech_key},
                proxies=self.proxies,
            )
            with open(cache_file, "w") as writer:
                json_data = response.json()
                writer.write(json.dumps(
                    json_data, indent=2, ensure_ascii=False))
        with open(cache_file, "r") as reader:
            return json.loads(reader.read())

    def __get_tts(self, gender, locale, name, style, text):
        # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup
        if style:
            style_text = f"<mstts:express-as style='{style}' styledegree='2'>{text}</mstts:express-as>"
        else:
            style_text = text

        data = f"<speak version='1.0' xml:lang='{locale}'  xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts'><voice xml:lang='{locale}' xml:gender='{gender}' name='{name}'>{style_text}</voice></speak>"
        response = requests.post(
            url=f"{self.end_point}/v1",
            headers={
                "Ocp-Apim-Subscription-Key": self.speech_key,
                "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
                "Content-Type": "application/ssml+xml",
            },
            data=data.encode("utf-8"),
            proxies=self.proxies,
        )
        return response.content

    def __do_tts(self, gender, locale, name, style, text):
        short_name = self.data_map[gender][locale][name]

        data = self.__get_tts(gender, locale, short_name, style, text)
        return read(io.BytesIO(data))

    def __gender_change(self, gender):
        choices = list(self.data_map[gender].keys())
        return gr.Dropdown(choices=choices, value="zh-CN", interactive=True)

    def __locale_change(self, gender, locale):
        choices = list(self.data_map[gender][locale].keys())
        return gr.Dropdown(choices=choices, value=choices[0], interactive=True)

    def __name_change(self, gender, locale, name):
        short_name = self.data_map[gender][locale][name]
        style_list = self.style_map[short_name]

        if len(style_list) == 0:
            return gr.Dropdown(choices=[], value=None, interactive=True)
        else:
            return gr.Dropdown(
                choices=style_list, value=style_list[0], interactive=True
            )
