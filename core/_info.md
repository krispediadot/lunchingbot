"""<br>
작성자: 김근우<br>
작성일: 2021.08.13<br>
"""

### prefer 설명
1. def preferMenu(members, delivery=True):<br>
    - 입력: <br>
        members = 점심을 먹을 멤버들이 포함된 튜플 또는 리스트,<br>
        delivery(default = True) = 배달 여부 boolean (True = 내부(배달), False = 외부)
    - 출력: <br>
        printMent0~3-5 = 슬랙에 나타낼 메시지 string
    - 로직1(3일 가중치):<br>
        가중치 값: 1일전 = 0.6, 2일전 = 0.2, 3일전 = 0
    - 로직2(선호도):<br>
        계산법: 점심을 먹는 멤버들의 선호도를 곱한 값으로 순위를 매김
    <br><br>
    1. def return_best_restaurants(cat, delivery):<br>
        - 입력: <br>
            cat = 음식 카테고리, (preferMenu 연산 중에 추천한 카테고리(string)가 cat으로 입력됨)<br>
            delivery = 배달 여부 boolean (True = 내부(배달), False = 외부)<br>
        - 출력: <br>
            best_restaurants = 음식점 점수를 기준으로 상위 5개 음식점 목록(dataframe)을 반환
        - 내부 변수: <br>
            cut_countTRUE = cat이 '치킨'이면 1, 아니면 4인 값.
        - 로직(점수):<br>
            delivery가 True면 리뷰별점순(1순위)으로 정렬. 별점이 동등이면 리뷰 개수(2순위)로 정렬<br>
            delivery가 False면 리뷰별점/거리 순으로 정렬.
    <br><br>
1. def revise_restaurants_csv():<br>
    - 입출력: 없음<br>
    - 로직<br>
        1. path에 저장된 restaurants.csv를 불러와서 restaurants(revised).csv를 저장<br>
        1. restaurants의 상호명과 메뉴명을 기준으로, 특정 문자열이 포함되면 특정 카테고리로 분류하는 column(dtype = boolean)을 생성<br>
        1. 'countTRUE' column은 분류된 카테고리의 개수를 세어 입력 (이후 return_best_restaurants()에서 cut_countTRUE의 연산에 반영되는 column임)<br>
