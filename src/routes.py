from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from src import app
import os
import cv2
from src.services import *

UPLOAD_FOLDER = "src/static/images"

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/students", methods=["GET"])
def students():
    course_id = request.args.get("course_id")
    courses = get_all_courses()
    students_list = get_all_student_by_course_id(course_id) if course_id else []
    return render_template("list_student-by-course.html", students=students_list, courses=courses, selected_course=course_id)

@app.route('/user-login', methods=['GET', 'POST'])
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

@app.route("/attendance", methods=["POST", "GET"])
def attendance():
    if request.method == 'GET':
        return render_template('attendance.html')
    elif request.method == 'POST':
        course_id = request.form.get('course_id').strip()
        image_file = request.files.get('file')
        file_name = image_file.filename

        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        image_file.save(file_path)
        img = cv2.imread(file_path)
        if course_id and image_file:
            results = check_in(img, course_id)
        else:
            os.remove(file_path)
            return render_template('attendance.html', result=None, message=None)
        os.remove(file_path)
        return render_template('attendance.html', result=results["success"], message=results["message"])
    return render_template('attendance.html', result=None, message=None)