from flask import render_template, request, redirect, url_for, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from src import app, login
from src.admin import *
import os
import cv2
from src.services import *

UPLOAD_FOLDER_ATTENDANCE = "attendance_temp"
UPLOAD_FOLDER = 'temp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_ATTENDANCE, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/students', methods=['get'])
def get_all_students():
    list_sinhvien = get_all_user_by_role('student')
    return render_template('students.html', students=list_sinhvien)

@app.route("/students-in-course", methods=["GET"])
def students_in_course():
    course_id = request.args.get("course_id")
    courses = get_all_courses()
    students_list = get_all_student_by_course_id(course_id) if course_id else []
    return render_template("list_student_by_course.html", students=students_list, courses=courses, selected_course=course_id)

@app.route("/courses/<user_id>")
def get_course_by_user(user_id):
    courses = get_all_course_by_user(user_id)
    if not courses:
        return jsonify({'message': 'Không có khóa học nào của sinh viên'}), 404
    return render_template("get_courses_by_student.html", courses=courses)

@app.route('/user-login', methods=['GET', 'POST'])
def user_signin():
    err_msg = ""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = check_login(email=email, password=password)
        if user:
            login_user(user=user)
            next = request.args.get('next', 'home')
            return redirect(url_for(next))
        else:
            err_msg = "Sai tên đăng nhập hoặc mật khẩu!"

    return render_template('login.html', err_msg=err_msg)

@app.route('/admin-login', methods=['POST'])
def admin_login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = check_admin_login(email=email, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')


@login.user_loader
def user_load(user_id):
    return get_user_by_id(user_id=user_id)

@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ''
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        user_id = email.split('@')[0]
        if str(password) == str(confirm):
            avatar = request.files.get('avatar')
            avatar.save(os.path.join('temp', avatar.filename))
            add_user(user_id=user_id, name=name, email=email, password=password, avatar=avatar)
            return redirect(url_for('admin'))
        else:
            err_msg = "Mật khẩu không khớp!"

    return render_template('register.html', err_msg=err_msg)

@app.route("/attendance", methods=["POST", "GET"])
def attendance():
    course_id = request.args.get('course_id', '').strip()
    if request.method == 'POST':
        course_id = request.form.get('course_id').strip()
        image_file = request.files.get('file')
        file_name = image_file.filename

        file_path = os.path.join(UPLOAD_FOLDER_ATTENDANCE, file_name)
        image_file.save(file_path)
        img = cv2.imread(file_path)
        if course_id and image_file:
            results = check_in(img, course_id)
        else:
            os.remove(file_path)
            return render_template('attendance.html', message=None, course_id=course_id)
        os.remove(file_path)
        return render_template('attendance.html', message=results["message"], course_id=course_id)
    return render_template('attendance.html', message=None, course_id=course_id)
