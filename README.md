
![](https://github.com/krispediadot/lunchingbot/blob/master/run.png?raw=true)


### 사용법

1. utils/crawler.py 코드 작성
1. `config.ini` 파일에서 TOKEN, SECRET_SIGNING 값을 변경
1. ngrok(https://ngrok.com/download)을 설치
1. `ngrok http 3000` 명령어를 실행
1. `bot.py` 파일을 실행
1. `ngrok` 실행 결과로 나오는 url을 slack api 웹사이트에서 verify  (~~~/slack/events)
