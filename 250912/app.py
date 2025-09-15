# 라이브러리 로드 
from flask import Flask, render_template, request, redirect
import pandas as pd 

# render_template() -> html문서를 불러와서 문자열으로 변환
# html문서에서 {{ python code }}, {%=변수명%} 해당하는 부분은 찾아서 형태를 변환
# html문서를 불러오는 기본 경로가 현재 경로에서 templates 하위 폴더

# Flask class 생성 -> 웹 서버를 구축하는 기능
# 해당 class에는 생성시 호출이 되는 생성자 함수 
    # 필수 인자 1개 -> 현재 파일의 이름(app.py)
    # __name__ : 파일의 이름
app = Flask(__name__)

# 네비게이션 함수 
# base url -> 127.0.0.1:5000
# route({주소값 -> 상대주소}) -> base_url + 상대 주소 -> 요청이 들어왔을때
# 바로 아래의 함수와 연결 (함수를 호출)
@app.route('/')
def index():
    # return "Hello World"
    return render_template('index.html')

@app.route('/second')
def second():
    # return "Second Page"
    # return "<a href='http://www.google.com'>Google</a>"
    # templates 폴더 안에 있는 second.html를 불러와서 되돌려준다. 
    # 유저가 보낸 데이터를 확인
    # 데이터를 get 방식으로 보내면 request안에 args 안에 데이터가 존재 
    # request.args는 dict 형태의 데이터 
    print(request.args)
    _text = request.args['input_text']
    _pass = request.args['input_pass']
    print(f"유저가 입력한 text는 {_text}이고 password는 {_pass}이다")
    # _text 가 'test'이고 _pass가 '1234'와 같다면 로그인이 성공
    # second.html을 보여준다. 
    if (_text == "test") & (_pass == '1234'): 
        df = pd.read_csv("../csv/aapl.csv").head(10)
        # df를 dict형태로 변환
        data = df.to_dict(orient='records')
        # columns의 목록을 html에 보낸다. 
        cols = list(df.columns)
        # x축의 데이터 -> list
        x = df['Date'].to_list()
        y = df['Adj Close'].to_list()
        return render_template("second.html", 
                               table_data = data, 
                               cols = cols, 
                               x_data = x, 
                               y_data = y)                                       
    else:
        # 로그인 페이지로 되돌아간다. 
        # 127.0.0.1:5000/으로 이동한다. 
        return redirect('/')

@app.route("/third", methods=['post'])
def third():
    print(redirect)
    # post 방식으로 데이터를 보낸다면 
    # request안에 form에 데이터가 존재 
    _text = request.form['input_text']
    _pass = request.form['input_pass']
    print(f"입력한 text는 {_text}이고 비밀번호는 {_pass}이다")
    return ""


# 웹 서버를 시작한다. 
# host 매개변수 -> 허용주소 목록 (기본값은 로컬 피씨만 접속, 0.0.0.0 변경시 모든 주소에서 접속 가능)
# port 매개변수 -> 해당 웹서버의 지정되는 포트 번호(5000 기본값)
# debug 매개변수 -> 디버그모드 on/off (off(False) 기본값)
app.run(debug=True)


# 유저와 서버간의 데이터를 주고 받는다. 
# 데이터 보내는 방식(주소 의 생성 방식)  ->  get // post
# 유저가 보낸 데이터를 서버가 확인 -> 요청 메시지 안에 데이터가 존재