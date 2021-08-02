"""
작성자: 이수진
작성일: 2021.07.28
수정일: 2021.07.29
"""

import os                              # ngrok용 port 설정
from configparser import ConfigParser  # bot token
from slack_bolt import App             # event handling
from core.prefer import preferMenu     # 추천 알고리즘
from utils.data_manager import updateMenu, getMenuCategory, getMemberList # 오늘의 메뉴 업데이트

config = ConfigParser()
config.read('config.ini')

TOKEN = config['SLACKBOT']['TOKEN']
SIGNING_SECRET = config['SLACKBOT']['SECRET_SIGNING']

# Initializes the app
app = App(
    token=TOKEN,
    signing_secret = SIGNING_SECRET
)

# 메뉴 종류 & 멤버 정보
menuCategory = getMenuCategory()
members = getMemberList()

def printMenuCategory():
    print(menuCategory)

# event handling
@app.message("hello")
def say_hello(message, say, payload):
    say("hi")
    print(payload['text'])

@app.message("봇정보")
def say_hello(message, say, payload):
    messageForm = "*점심 메뉴 추천을 위해 만들어진 봇입니다!*\n>"\
                  " :page_facing_up: 사용 가능한 명령어\n>"\
                  "- 점심추천 [밖/안] [멤버 이름1] [멤버 이름2] [멤버 이름2] : 점심 메뉴 추천\n>"\
                  "- 오늘 메뉴 [메뉴 이름] : 오늘 먹은 음식 기록 저장\n>"

    say(messageForm)

@app.message("점심추천")
def lunch(say, payload):
    print(payload)

    try:
        commands = payload['text'].split()
        if len(commands) < 2: raise
        if commands[1] != '안' and commands[1] != '밖':  say("밖/안 구분을 넣어주세요!"); raise
        delivery = (commands[1] == '안')

        memberList = [x for x in commands[2:]]
        for mem in memberList:
            if mem not in members: say("멤버 이름 확인해주세요!"); raise

        print((delivery == True))
        print(memberList)

        menuList = preferMenu(memberList, delivery)

        say(menuList)

    except:
        say(
            "*점심추천 명령어의 사용법을 다시 확인해주세요!\n>" \
            "> 점심추천 [밖/안] [멤버 이름들]"
        )

@app.message("오늘메뉴")
def lunch(say, payload):

    try:
        commands = payload['text'].split()
        if len(commands) < 2: raise
        if commands[1] != '안' and commands[1] != '밖':  say("밖/안 구분을 넣어주세요!"); raise
        delivery = (commands[1] == '안')

        menu = commands[2]
        if menu not in menuCategory: say("메뉴 카테고리를 다시 확인해주세요!"); printMenuCategory(); raise

        memberList = [x for x in commands[3:]]
        for mem in memberList:
            if mem not in members: say("멤버 이름 확인해주세요!"); raise

        updateMenu(menuName=menu, memberList=memberList, delivery=delivery)

        say(f"오늘의 메뉴 {menu} 저장되었어요!")
    except:
        say(
            "*오늘메뉴 명령어의 사용법을 다시 확인해주세요!\n>"\
            "> 오늘메뉴 [밖/안] [메뉴명] [멤버이름들]"
        )


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))