
import os
import json
from http import HTTPStatus

import bardapi
import requests
from environs import Env

import openai
from dashscope import Generation
from bardapi import Bard
from bardapi.constants import SESSION_HEADERS

env = Env()

class ChatAgent():

    def __init__(self,env, prompt):
        print(f'\n\n======= 调用 Chat Bot =======')
        self.prompt = prompt
        self.env = env

    def chat_gpt_agent(self):
        print(f'\n+++++++++++++++++++++++++++++++')
        print(f'++++++ 调用 OpenAI ChatGPT++++++')
        print(f'++++++++++++++++++++++++++++++++')
        print("提问内容 ："+ self.prompt)
        openai.api_key = os.getenv("OPENAI_API_KEY")

        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                       messages=[{"role": "user", "content": self.prompt}])

        jsonObj = json.loads(chat_completion.__str__())
        chat_gpt_answer = jsonObj['choices'][0]['message']['content']

        print(chat_gpt_answer)
        #print(chat_completion.__str__())

        return chat_gpt_answer

    def bd_wxyy_agent(self):
        print(f'\n+++++++++++++++++++++++++++++')
        print(f'++++++ 调用 百度 文心一言 ++++++')
        print(f'+++++++++++++++++++++++++++++')
        print("提问内容 ：" + self.prompt)

        # url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + os.getenv("BD_ACCESS_TOKEN")

        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + os.getenv("BD_ACCESS_TOKEN")
        #print(url)

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": self.prompt
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.text)

        jsonObj = json.loads(response.text)
        bd_wxyy_answer = jsonObj['result']

        print(bd_wxyy_answer)

        return bd_wxyy_answer


    def ali_tyqw_agent(self):
        print(f'\n+++++++++++++++++++++++++++++')
        print(f'++++++ 调用 阿里 通义千问 ++++++')
        print(f'+++++++++++++++++++++++++++++')
        print("提问内容 ：" + self.prompt)

        messages = [{'role': 'system', 'content': '你是达摩院的知识助手机器人。'},
                    {'role': 'user', 'content': self.prompt}]
        gen = Generation()
        response = gen.call(
            Generation.Models.qwen_v1,
            api_key=os.getenv("ALI_API_KEY"),
            messages=messages,
            result_format='message',  # set the result is message format.
        )
        if response.status_code == HTTPStatus.OK:
            #print(response)
            jsonObj = json.loads(response.__str__())
            ali_tyqw_answer = jsonObj['output']['choices'][0]['message']['content']
            print(ali_tyqw_answer)
            return ali_tyqw_answer
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))


    def google_bard_agent(self):
        print(f'\n+++++++++++++++++++++++++++++')
        print(f'++++++ 调用 Google Bard ++++++')
        print(f'+++++++++++++++++++++++++++++')
        print("提问内容 ：" + self.prompt)

        bard_token =os.getenv("1PSID")
        #print(bard_token)

        session = requests.Session()
        session.headers = SESSION_HEADERS
        session.cookies.set("__Secure-1PSID", os.getenv("1PSID"))
        session.cookies.set("__Secure-1PSIDTS", os.getenv("1PSIDTS"))
        session.cookies.set("__Secure-1PSIDCC", os.getenv("1PSIDCC"))

        bard = Bard(token=bard_token, session=session)
        response = bard.get_answer(self.prompt).__str__().replace('\'',"\"")
        print(response)
        return response
