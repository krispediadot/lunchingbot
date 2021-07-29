"""
작성자: 김근우
"""

import pandas as pd
from datetime import datetime, date, timedelta

def preferMenu(members, delivery=True):
    # members: 점심을 먹을 멤버들이 포함된 튜플 또는 리스트 (예: (member1, member3))
    # delivery(default: True): 배달 여부 (True: 배달음식, False: 외부음식)
    path = 'core/data/'  # .csv 파일들이 저장된 경로 입력

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
