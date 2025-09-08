import pymysql

# 데이터베이스 서버와 연결하여 query문을 사용하고 서버와의 연결을 종료하는 class 생성

# class 선언 
class MyDB:
    # 생성자 함수 
    # class 내부에서 사용하려는 변수의 데이터를 대입하는 함수 
    # class 생성 될때 한번만 실행이 되는 함수 
    # 입력 받을 데이터는 데이터베이스 서버의 정보 -> 기본값 설정(로컬 피씨의 데이터베이스 정보)
    def __init__(
            self, 
            _host = '127.0.0.1', 
            _port = 3306, 
            _user = 'root', 
            _pw = '1234', 
            _db_name = 'multicam'
    ):
        # self.변수를 생성 
        # class에서 사용할 서버의 정보를 변수에 저장 
        self.host = _host
        self.port = _port
        self.user = _user
        self.pw = _pw
        self.db_name = _db_name
    
    # query문과 데이터를 입력받아서 데이터베이스 서버에 질의를 보내는 함수 
    def sql_query(
            self, 
            _query, 
            *_data_list
    ):
        # _query 매개변수는 기본값이 존재하지 않으므로 필수 입력 공간 
        # _data_list는 인자의 개수를 가변으로 받는다. 개수가 0개면 ()을 생성

        # 데이터베이스 서버와의 연결 ( _db 변수를 생성하여 연결 )
        # pymysql.connet() 함수는 입력값이 서버의 정보 -> 
        # 서버의 정보는 self.host, self.port, self.user, self.pw, self.db_name 저장되어 있다. 
        # connect() 함수에 해당 데이터를 입력
        try:
            # self._db라는 변수를 확인
            self._db
            # 해당 변수가 선언이 되어있지 않다면 NameError 발생
        except:
            # self._db라는 변수가 존재하지 않을때 
            self._db = pymysql.connect(
                host = self.host, 
                port = self.port, 
                user = self.user, 
                password = self.pw, 
                db = self.db_name
            )
        # self._db를 이용하여 cursor를 생성 
        # ( class 내부에 다른 함수에서 사용이 가능하도록 self.변수로 등록 )
        self.cursor = self._db.cursor( pymysql.cursors.DictCursor )

        # _query와 _data_list를 이용하여 self.cursor에 질의 보낸다. 
        # 질의를 보내는 과정에서 문제가 발생하면 예외 처리를 한다. 
        try : 
            self.cursor.execute( _query, _data_list )
        except Exception as e:
            print(e)
            # query문에서 문제가 발생했으니 에러 메시지를 돌려주고 함수를 종료 
            return 'Query Error'
        # _query가 만약에 select 문이라면?
        if _query.lower().strip().startswith('select'):
            # query문이 select문인 경우
            # self.cursor에서 결과물을 돌려받는다. 
            result = self.cursor.fetchall()
        else:
            # select문이 아닌 경우 
            result = "Query OK"
        return result
    def db_commit(self):
        try:
            # self._db와 self.cursor를 동기화
            self._db.commit()
            print('commit 완료')
            # 데이터베이스 서버와의 연결을 종료 
            self._db.close()
            print('서버와의 연결 종료')
            # 변수를 삭제 
            del self._db
        except Exception as e:
            print(e)
            # self._db와 self.cursor가 생성되지 않은 상황 
            print("""데이터베이스 서버와의 연결이 없습니다. 
                  sql_query() 함수를 이용하여 서버와의 연결을 해주세요""")