from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

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
