

import requests
import json
from bs4 import BeautifulSoup
from environs import Env
from pyairtable import Api
from bardapi import Bard
from dashscope import Generation

from zh_util import *
from search import *
from chat_agent import *

env = Env()

# Step1: 获取知乎的问题数据 或者 自定义问题

# Step2.1: 调用 google 给出答案

# Step2.2: 调用 openAI 直接给出回答

# Step2.3: 调用 百度 文心一言 直接给出回答

# Step2.5  调用 阿里 通义千问 直接给出回答

# Step2.6: 调用 google bard 直接给出回答

# Step3: 数据格式化后写入 airtable

# Step4: 调用插件总结(未完成)



# 获取元数据
def get_question(request_url):
    HEADERS = env.dict('HEADERS')
    # print(type(HEADERS), HEADERS)

    response = requests.get(url=request_url, headers=HEADERS)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.get_text())

    return soup.get_text()

#获取知乎 邀请回答页 数据
def add_inivited_to_airtable(result, table):
    jsonObj = json.loads(result)
    jsonData = jsonObj['data']
    # print(jsonData)

    for i in range(20):
        # print()
        jsonQuestion = jsonData[i]['target_source']
        print(str(i+1)+" : "+jsonQuestion['text']+" --- "+jsonQuestion['sub_text'])

        # print(jsonQuestion['sub_text'])
        visitCount = ZHUtil.getVisitCount(str(jsonQuestion['sub_text']))

        #s = Search(env,jsonQuestion['text'])
        #google_result = s.doSearch()
        # print("所有的搜索结果 ："+google_result)

        #agent = ChatAgent(env, jsonQuestion['text'])

        # 调用 openai
        #openai_result = agent.chat_gpt_agent()
        # print("\n\nOpenAI ChatGPT：\n"+openai_result)

        # 调用 百度 文心一言
        #bd_wxyy_result = agent.bd_wxyy_agent()
        # print("\n\n百度 文心一言 ：\n"+bd_wxyy_result)

        # 调用 阿里 通义千问
        #ali_tyqw_result = agent.ali_tyqw_agent()
        # print("\n\n 阿里 通义千问 ：\n"+ali_tyqw_result)

        # 调用 google bard
        #bard_result = agent.google_bard_agent()
        # print("\n\n Google Bard ：\n"+bard_result)

        record = table.create({"content": jsonQuestion['text'], "visit": visitCount}, False,True)
        print(record)

        # Step2: 数据格式化后写入 airtable
        # record = table.create({"content": jsonQuestion['text'], "visit": visitCount,
        #                        "google_response": google_result,
        #                        "openai_response": openai_result,
        #                        "wxyy_response": bd_wxyy_result,
        #                        "tyqw_response": ali_tyqw_result}, False, True)
        #
        # print("\n\n==============================================")
        # print("")
        # print("写入 AirTable: " + record.__str__())
        # print("")
        # print("==============================================")

#获取知乎 为你推荐页 数据
def add_recommend_to_airtable(result,table):
    jsonObj = json.loads(result)
    jsonData = jsonObj['data']
    print(jsonData)

    for i in range(20):
        print()
        jsonQuestion = jsonData[i]['question']
        # print(str(i+1)+" : "+jsonQuestion['title']+" --- "+ str(jsonQuestion['visit_count']))

        # Step2: 数据格式化后写入 airtable
        record = table.create({"content": jsonQuestion['title'], "visit": str(jsonQuestion['visit_count'])}, False, True)
        print(record)


#自定义数据  收集数据
def answer_custom_question(question,table):

    #调用  google 搜索  提取前五个答案
    s = Search(env, question)
    google_result = s.doSearch()
    #print("\n\n所有的搜索结果 ：\n"+google_result)


    agent = ChatAgent(env, question)
    #调用 openai
    openai_result = agent.chat_gpt_agent()
    # print("\n\nOpenAI ChatGPT：\n"+openai_result)

    #调用 百度 文心一言
    bd_wxyy_result = agent.bd_wxyy_agent()
    # print("\n\n百度 文心一言 ：\n"+bd_wxyy_result)

    #调用 阿里 通义千问
    ali_tyqw_result = agent.ali_tyqw_agent()
    # print("\n\n 阿里 通义千问 ：\n"+ali_tyqw_result)

    #调用 google bard
    #bard_result = agent.google_bard_agent()
    # print("\n\n Google Bard ：\n"+bard_result)

    #写入 AirTable
    record = table.create({"content": question, "visit": "100",
                           "google_response": google_result,
                            "openai_response": openai_result,
                            "wxyy_response":bd_wxyy_result,
                            "tyqw_response":ali_tyqw_result}, False, True)


    print("\n\n==============================================")
    print("")
    print("写入 AirTable: " + record.__str__())
    print("")
    print("==============================================")



def controller():
    #获取系统参数
    env.read_env()

    #conenect airtable 获取存储数据的 table
    airtable_api = Api(env('AIRTABLE_TOKEN'))
    table = airtable_api.table(env.str('AIRTABLE_DB_ID'), env.str('AIRTABLE_TABLE_ID'))

    #问题实例
    #question = "韩国为什么被称为世界经济金丝雀"
    #question = "为什么回不到计划经济了？"
    question="描写晚霞的唐诗"

    #有些知乎 问题 在 各个LLM 都找不到答案  请优先使用自定义问题进行测试
    # Step1: 获取知乎的问题数据
    #invitedResult = get_question(env('URL_INVITED'))
    #print("元数据： "+invitedResult)

    # Step2: 数据格式化后写入 airtable
    #add_inivited_to_airtable(invitedResult,table)

    # Step1: 获取知乎的问题数据
    #recommendResult = get_question(env('URL_RECOMMEND'))
    #print(recommendResult)

    # Step2: 数据格式化后写入 airtable
    #add_recommend_to_airtable(recommendResult,table)



    #自定义问题 先后调用 LLM 和 Google search
    #测试请优先使用这个
    answer_custom_question(question,table)



def print_message(message):
    print(f'***********************************************************')
    print(f'======= {message} =======')
    print(f'***********************************************************')
    print(f'')

if __name__ == '__main__':
    print_message('调用 Google search & LLM  实现 AI 数据收集 Demo')
    controller()



