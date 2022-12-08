import datetime

from flask import Flask, render_template, request, jsonify
import pymysql
app = Flask(__name__)


if not app.debug:
    # 즉 debug=true면 이는 false로서 아래 함수가 돌아간다.
    # 실제 상용화단계에서 로깅을 진행해라는 의미이다
    import logging
    from logging.handlers import RotatingFileHandler
    # logging 핸들러에서 사용할 핸들러를 불러온다.
    file_handler = RotatingFileHandler(
        'dave_server.log', maxBytes=2000, backupCount=10)
    file_handler.setLevel(logging.WARNING)
    # 어느 단계까지 로깅을 할지를 적어줌
    # app.logger.addHandler() 에 등록시켜줘야 app.logger 로 사용 가능
    app.logger.addHandler(file_handler)

@app.errorhandler(404)
def page_not_found(error):
    asctime = datetime.datetime.now()
    app.logger.error(f'시간:{asctime}/이것은 중요한 에러입니다. page_not_found에서 일어났습니다.')
    return "<h1>해당 경로에 맞는 웹페이지가 없습니다. 문제가 지속되면, 죄송하지만 관리자에게 연락해주세요</h1>", 404

@app.route('/')
def home():

    # rand() 배치를 무작위로
    # data return일경우 자료 하나하나, result return 일경우 자료 뭉치
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='3d720307',
                           db='dailycafe',
                           charset='utf8')
    sql = "SELECT * FROM cafelist ORDER BY rand() LIMIT 4"

    with conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchall()
            for data in result:
                print(data)
    return render_template('index.html', result=result)


@app.route("/searchdata",methods=["POST","GET"])
def searchdata():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='3d720307',
                           db='dailycafe',
                           charset='utf8')
    if request.method == 'POST':
        search_word = request.form['search_word']
        query = "SELECT * from cafelist WHERE shopname LIKE '%{}%' ORDER BY idnumber DESC LIMIT 500".format(search_word)

        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                print(search_word)
                cur.execute(query)
                result = cur.fetchall()

    return jsonify({'data': render_template('response.html', result = result)})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
