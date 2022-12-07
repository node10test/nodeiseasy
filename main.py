from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from flask import flash
import pymysql
import bcrypt
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD"
# app.permanent_session_lifetime = timedelta(minutes=1)

db = pymysql.connect(host='127.0.0.1', user='root', password='12345', db='daily_cafe', charset='utf8')

@app.route('/')
def home():
    if 'email' not in session:
        email = None
        name = None
        flash('로그인 하세요!')
        return render_template('register.html', email=email, name=name)

    return render_template('login.html', email=session['email'], name=session['name'])

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt()) # bcrypt 로 암호화된 패스워드 생성
        print(hash_password)

        curs = db.cursor(pymysql.cursors.DictCursor)
        # 암호화된 패스워드를 DB에 저장
        sql = 'INSERT INTO users (name, email, password) VALUES (%s, %s, %s)'
        curs.execute(sql, (name, email, hash_password,))
        db.commit()
        session['name'] = name      # session에 이름, 이메일 저장
        session['email'] = email
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curs = db.cursor(pymysql.cursors.DictCursor)
        curs.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = curs.fetchone()
        curs.close()

        if user is not None:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['email'] = user['email']
                return render_template('home.html')
            else:
                msg = '이메일 또는 비밀번호를 확인해주세요'
                return render_template('login.html', msg=msg)
        else:
            msg = '이메일 또는 비밀번호를 확인해주세요'
            return render_template('login.html', msg=msg)

    else:
        return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('home.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run('0.0.0.0', port=5000, debug=True)

