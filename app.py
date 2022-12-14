import ConnectSQl as connectsql
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
import pymysql
import bcrypt
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_paginate import Pagination, get_page_args, get_page_parameter
#db 정보에 대한 변수(f스트링으로 받음)
mysqluser = "root"
mysqldb = "dailycafe"
host = "localhost"
pwd = "3d720307"
logfiledir = "server.log"


app = Flask(__name__)
app.secret_key = 'any random string'

# if not app.debug:
#     # 즉 debug=true면 이는 false로서 아래 함수가 돌아간다.
#     # 실제 상용화단계에서 로깅을 진행해라는 의미이다
#     import logging
#     from logging.handlers import RotatingFileHandler
#
#     # logging 핸들러에서 사용할 핸들러를 불러온다.
#     file_handler = RotatingFileHandler(
#         f'{logfiledir}', maxBytes=2000, backupCount=10)
#     file_handler.setLevel(logging.WARNING)
#     # 어느 단계까지 로깅을 할지를 적어줌
#     # app.logger.addHandler() 에 등록시켜줘야 app.logger 로 사용 가능
#     app.logger.addHandler(file_handler)
#
#
# @app.errorhandler(404)
# def page_not_found(error):
#     asctime = datetime.datetime.now()
#     app.logger.error(f'시간:{asctime}/page_not_found 오류입니다.')
#     return "<h1>해당 경로에 맞는 웹페이지가 없습니다. 문제가 지속되면, 죄송하지만 관리자에게 연락해주세요</h1>", 404


@app.route('/')
def home():
    # rand() 배치를 무작위로
    # data return일경우 자료 하나하나, result return 일경우 자료 뭉치
    conn = pymysql.connect(host=f'{host}',
                           user=f'{mysqluser}',
                           password=f'{pwd}',
                           db=f'{mysqldb}',
                           charset='utf8')
    sql = "SELECT * FROM cafelist ORDER BY rand() LIMIT 4"
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchall()
            for data in result:
                print(data)
    return render_template('index.html', result=result)


@app.route("/searchdata", methods=["GET"])
def searchdata():
    conn = pymysql.connect(host=f'{host}',
                           user=f'{mysqluser}',
                           password=f'{pwd}',
                           db=f'{mysqldb}',
                           charset='utf8')
    if request.method == 'GET':
        search_word = request.args['search_word']
        pages = 0
        if (request.args.getlist('page')):
            pages = (int(request.args.getlist('page')[0]) - 1) * 10
            print('page', pages)
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                per_page = 10
                page, _, offset = get_page_args(per_page=per_page)
                # db = pymysql.connect(host='localhost', user='root', db='spartagram', password='12345678', charset='utf8')
                curs.execute("SELECT * from cafelist WHERE shopname LIKE '%{}%' ORDER BY idnumber DESC;".format(search_word))
                all_count = len(curs.fetchall())
                print(all_count)
                # '%{}%'을 쓰면서 %s로 변수를 받을께 있다!? = f스트링이 답이다
                sql = f"SELECT * from cafelist WHERE shopname LIKE '%{search_word}%' ORDER BY idnumber DESC LIMIT {per_page} OFFSET {pages};"
                print('sql', sql);
                curs.execute(sql)
                data_list = curs.fetchall()
                print(data_list)
                pagination = Pagination(page=page, per_page=per_page, total=all_count, record_name='searchdata',
                                        css_framework='foundation', bs_version=5,prev_label="<<", next_label=">>")
                print("this is pagination", pagination)
                check = False
                return jsonify({'data': render_template('response.html', data_lists=data_list, pagination=pagination)})


@app.route("/searchdata_auto", methods=["POST", "GET"])
def searchdata_auto():
    conn = pymysql.connect(host=f'{host}',
                           user=f'{mysqluser}',
                           password=f'{pwd}',
                           db=f'{mysqldb}',
                           charset='utf8')
    if request.method == 'GET':
        search_word = request.args['search_word']
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as curs:
                per_page = 10
                page, _, offset = get_page_args(per_page=per_page)
                # db = pymysql.connect(host='localhost', user='root', db='dailycafe', password='3d720307', charset='utf8')
                curs.execute("SELECT * from cafelist WHERE shopname LIKE '%{}%' ORDER BY 번호 DESC;".format(search_word))
                all_count = len(curs.fetchall())
                print(all_count)
                # '%{}%'을 쓰면서 %s로 변수를 받을께 있다!? = f스트링이 답이다
                sql = f"SELECT * from cafelist WHERE shopname LIKE '%{search_word}%' ORDER BY 번호 DESC LIMIT {per_page} OFFSET {offset};"
                curs.execute(sql)
                data_list = curs.fetchall()
                print(data_list)
                pagination = Pagination(page=page, per_page=per_page, total=all_count, record_name='searchdata',
                                        css_framework='foundation', bs_version=5)
                print("this is pagination", pagination)
                check = False
                # if page != None:
                #     return jsonify({'data': render_template('response.html', data_lists=data_list, pagination=pagination)})
                # else:
                return jsonify({'data': render_template('response.html', data_lists=data_list, pagination=pagination)})
                # if page ==1:
                #     return jsonify({'data': render_template('response.html',data_lists=data_list, pagination=pagination)})
                # else:
                #     return render_template('response.html', data_lists=data_list, pagination=pagination)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/post/users', methods=['GET', 'POST'])
def user_post():
    conn = pymysql.connect(host=f'{host}',
                           user=f'{mysqluser}',
                           password=f'{pwd}',
                           db=f'{mysqldb}',
                           charset='utf8')
    cur = conn.cursor()
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
    conn = pymysql.connect(host=f'{host}',
                           user=f'{mysqluser}',
                           password=f'{pwd}',
                           db=f'{mysqldb}',
                           charset='utf8')
    cur = conn.cursor()
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        print(user)
        print(password)

        if user is not None:
            print(1)
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                print(2)
                session['email'] = user['email']
                session['id'] = user['id']
                print(session.get('email'))
                sql = "SELECT * FROM cafelist ORDER BY rand() LIMIT 4"
                with conn:
                    with conn.cursor() as cur:
                        cur.execute(sql)
                        result = cur.fetchall()
                        for data in result:
                            print(data)
                return render_template('index.html', result=result)

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
    conn = pymysql.connect(host=f'{host}',
                           user=f'{mysqluser}',
                           password=f'{pwd}',
                           db=f'{mysqldb}',
                           charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM cafelist ORDER BY rand() LIMIT 4"
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchall()
            for data in result:
                print(data)
    return render_template('index.html', result=result)
# @app.route('/logout')
# def logout():
#     session.pop('email', None)
#     return redirect('/')

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # flash 사용


# app.config["SECRET_KEY"] = "1234"


# db = pymysql.connect(user="root", passwd="qwe1357asd!", host="localhost", db="dailycafe", charset="utf8")
# curs = db.cursor()

# @app.route('/')
# def home():
#     return redirect('/my_page')

@app.route('/my_page')
def my_page():
    if 'email' in session:
        email = session['email']
        return render_template('my_page.html')
    else:
        email = None
        return render_template('login.html')

@app.route('/edit_page')
def edit_page():
    print(123)
    return render_template('edit_page.html')


@app.route('/users', methods=['GET'])
def get_users():
    print(5678)
    id = session["id"]
    db = pymysql.connect(host=f'{host}',
                           user=f'{mysqluser}',
                           password=f'{pwd}',
                           db=f'{mysqldb}',
                           charset='utf8')
    # connection 으로부터 cursor(fetch 역할) 생성
    curs = db.cursor()
    # 쿼리문 작성
    sql = '''SELECT `name`,`desc`,`img` FROM `users` AS u WHERE u.id = %s'''

    # 쿼리 실행
    curs.execute(sql, id)

    # 결과 받고 컨트롤 하기 / 전체 데이터 패치
    rows = curs.fetchall()

    # print(rows)

    db.commit()
    db.close()
    # 결과 값 저장
    result = {
        "name": rows[0][0],
        "desc": rows[0][1],
        "img": rows[0][2]
    }

    return jsonify({'users': result}), 200


@app.route('/users', methods=['POST'])
def post_users():
    id = session["id"]
    db = pymysql.connect(host=f'{host}',
                           user=f'{mysqluser}',
                           password=f'{pwd}',
                           db=f'{mysqldb}',
                           charset='utf8')
    curs = db.cursor()

    name_receive = request.form['name']
    desc_receive = request.form['desc']

    sql = '''UPDATE `users` SET name=%s, `desc`=%s  WHERE id=%s;'''

    curs.execute(sql, (name_receive, desc_receive, id))

    db.commit()
    db.close()

    flash("수정이 완료되었습니다")
    return render_template("my_page.html")



# 파일 업로드
# rsplit은 뒤에서 부터의 값을 끊어주는 것 = 파일의 확장자명 저장
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['POST'])
def upload():

    db = pymysql.connect(host=f'{host}',
                           user=f'{mysqluser}',
                           password=f'{pwd}',
                           db=f'{mysqldb}',
                           charset='utf8')

    cur = db.cursor(pymysql.cursors.DictCursor)
    # 저장 시간 저장
    now = datetime.now()
    # 이메일 세션 저장
    id = session['id']
    # method = post 이면
    if request.method == 'POST':
         # input 타입의 태그 이름을 files에 저장
        files = request.files.getlist('files[]')
        for file in files:
            # 만약 파일이 {'png', 'jpg', 'jpeg'} 이와 같은 확장자와 일치하면
            if file and allowed_file(file.filename):
                # 어려워
                filename = secure_filename(file.filename)
                # 이건 더
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # users 테이블 안에 있는 세션 저장한 email의 img, upload_time의 컬럼 값을 변경
                sql = f'UPDATE users SET img="{filename}",upload_time="{now}" WHERE id="{id}";'
                # sql 쿼리문 실행
                cur.execute(sql)
                # 커밋 및 연결 종료
                db.commit()
                db.close()
        # alert 띄워주기
        flash('사진이 성공적으로 업로드 되었어요!')
    # edit 페이지로 돌아가기
    return redirect('/edit_page')


# from flask import Flask, render_template, session, url_for, request, redirect
# import pymysql


def connectsql():
    conn = pymysql.connect(host=f'{host}',
                           user=f'{mysqluser}',
                           password=f'{pwd}',
                           db=f'{mysqldb}',
                           charset='utf8')
    return conn

#
# @app.route('/')
# # 세션유지를 통한 로그인 유무 확인
# def index():
#     if 'email' in session:
#         email = session['email']
#
#         return render_template('index.html', logininfo=email)
#     else:
#         email = None
#         return render_template('index.html', logininfo=email)


@app.route('/post')
# board테이블의 게시판 제목리스트 역순으로 출력
def post():
    if 'email' in session:
        username = session['email']
    else:
        username = None

    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT id, name, title, wdate, view FROM board ORDER BY id DESC"  # ORDER BY 컬럼명 DESC : 역순출력, ASC : 순차출력
    cursor.execute(query)
    result = cursor.fetchall()
    # post_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('post.html', result=result, logininfo=username)


# postlist=postlist


@app.route('/post/content/<id>')
# 조회수 증가, post페이지의 게시글 클릭시 id와 content 비교 후 게시글 내용 출력
def content(id):
    if 'email' in session:
        email = session['email']
        conn = connectsql()
        cursor = conn.cursor()
        query = "UPDATE board SET view = view + 1 WHERE id = %s"
        value = id
        cursor.execute(query, value)
        conn.commit()
        cursor.close()
        conn.close()

        conn = connectsql()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT id, title, content FROM board WHERE id = %s"
        value = id
        cursor.execute(query, value)
        content = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('content.html', data=content, email=email)
    else:
        return render_template('Error.html')


@app.route('/post/edit/<id>', methods=['GET', 'POST'])
# GET -> 유지되고있는 email 세션과 현재 접속되어진 id와 일치시 edit페이지 연결
# POST -> 접속되어진 id와 일치하는 title, content를 찾아 UPDATE
def edit(id):
    if request.method == 'POST':
        if 'email' in session:
            email = session['email']

            edittitle = request.form['title']
            editcontent = request.form['content']

            conn = connectsql()
            cursor = conn.cursor()
            query = "UPDATE board SET title = %s, content = %s WHERE id = %s"
            value = (edittitle, editcontent, id)
            cursor.execute(query, value)
            conn.commit()
            cursor.close()
            conn.close()

            return render_template('editSuccess.html')
    else:
        if 'email' in session:
            email = session['email']
            conn = connectsql()
            cursor = conn.cursor()
            query = "SELECT name FROM board WHERE id = %s"
            value = id
            cursor.execute(query, value)
            data = [post[0] for post in cursor.fetchall()]
            cursor.close()
            conn.close()

            if email in data:
                conn = connectsql()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                query = "SELECT id, title, content FROM board WHERE id = %s"
                value = id
                cursor.execute(query, value)
                postdata = cursor.fetchall()
                cursor.close()
                conn.close()
                return render_template('edit.html', data=postdata, logininfo=email)
            else:
                return render_template('editError.html')
        else:
            return render_template('Error.html')


@app.route('/post/delete/<id>')
# 유지되고 있는 email 세션과 id 일치시 삭제확인 팝업 연결
def delete(id):
    if 'email' in session:
        email = session['email']
        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT name FROM board WHERE id = %s"
        value = id
        cursor.execute(query, value)
        data = [post[0] for post in cursor.fetchall()]
        cursor.close()
        conn.close()

        if email in data:
            return render_template('delete.html', id=id)
        else:
            return render_template('editError.html')
    else:
        return render_template('Error.html')


@app.route('/post/delete/success/<id>')
# 삭제 확인시 id와 일치하는 컬럼 삭제, 취소시 /post 페이지 연결
def deletesuccess(id):
    conn = connectsql()
    cursor = conn.cursor()
    query = "DELETE FROM board WHERE id = %s"
    value = id
    cursor.execute(query, value)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('post'))


@app.route('/write', methods=['GET', 'POST'])
# GET -> write 페이지 연결
# POST -> email, password를 세션으로 불러온 후, form에 작성되어진 title, content를 테이블에 입력
def write():
    if request.method == 'POST':
        if 'email' in session:
            email = session['email']
            usertitle = request.form['title']
            usercontent = request.form['content']
            conn = connectsql()
            cursor = conn.cursor()
            query = "INSERT INTO board(title, content, name) values (%s, %s, %s)"
            value = (usertitle, usercontent, email)
            print()
            cursor.execute(query,value)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('post'))
        else:
            return render_template('error.html')
    else:
        if 'email' in session:
            email = session['email']
            return render_template('write.html', logininfo=email)
        else:
            return render_template('error.html')



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
