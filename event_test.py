from configparser import ConfigParser
import os
from slack_bolt import App
from datetime import datetime, date, timedelta
import pandas as pd

config = ConfigParser()
config.read('config.ini')

TOKEN = config['SLACKBOT']['TOKEN']
SIGNING_SECRET = config['SLACKBOT']['SECRET_SIGNING']

# Initializes the app
app = App(
    token=TOKEN,
    signing_secret = SIGNING_SECRET
)

# 메뉴추천
def preferMenu(members, delivery=True):
    # members: 점심을 먹을 멤버들이 포함된 튜플 또는 리스트 (예: (member1, member3))
    # delivery(default: True): 배달 여부 (True: 배달음식, False: 외부음식)
    path = './data/'  # .csv 파일들이 저장된 경로 입력

    memberLen = len(members)
    menu = pd.read_csv(path + 'menu.csv', engine='python', encoding='CP949')
    menu.index = menu['menu'].values  # 메뉴의 행 이름을 메뉴명으로 변경하기 위한 코드
    menu.drop(['menu'], axis=1, inplace=True)  # 메뉴의 행 이름을 메뉴명으로 변경하기 위한 코드

    if delivery == False:  # delivery 인자가 False(즉, 외식)이면 외식용 메뉴 리스트로 변환. 즉, True(배달용)에 해당하는 메뉴를 모두 버림
        menu = menu.loc[menu['delivery'] == False]
    menuScore = menu.loc[:, members].prod(axis=1)  # menuScore를 반환, menuScore = members의 메뉴 선호도를 모두 곱한 값을 반환

    menulog = pd.read_csv(path + 'menulog.csv', engine='python', encoding='CP949')

    yeday = (date.today() - timedelta(1)).isoformat()  # 어제
    yeyeday = (date.today() - timedelta(2)).isoformat()  # 그제
    yeyeyeday = (date.today() - timedelta(3)).isoformat()  # 그끄제

    for day in ((yeday, 0), (yeyeday, 0.2), (yeyeyeday, 0.6)):  # 어제의 메뉴는 가중치 0, 그제 메뉴는 가중치 0.2, 그끄제 메뉴는 가중치 0.6
        if (menulog['date'] == day[0]).any():  # 어제날짜(또는 그제,그끄제)가 menulog에 있으면 menulog에서 뽑아낸 어제의 메뉴
            daymanu = menulog[menulog['date'] == day[0]]['menu'].reset_index()['menu'][0]
            if (menuScore.index == daymanu).any():  # 어제의 메뉴가 menuScore에 있으면 score에 가중치 곱산
                menuScore.loc[daymanu] = day[1] * menuScore.loc[daymanu]

    preferSorted = menuScore.sort_values(ascending=False).head(3)  # menuScore를 내림차순으로 3개 반환하여 preferSorted에 저장하는 코드

    # 아래는 printMent를 구성
    printMent0 = "*오늘 점심 메뉴 추천은 다음과 같아요!*"
    printMent1 = "> :first_place_medal: " + preferSorted.index[0] + "    (점수: " + str(
        round(preferSorted[0] * 100 / (5 ** memberLen), 1)) + " )"
    printMent2 = "> :second_place_medal: " + preferSorted.index[1] + "    (점수: " + str(
        round(preferSorted[1] * 100 / (5 ** memberLen), 1)) + " )"
    printMent3 = "> :third_place_medal: " + preferSorted.index[2] + "    (점수: " + str(
        round(preferSorted[2] * 100 / (5 ** memberLen), 1)) + " )"
    return printMent0 + '\n' + printMent1 + '\n' + printMent2 + '\n' + printMent3



# Respond to hello
@app.message("hello")
def say_hello(message, say, payload):
    say("hi")
    print(payload['text'])

@app.message("넌뭐야")
def say_hello(message, say, payload):
    # 설명 추가
    say("hi")
    print(payload['text'])

@app.message("점심추천")
def lunch(say, payload):
    """
    :param say:
    :param payload: message 내용
    :return:

    명령어 형식(모두 띄어쓰기 해야함) = [점심추천] [밖/안] [멤버1] [멤버2] [멤버3] [멤버4] ~~
    """
    commands = payload['text'].split()
    inside = (commands[1] == '안')
    memberList = [x for x in commands[2:]]

    print((inside == True))
    print(memberList)

    # menuList = ["한식", "중식", "양식"]
    menuList = preferMenu(memberList, inside)

    # message_format = f"---------------------\n>" \
    #                  f"{datetime.now().strftime('%Y-%m-%d')} \n>\n>" \
    #                  f"오늘의 추천 메뉴\n>" \
    #                  f"1순위. {menuList[0]}\n>" \
    #                  f"2순위. {menuList[1]}\n>" \
    #                  f"3순위. {menuList[2]}\n>" \
    #                  f"---------------------\n>"
    # say(message_format)

    say(menuList)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))