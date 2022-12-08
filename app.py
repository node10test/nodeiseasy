from flask import Flask, render_template, request, session, redirect, url_for
import pymysql
import bcrypt

app = Flask(__name__)
# 로컬 mysql 연결 by TK

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='1231234',
                       db='user',
                       charset='utf8')
cur = conn.cursor()


# 데이터 보내주기, 완료시 로그인페이지로 이동 by TK
@app.route('/post/users', methods=['GET', 'POST'])
def user_post():
    email = request.form['email']
    pass_word = request.form['password']
    b = bcrypt.hashpw(pass_word.encode('utf-8'), bcrypt.gensalt())
    insert_password_hash = b.decode()
    name_re = request.form['name']
    sql = """INSERT INTO users(email, password, name) VALUES('%s','%s','%s')""" % (email, insert_password_hash, name_re)
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
            return render_template('login.html')


# 회원가입 페이지 by TK
@app.route('/')
def signup():
    return render_template('signup.html')


# 임시로만든 로그인페이지 by TK
@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
