from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
import pymysql
import bcrypt
import os
from werkzeug.utils import secure_filename
import urllib.request
from datetime import datetime

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

#위 TK 아래 태현

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



UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # flash 사용
app.config["SECRET_KEY"] = "1234"

db = pymysql.connect(user="root", passwd="qwe1357asd!", host="localhost", db="dailycafe", charset="utf8")
curs = db.cursor()

# @app.route('/')
# def home():
#     return redirect('/my_page')

@app.route('/my_page')
def my_page():
    return render_template('my_page.html')

@app.route('/edit_page')
def edit_page():
    return render_template('edit_page.html')

@app.route('/users/<id>', methods=['GET'])
def get_users(id):
    db = pymysql.connect(user="root",
                         passwd="qwe1357asd!",
                         host="localhost",
                         db="dailycafe",
                         charset="utf8")
    # connection 으로부터 cursor(fetch 역할) 생성
    curs = db.cursor()
    # 쿼리문 작성
    sql = '''SELECT `name`,`desc` FROM `users` AS u WHERE u.id = %s'''

    # 쿼리 실행
    curs.execute(sql, id)

    # 결과 받고 컨트롤 하기 / 전체 데이터 패치
    rows = curs.fetchall()

    print(rows)

    db.commit()
    db.close()

    result = {
        "name": rows[0][0],
        "desc": rows[0][1]
    }

    return jsonify({'users': result}), 200


@app.route('/users/<id>', methods=['POST'])
def post_users(id):
    db = pymysql.connect(user="root", passwd="qwe1357asd!", host="localhost", db="dailycafe", charset="utf8")
    curs = db.cursor()

    name_receive = request.form['name']
    desc_receive = request.form['desc']

    sql = '''UPDATE `users` SET name=%s, `desc`=%s  WHERE id=%s;'''

    curs.execute(sql, (name_receive, desc_receive, id))

    db.commit()
    db.close()

    flash("수정이 완료되었습니다")
    return render_template("my_page.html")

    # return redirect('/')
    # return jsonify({'msg': '수정이 완료되었습니다'}), 200

    # 파일 업로드
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    print(0)
    db = pymysql.connect(user="root", passwd="qwe1357asd!", host="localhost", db="dailycafe", charset="utf8")
    cur = db.cursor(pymysql.cursors.DictCursor)
    print(1)
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        # print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute("INSERT INTO images (file_name,upload_time) VALUES (%s,%s)", [filename,now])
                db.commit()
            print(file)
        db.close()
        flash('사진이 성공적으로 업로드 되었어요!')
    return redirect('/edit_page')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
