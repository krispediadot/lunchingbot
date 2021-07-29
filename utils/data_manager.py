from datetime import datetime, date
import csv

path = 'core/data/'  # .csv 파일들이 저장된 경로 입력

def updateMenu(targetDate=None, menuName=None, memberList=None, delivery=True):
    filename = 'menulog.csv'

    f = open(path + filename, 'a', newline='')
    wr = csv.writer(f)

    targetDate = datetime.today().strftime("%Y-%m-%d")
    wr.writerow([targetDate, menuName, memberList, delivery])

    f.close()

def getMenuCategory():
    filename = 'menu.csv'

    f = open(path + filename, 'r', encoding='CP949')
    rd = csv.reader(f)

    return [line[0] for line in rd][1:]

def getMemberList():
    filename = 'menu.csv'

    f = open(path + filename, 'r', encoding='CP949')
    rd = csv.reader(f)

    return [line for line in rd][0]

if __name__ == "__main__":
    getMenuCategory()