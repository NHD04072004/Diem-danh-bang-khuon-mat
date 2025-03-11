from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from src import app
import os
import cv2
from src.services import *

UPLOAD_FOLDER = "src/static/images"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ""

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = check_login(username=username, password=password)
        if user:
            login_user(user=user)
            next = request.args.get('next', 'home')
            return redirect(url_for(next))
        else:
            err_msg = "Sai tên đăng nhập hoặc mật khẩu"

    return render_template('login.html', err_msg=err_msg)

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('attendance.html', message="Không có ảnh upload!", result=None)
        file = request.files['file']
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        image = cv2.imread(filepath)
        if image is None:
            os.remove(filepath)
            return render_template('attendance.html', message="Không thể đọc ảnh!", result=None)

        course_id = request.form.get('course_id', '1')
        results = check_in(image, course_id)

        os.remove(filepath)

        if results["success"]:
            return render_template('attendance.html', message=results["message"], result="present")
        else:
            return render_template('attendance.html', message=results["message"], result="absent")

    return render_template('attendance.html', message=None, result=None)
