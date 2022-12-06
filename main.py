from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)


@app.route('/')
def home():
    # rand() 배치를 무작위로
    # data일경우 자료 하나하나, result일경우 자료 뭉치
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
    return render_template('index.html', result=result, data=data)



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
