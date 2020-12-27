from datetime import datetime

from transitions.extensions import GraphMachine

from helper import LineAPI

from bs4 import BeautifulSoup
import requests



class TocMachine(GraphMachine):
    def __init__(self):
        self.page = 1
        self.category=0
        self.machine = GraphMachine(
            model=self,
            **{
                "states" : [
                    'init',
                    'functionList',
                    'anime',
                    'animeRank',
                    'graph',
                    'kind',
                    'Rank'
                ],
                "transitions" : [
                    {
                        'trigger': 'start',
                        'source': 'init',
                        'dest': 'functionList',
                    },
                    {
                        'trigger': 'Function1',
                        'source': 'functionList',
                        'dest': 'anime',
                    },
                    {
                        'trigger': 'Function2',
                        'source': 'functionList',
                        'dest': 'animeRank',
                    },
                    {
                        'trigger': 'Function3',
                        'source': 'functionList',
                        'dest': 'graph',
                    },
                    {
                        'trigger': 'search',
                        'source': 'anime',
                        'dest': 'kind',
                    },
                    {
                        'trigger': 'loop',
                        'source': 'kind',
                        'dest': 'kind',
                    },
                    {
                        'trigger': 'restart',
                        'source': 'kind',
                        'dest': 'functionList',
                    },
                    {
                        'trigger': 'goback',
                        'source': 'kind',
                        'dest': 'anime',
                    },
                    {
                        'trigger': 'searchRank',
                        'source': 'animeRank',
                        'dest': 'Rank',
                    },
                    {
                        'trigger': 'goback_r',
                        'source': 'Rank',
                        'dest': 'animeRank',
                    },
                    {
                        'trigger': 'restart_r',
                        'source': 'Rank',
                        'dest': 'functionList',
                    },
                ],
                "initial" : 'init',
                "auto_transitions" : False,
            }
        )

    def is_going_to_Error(self, reply_token, text):
        options_str = (
            "輸入非法字元，請重新輸入"
        )
        LineAPI.send_reply_message(reply_token, options_str)
    
    
        
    # states
    def on_enter_functionList(self, reply_token, text):
        
        options_str = (
            "這個聊天室提供3個功能\n\n"
            "1.動漫資訊蒐集\n" 
            "2.查詢本月熱門排行\n" 
            "3.印出聊天室fsm圖\n\n"
            "請輸入數字來決定你的功能"
        )
        LineAPI.send_reply_message(reply_token, options_str)

    def on_enter_anime(self, reply_token, text):
        self.page = 1
        self.category=0
        options_str = (
            "請輸入動漫類別\n\n"
            "戀愛\n溫馨\n奇幻冒險\n科幻未來\n幽默搞笑\n靈異鬼怪\n推理懸疑\n料理美食\n社會寫實\n運動競技\n歷史傳記\n"
            "青春校園\n其他\n電影版\nOVA"
        )
        LineAPI.send_reply_message(reply_token, options_str)
    
    def on_enter_animeRank(self, reply_token, text):
        options_str = (
            "請輸入動漫類別\n\n"
            "所有動畫\n戀愛\n溫馨\n奇幻冒險\n科幻未來\n幽默搞笑\n靈異鬼怪\n推理懸疑\n料理美食\n社會寫實\n運動競技\n歷史傳記\n"
            "青春校園\n其他\n電影版\nOVA"
        )
        LineAPI.send_reply_message(reply_token, options_str)
    
    def on_enter_graph(self, reply_token, text):
        TocMachine().get_graph().draw('fsm.png', prog='dot', format='png')
        
        
    
    def on_enter_kind(self, reply_token, text):

        baseAddr="https://ani.gamer.com.tw/"
        advancedAddr=""

        if text=="下一頁" :
            if self.page <= 0 : 
                self.page+=2
            else:
                self.page=self.page+1
        if text=="上一頁" :
            if self.page == 1:
                self.page=self.page-2
            elif self.page > 1:
                self.page=self.page-1
        pageStr="page="+str(self.page)+"&"
        
        if text=="戀愛" or self.category== 1 :
            advancedAddr="animeList.php?"+pageStr+"c=1&sort=1"
            self.category=1
        if text=="溫馨" or self.category== 2:
            advancedAddr="animeList.php?"+pageStr+"c=2&sort=1"
            self.category=2
        if text=="奇幻冒險" or self.category== 3:
            advancedAddr="animeList.php?"+pageStr+"c=3&sort=1"
            self.category=3
        if text=="科幻未來" or self.category== 4 :
            advancedAddr="animeList.php?"+pageStr+"c=4&sort=1"
            self.category=4
        if text=="幽默搞笑" or self.category== 5:
            advancedAddr="animeList.php?"+pageStr+"c=5&sort=1"
            self.category=5
        if text=="靈異鬼怪" or self.category== 6:
            advancedAddr="animeList.php?"+pageStr+"c=6&sort=1"
            self.category=6
        if text=="推理懸疑" or self.category== 7:
            advancedAddr="animeList.php?"+pageStr+"c=7&sort=1"
            self.category=7
        if text=="料理美食" or self.category== 8:
            advancedAddr="animeList.php?"+pageStr+"c=8&sort=1"
            self.category=8
        if text=="社會寫實" or self.category== 9:
            advancedAddr="animeList.php?"+pageStr+"c=9&sort=1"
            self.category=9
        if text=="運動競技" or self.category== 10:
            advancedAddr="animeList.php?"+pageStr+"c=10&sort=1"
            self.category=10
        if text=="歷史傳記" or self.category== 11:
            advancedAddr="animeList.php?"+pageStr+"c=11&sort=1"
            self.category=11
        if text=="其他" or self.category== 12:
            advancedAddr="animeList.php?"+pageStr+"c=12&sort=1"
            self.category=12
        if text=="青春校園" or self.category== 13:
            advancedAddr="animeList.php?"+pageStr+"c=13&sort=1"
            self.category=13
        if text=="電影版" or self.category== 14:
            advancedAddr="animeList.php?"+pageStr+"c=movie&sort=1"
            self.category=14
        if text=="OVA" or self.category== 15:
            advancedAddr="animeList.php?"+pageStr+"c=ova&sort=1"
            self.category=15

        response = requests.get(baseAddr+advancedAddr)
        soup = BeautifulSoup(response.content, "html.parser")
        
        count=0
        nameList = []
        linklist = []
        output_str=""

        datas = soup.find('div', {'class': 'theme-list-block'}).find_all('a')
        for data in datas:
            linklist.append(baseAddr+ data['href'])

            response2=requests.get(baseAddr+ data['href'])
            soup2 = BeautifulSoup(response2.content, "html.parser")
            name = soup2.find('div', {'class': 'anime_name'}).find('h1').getText()
            nameList.append(name)
            count+=1
        if count == 0:
            if self.page >= 1:
                output_str += "已到清單最末頁"
                self.page =self.page-1
            else:
                output_str += "已到清單最前頁"
        else:
            for i in range(len(nameList)):
                output_str += nameList[i]
                output_str += "\n"
                output_str += linklist[i]
                output_str += "\n\n"

        output_str +="\n\n輸入:0 , 回到程式最開始 \n"
        output_str +="輸入:1 , 回到上一個功能 \n"
        output_str +="輸入:上一頁\n"
        output_str +="輸入:下一頁"

        LineAPI.send_reply_message(reply_token, output_str)

    def on_enter_Rank(self, reply_token, text):

        baseAddr="https://ani.gamer.com.tw/"
        advancedAddr=""
        if text =="所有動畫":
            advancedAddr="animeList.php?"+"c=0&sort=2"
        if text=="戀愛"  :
            advancedAddr="animeList.php?"+"c=1&sort=2"
        if text=="溫馨" :
            advancedAddr="animeList.php?"+"c=2&sort=2"
        if text=="奇幻冒險":
            advancedAddr="animeList.php?"+"c=3&sort=2"
        if text=="科幻未來" :
            advancedAddr="animeList.php?"+"c=4&sort=2"
        if text=="幽默搞笑" :
            advancedAddr="animeList.php?"+"c=5&sort=2"
        if text=="靈異鬼怪" :
            advancedAddr="animeList.php?"+"c=6&sort=2"
        if text=="推理懸疑" :
            advancedAddr="animeList.php?"+"c=7&sort=2"
        if text=="料理美食" :
            advancedAddr="animeList.php?"+"c=8&sort=2"
        if text=="社會寫實" :
            advancedAddr="animeList.php?"+"c=9&sort=2"
        if text=="運動競技" :
            advancedAddr="animeList.php?"+"c=10&sort=2"
        if text=="歷史傳記" :
            advancedAddr="animeList.php?""c=11&sort=2"
        if text=="其他" :
            advancedAddr="animeList.php?""c=12&sort=2"
        if text=="青春校園" :
            advancedAddr="animeList.php?"+"c=13&sort=2"
        if text=="電影版" :
            advancedAddr="animeList.php?"+"c=movie&sort=2"
        if text=="OVA" :
            advancedAddr="animeList.php?"+"c=ova&sort=2"

        response = requests.get(baseAddr+advancedAddr)
        soup = BeautifulSoup(response.content, "html.parser")

        count=0
        nameList = []
        linklist = []
        output_str=""

        datas = soup.find('div', {'class': 'theme-list-block'}).find_all('a')

        for data in datas:
            linklist.append(baseAddr+ data['href'])
            response2=requests.get(baseAddr+ data['href'])
            soup2 = BeautifulSoup(response2.content, "html.parser")
            name = soup2.find('div', {'class': 'anime_name'}).find('h1').getText()
            nameList.append(name)
            count+=1
            if count >= 5 :
                break

            

        for i in range(len(nameList)):
            output_str += ("第"+str(i+1)+"名\n")
            output_str += nameList[i]
            output_str += "\n"
            output_str += linklist[i]
            output_str += "\n\n"

        output_str +="\n\n輸入:0 , 回到程式最開始 \n"
        output_str +="輸入:1 , 回到上一個功能 \n"
        output_str +="輸入:上一頁\n"
        output_str +="輸入:下一頁"

        LineAPI.send_reply_message(reply_token, output_str)

        
        
        

    
