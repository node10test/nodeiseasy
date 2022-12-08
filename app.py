from flask import Flask, render_template, request, session, redirect, url_for
import pymysql
import bcrypt
from flask import flash

app = Flask(__name__)
app.secret_key = 'any random string'

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='1231234',
                       db='user',
                       charset='utf8')
cur = conn.cursor()


@app.route('/home')
def home():
    if 'email' not in session:
        email = None
        name = None
        flash('로그인 하세요!')
        return render_template('register.html', email=email, name=name)

    return render_template('login.html', email=session['email'], name=session['name'])


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/post/users', methods=['GET', 'POST'])
def user_post():
    email = request.form['email']
    pass_word = request.form['password']
    b = bcrypt.hashpw(pass_word.encode('utf-8'), bcrypt.gensalt())
    name_re = request.form['name']
    sql = "INSERT INTO users(email, password, name) VALUES(%s,%s,%s)"
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, (email, b, name_re))
            conn.commit()
            return render_template('login.html')
            # session['name'] = name_re
            # session['email'] = email
            # return redirect(url_for('login'))


# conn.commit() > 데이터 베이스 반영할때 들어감
# conn.commit()
# cur = conn.cursor()
# sql = "INSERT INTO user(id, % s, % s, % s) VALUE(, email, password, name_re)"


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curs = conn.cursor(pymysql.cursors.DictCursor)
        curs.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = curs.fetchone()
        curs.close()
        print(user)
        print(password)
        print(bcrypt.hashpw(password, user['password'].encode('utf-8')))
        print(user['password'].encode('utf-8'))

        if user is not None:
            print(1)
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                print(2)
                session['email'] = user['email']
                # session['email'] = user['email']
                print(session.get('email'))
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


# @app.route('/user', methods=['POST'])
# def user_post():
#     email_receive = request.form['email_give']
#     password_receive = request.form['password_give']
#     name_receive = request.form['name_give']
#     return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})

# @app.route('/test', methods=['GET'])
# def test_get():
#     title_receive = request.args.get('title_give')
#     print(title_receive)
#     return jsonify({'result': 'success', 'msg': '이 요청은 GET!'})
#
#
# @app.route('/test', methods=['POST'])
# def test_post():
#     title_receive = request.form['title_give']
#     print(title_receive)
#     return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
