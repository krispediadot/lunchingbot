import requests
from bs4 import BeautifulSoup
import json
import time
import csv

headers = {"referer": "https://www.yogiyo.co.kr/mobile/",
           "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
           "x-apikey": "iphoneap",
           "x-apisecret": "fe5183cc3dea12bd0ce299cf110a75a2"
          }

categories = ['피자양식', '한식', '족발보쌈', '분식', '치킨', '중국집', '일식돈까스']

def updateRestaurantList(info:dict):
    """
            info = {"category": category,
                "id": "",
                "name": "",
                "phone": "",
                "lng": "",
                "lat": "",
                "distance": "",
                "review_avg": "",
                "review_count": "",
                "begin": "",
                "adjusted_delivery_fee": "",
                "min_order_amount": "",
                "menu_list": []
            }

    :param info:
    :return:
    """
    path = '../core/data/'  # .csv 파일들이 저장된 경로 입력
    filename = 'restaurants.csv'

    f = open(path + filename, 'a', newline='')
    wr = csv.writer(f)

    # for info in infor:
    wr.writerow([info['category'],
                 info['id'],
                 info['name'],
                 info['phone'],
                 info['lng'],
                 info['lat'],
                 info['distance'],
                 info['review_avg'],
                 info['review_count'],
                 info['begin'],
                 info['adjusted_delivery_fee'],
                 info['min_order_amount'],
                 info['menu_list']
                 ])

    f.close()

def getMenu(restaurantsID):
    params = {"add_photo_menu": "android",
              "add_one_dish_menu": "true",
              "order_serving_type": "delivery"
              }

    url = f"https://www.yogiyo.co.kr/api/v1/restaurants/{restaurantsID}/menu/"
    req = requests.get(url, headers=headers, params=params)
    data = req.json()

    infor = []

    #     for idx in range(len(data)):
    # 인기메뉴만 가져오려고 idx=1로 고정
    idx = 1
    for menu in data[idx]['items']:
        info = {"id": "",
                "name": "",
                "price": "",
                "review_count": ""
                }
        info['id'] = menu['id']
        info['name'] = menu['name']
        info['price'] = menu['price']
        info['review_count'] = menu['review_count']

        infor.append(info)

    return infor

def getRestaurants(category="", search=""):
    params = {"category": category,
              "itmes": 60,
              "lat": 35.1005913092695,
              "lng": 129.018514852669,
              "order": "rank",
              "page": 0,
              "search": search
              }
    url = "https://www.yogiyo.co.kr/api/v1/restaurants-geo/"

    req = requests.get(url, headers=headers, params=params)
    data = req.json()

    infor = []

    for restaurant in data['restaurants']:
        try:
            # review_count 20개 이상만 가져옴
            if (restaurant['review_count'] >= 20):
                info = {"category": category,
                        "id": "",
                        "name": "",
                        "phone": "",
                        "lng": "",
                        "lat": "",
                        "distance": "",
                        "review_avg": "",
                        "review_count": "",
                        "begin": "",
                        "adjusted_delivery_fee": "",
                        "min_order_amount": "",
                        "menu_list": []
                        }

                info['id'] = restaurant['id']
                info['name'] = restaurant['name']
                info['phone'] = restaurant['phone']
                info['lng'] = restaurant['lng']
                info['lat'] = restaurant['lat']
                info['distance'] = restaurant['distance']
                info['review_avg'] = restaurant['review_avg']
                info['review_count'] = restaurant['review_count']
                info['begin'] = restaurant['begin']
                info['adjusted_delivery_fee'] = restaurant['adjusted_delivery_fee']
                info['min_order_amount'] = restaurant['min_order_amount']
                info['menu_list'] = getMenu(restaurant['id'])

                infor.append(info)
                updateRestaurantList(info)
                time.sleep(3)
                print(info)
        except:
            continue

    return infor

if __name__ == "__main__":
    # getMenu(306957)
    # for i in range(len(categories)):
    res = getRestaurants(categories[5])
