import os
import pymysql
from flask import Flask, render_template, jsonify, request, redirect, flash, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # flash 사용
app.config["SECRET_KEY"] = "1234"

db = pymysql.connect(user="root", passwd="qwe1357asd!", host="localhost", db="dailycafe", charset="utf8")
curs = db.cursor()

@app.route('/')
def home():
    return redirect('/my_page')

@app.route('/my_page')
def my_page():
    return render_template('my_page.html')


@app.route('/edit')
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
    sql = '''SELECT `name`,`desc`  FROM `user` AS u WHERE u.id = %s'''

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

    sql = '''UPDATE `user` SET name=%s, `desc`=%s  WHERE id=%s;'''

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

    @app.route('/upload', methods=["POST"])
    def upload_file():
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/")

        return jsonify({"msg": "good"})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
