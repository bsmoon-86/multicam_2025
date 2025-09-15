from flask import Flask, request, render_template, url_for

# __name__ : 현재 파일의 이름
app = Flask(__name__)

# ===========================
# 웹서버를 사용할 주소들의 목록

# base_url -> 127.0.0.1:5000
# base_url + '/' 주소로 요청이 들어왔을때
# 바로 아래의 함수를 호출
# 함수를 생성할때 유의할 점은 함수의 이름은 중복 불가
@app.route('/')
def index():
    # 현재 작업 경로에서 하위 디렉토리인 
    # templates 안에 있는 index.html를 되돌려준다.
    return render_template('index.html')








# ===========================

# 웹 서버를 실행 
# debug= True는 파일이 저장될때 마다 웹서버를 자동으로 재시작
app.run(debug=True)