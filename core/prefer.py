"""
작성자: 김근우
작성일:
수정일: 2021.08.09
"""

import pandas as pd
from datetime import datetime, date, timedelta

path = 'core/data/'  # .csv 파일들이 저장된 경로 입력

def preferMenu(members, delivery=True):
    # members: 점심을 먹을 멤버들이 포함된 튜플 또는 리스트 (예: (member1, member3))
    # delivery(default: True): 배달 여부 (True: 배달음식, False: 외부음식)

    memberLen = len(members)
    menu = pd.read_csv(path + 'menu.csv', engine='python', encoding='CP949')
    menu.index = menu['menu'].values  # 메뉴의 행 이름을 메뉴명으로 변경하기 위한 코드
    menu.drop(['menu'], axis=1, inplace=True)  # 메뉴의 행 이름을 메뉴명으로 변경하기 위한 코드
"ㅈㅂ:ㅂ!"
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

    restaurants = pd.read_csv(path + 'restaurants(revised).csv', engine='python', encoding='CP949')

    def return_best_restaurants(cat, delivery):
        cut_countTRUE = 4 if cat != '치킨' else 1  # 치킨이 선택되면 cut_countTRUE에 1, 나머지는 4를 주도록 설정.
        if delivery == True:
            best_restaurants = restaurants[restaurants[cat] & (restaurants['countTRUE'] <= cut_countTRUE)].sort_values(
                by=['review_avg', 'review_count'], ascending=False).head(5).astype('string')
        else:
            best_restaurants = restaurants[restaurants[cat] & (restaurants['countTRUE'] <= cut_countTRUE)]
            best_restaurants['score'] = best_restaurants['review_avg'] / best_restaurants['distance']
            best_restaurants = best_restaurants.sort_values(by='score', ascending=False).head(5).astype('string')
        return best_restaurants

    first_restaurants = return_best_restaurants(preferSorted.index[0], delivery)
    second_restaurants = return_best_restaurants(preferSorted.index[1], delivery)
    third_restaurants = return_best_restaurants(preferSorted.index[2], delivery)

    # 아래는 printMent를 구성
    printMent0 = "*오늘 점심 메뉴 추천은 다음과 같아요!*\n"
    printMent1 = ">>> :first_place_medal: " + preferSorted.index[0] + "    ( 점수: " + str(
        round(preferSorted[0] * 100 / (5 ** memberLen), 1)) + " )\n"
    printMent1_1 = "```1위: " + first_restaurants['name'].values[0] + "   (평점: " + \
                   first_restaurants['review_avg'].values[0] + ")\n"
    printMent1_2 = "2위: " + first_restaurants['name'].values[1] + "   (평점: " + first_restaurants['review_avg'].values[
        1] + ")\n"
    printMent1_3 = "3위: " + first_restaurants['name'].values[2] + "   (평점: " + first_restaurants['review_avg'].values[
        2] + ")\n"
    printMent1_4 = "4위: " + first_restaurants['name'].values[3] + "   (평점: " + first_restaurants['review_avg'].values[
        3] + ")\n"
    printMent1_5 = "5위: " + first_restaurants['name'].values[4] + "   (평점: " + first_restaurants['review_avg'].values[
        4] + ")```\n"
    printMent2 = " :second_place_medal: " + preferSorted.index[1] + "    ( 점수: " + str(
        round(preferSorted[1] * 100 / (5 ** memberLen), 1)) + " )\n"
    printMent2_1 = "```1위: " + second_restaurants['name'].values[0] + "   (평점: " + \
                   second_restaurants['review_avg'].values[0] + ")\n"
    printMent2_2 = "2위: " + second_restaurants['name'].values[1] + "   (평점: " + second_restaurants['review_avg'].values[
        1] + ")\n"
    printMent2_3 = "3위: " + second_restaurants['name'].values[2] + "   (평점: " + second_restaurants['review_avg'].values[
        2] + ")\n"
    printMent2_4 = "4위: " + second_restaurants['name'].values[3] + "   (평점: " + second_restaurants['review_avg'].values[
        3] + ")\n"
    printMent2_5 = "5위: " + second_restaurants['name'].values[4] + "   (평점: " + second_restaurants['review_avg'].values[
        4] + ")```\n"
    printMent3 = " :third_place_medal: " + preferSorted.index[2] + "    ( 점수: " + str(
        round(preferSorted[2] * 100 / (5 ** memberLen), 1)) + " )\n"
    printMent3_1 = "```1위: " + third_restaurants['name'].values[0] + "   (평점: " + \
                   third_restaurants['review_avg'].values[0] + ")\n"
    printMent3_2 = "2위: " + third_restaurants['name'].values[1] + "   (평점: " + third_restaurants['review_avg'].values[
        1] + ")\n"
    printMent3_3 = "3위: " + third_restaurants['name'].values[2] + "   (평점: " + third_restaurants['review_avg'].values[
        2] + ")\n"
    printMent3_4 = "4위: " + third_restaurants['name'].values[3] + "   (평점: " + third_restaurants['review_avg'].values[
        3] + ")\n"
    printMent3_5 = "5위: " + third_restaurants['name'].values[4] + "   (평점: " + third_restaurants['review_avg'].values[
        4] + ")```"
    return printMent0 + printMent1 + printMent1_1 + printMent1_2 + printMent1_3 + printMent1_4 + printMent1_5 + printMent2 + printMent2_1 + printMent2_2 + printMent2_3 + printMent2_4 + printMent2_5 + printMent3 + printMent3_1 + printMent3_2 + printMent3_3 + printMent3_4 + printMent3_5


def revise_restaurants_csv():
    restaurants = pd.read_csv('restaurants.csv', engine='python', encoding='CP949')
    restaurants = restaurants.drop_duplicates(['id'])  # 중복 데이터 삭제
    restaurants = restaurants[~restaurants['name'].str.contains('CU|GS')]  # 편의점 삭제
    restaurants = restaurants[restaurants.begin.str.split(':').str[0].astype('int') <= 11]  # 12시 이후 오픈 삭제
    restaurants['국밥'] = restaurants['menu_list'].str.contains('국밥') | restaurants['name'].str.contains('국밥')
    restaurants['찌개, 탕'] = (restaurants['menu_list'].str.contains('찌개|탕|찌게|전골|강된장') | restaurants['name'].str.contains(
        '찌개|탕|찌게|전골|강된장')) & (~restaurants['menu_list'].str.contains('탕수육'))
    restaurants['찜류(찜닭, ...)'] = restaurants['menu_list'].str.contains('찜|족발|보쌈') | restaurants['name'].str.contains(
        '찜|족발|보쌈')
    restaurants['냉면/밀면'] = restaurants['menu_list'].str.contains('냉면|밀면') | restaurants['name'].str.contains('냉면|밀면')
    restaurants['월남쌈'] = restaurants['menu_list'].str.contains('월남쌈|샤브') | restaurants['name'].str.contains('월남쌈|샤브')
    restaurants['라멘/국수'] = restaurants['menu_list'].str.contains('라멘|국수') | restaurants['name'].str.contains('라멘|국수')
    restaurants['비빔밥/덮밥'] = restaurants['menu_list'].str.contains('비빔밥|덮밥') | restaurants['name'].str.contains('비빔밥|덮밥')
    restaurants['도시락'] = restaurants['menu_list'].str.contains('도시락') | restaurants['name'].str.contains('도시락')
    restaurants['정식'] = restaurants['menu_list'].str.contains('백반|정식') | restaurants['name'].str.contains('백반|정식')
    restaurants['김밥'] = restaurants['menu_list'].str.contains('김밥') | restaurants['name'].str.contains('김밥')
    restaurants['분식'] = restaurants['menu_list'].str.contains('떡볶이') | restaurants['name'].str.contains('떡볶이')
    restaurants['중국집'] = restaurants['menu_list'].str.contains('짬뽕|탕수육|짜장면|자장면') | restaurants['name'].str.contains(
        '짬뽕|탕수육|짜장면|자장면')
    restaurants['돈까스'] = restaurants['menu_list'].str.contains('돈가스|까스|카츠') | restaurants['name'].str.contains(
        '돈가스|까스|카츠')
    restaurants['스시'] = (restaurants['menu_list'].str.contains('초밥|스시|사시미|회') | restaurants['name'].str.contains(
        '초밥|스시|사시미|회')) & (~restaurants['menu_list'].str.contains('육회'))
    restaurants['치킨'] = (restaurants['menu_list'].str.contains('치킨|통닭|후라이드|강정') | restaurants['name'].str.contains(
        '치킨|통닭|후라이드|강정')) & (~restaurants['menu_list'].str.contains('버거|토스트|덮밥')) & (
                            ~restaurants['name'].str.contains('바게뜨|토스트|돈까스|카페|버거'))
    restaurants['피자'] = restaurants['menu_list'].str.contains('피자') | restaurants['name'].str.contains('피자')
    restaurants['샌드위치(써브웨이, 이삭 등)'] = restaurants['menu_list'].str.contains('샌드위치|토스트|버거') | restaurants[
        'name'].str.contains('샌드위치|토스트|브웨이|버거')
    restaurants['파스타/ 필라프'] = restaurants['menu_list'].str.contains('파스타|필라프') | restaurants['name'].str.contains(
        '파스타|필라프')
    restaurants['countTRUE'] = restaurants.loc[:, '국밥':'파스타/ 필라프'].apply(pd.Series.value_counts, axis=1)[True].fillna(0)
    restaurants.to_csv("restaurants(revised).csv", mode='w', encoding='CP949', index=None)