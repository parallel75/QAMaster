from environs import Env
import requests
import json

env = Env()
class Search(object):

    def __init__(self,env, content):
        print(f'======= 调用 google 搜索 =======')
        self.content = content
        self.env = env


    # 请求 google API 获取搜索结果
    def doSearch(self):
        #GOOGLE_URL = https: // google.serper.dev / search
        url = env.str('GOOGLE_URL')
        # print(url)
        print("搜索内容： " + self.content)

        payload = json.dumps({"q": self.content, "gl": "cn", "hl": "zh-cn"})

        #Serper的 API Key 包含在 headers 中
        response = requests.request("POST", url, headers=env.dict('SERPER_HEADERS'), data=payload)
        # print(response.text)

        allAnswsers = self.getResult(response.text)

        return  allAnswsers

    # 获取搜索结果
    def getResult(self,result):
        jsonObj = json.loads(result)
        jsonData = jsonObj['organic']
        #(jsonData)

        # 获取前 5 个搜索结果
        allAnswsers = ""
        for i in range(5):
            answser = jsonData[i]['snippet'] + " --- "+ jsonData[i]['link']
            print("搜索结果：" + answser)
            allAnswsers+=answser+"\n\n"

        return allAnswsers
