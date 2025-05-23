from src import db
import numpy as np
from src.models import Courses, Course_Students, Attendance, Status, User, UserRole
from datetime import datetime, timedelta
from src.face_recognizer import FaceNet
import cv2
from src.utils import load_image_from_url
import chromadb

def get_all_user_by_role(role: str):
    if role == 'student':
        role = UserRole.STUDENT
    elif role == 'teacher':
        role = UserRole.TEACHER
    elif role == 'admin':
        role = UserRole.ADMIN

    sinhvien = db.session.query(
        User.id, User.user_id, User.name, User.email, User.avatar
    ).filter(User.role == role)

    return sinhvien.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def add_user(user_id, name, email, password, **kwargs):
    avatar = kwargs.get('avatar')
    role = kwargs.get('role')
    if role == 'student':
        role = UserRole.STUDENT
    elif role == 'teacher':
        role = UserRole.TEACHER
    elif role == 'admin':
        role = UserRole.ADMIN

    user = User(
        user_id=user_id,
        name=name.strip(),
        email=email,
        password_hash=password,
        avatar=avatar,
        role=role
    )
    db.session.add(user)
    db.session.commit()
    if avatar:
        client = chromadb.PersistentClient('./face_embedding_db')
        collection = client.get_or_create_collection(name='user_embeddings')
        if avatar.startswith("http://") or avatar.startswith("https://"):
            img = load_image_from_url(avatar)
        else:
            img = cv2.imread(avatar)
        facenet = FaceNet()
        face = facenet.face_detection(img)
        x, y, w, h = face["bounding_box"]
        face_img = img[y:h, x:w]
        avatar_embedding = facenet.face_embedding(face_img).numpy().tolist()

        collection.upsert(
            ids=[user_id],
            embeddings=[avatar_embedding],
            documents=[avatar],
            metadatas=[{"user_id": user_id}]
        )
        print("Has avatar")
        # facenet.face_display(img, face)

    else:
        print("Has not avatar")
        db.session.commit()
    print(f"Added user: {user.user_id}")

def delete_user(user_id):
    user = User.query.filter(User.user_id.__eq__(user_id)).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print("Deleted")
    else:
        print("Người này không tồn tại!")

def add_course(course_id, name_course, start_time, end_time, teacher_id):
    start_time = datetime.strptime(start_time, '%d-%m-%Y %H:%M')
    end_time = datetime.strptime(end_time, '%d-%m-%Y %H:%M')
    course = Courses(
        course_id=course_id,
        name_course=name_course,
        start_time=start_time,
        end_time=end_time,
        teacher_id=teacher_id
    )
    db.session.add(course)
    db.session.commit()
    print(f"Added course: {course.name_course} of {teacher_id}")

def get_all_courses():
    course = db.session.query(
        Courses.course_id,
        Courses.name_course,
        Courses.start_time,
        Courses.end_time,
        Courses.teacher_id
    )

    return course.all()

def get_avatar_from_db_by_user_id(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    return user.avatar

def get_all_attendance():
    attendance = db.session.query(
        Attendance.id,
        Attendance.attendance_time,
        Attendance.student_id,
        Attendance.status
    )
    return attendance.all()

def add_user_to_course(student_id, course_id):
    student_course = Course_Students(
        course_id=course_id,
        student_id=student_id
    )
    db.session.add(student_course)
    db.session.commit()
    print(f"Added {student_id} to {course_id}")

def get_all_student_by_course_id(course_id: str):
    students = db.session.query(
        User.user_id, User.name, User.email
    ).join(Course_Students, User.user_id == Course_Students.student_id).filter(Course_Students.course_id == course_id)
    return students.all()

def get_all_course_by_user(user_id):
    courses = db.session.query(
        Courses.course_id, Courses.name_course, Courses.start_time, Courses.end_time, User.name
    ).join(Course_Students, Courses.course_id == Course_Students.course_id) \
    .join(User, Courses.teacher_id == User.user_id) \
    .filter(Course_Students.student_id == user_id)
    return courses.all()

def check_login(email, password, role=UserRole.STUDENT):
    if email and password:
        return User.query.filter(User.email.__eq__(email),
                                 User.password_hash.__eq__(password),
                                 User.role.__eq__(role)).first()

def check_admin_login(email, password):
    if email and password:
        return User.query.filter(User.email.__eq__(email),
                                 User.password_hash.__eq__(password),
                                 User.role != UserRole.STUDENT).first()

def check_in(image: np.ndarray, course_id: str):
    """
    Điểm danh và lưu vào DB
    Parameters:
        image: Hình ảnh được tải lên từ camera
        course_id: ID lớp học muốn điêm danh

    Returns:
        dict: trả ra kết quả sau khi thực hiện điểm danh
    """
    attendance_results = {
        "success": False,
        "recognized_students": [],
        "unrecognized_faces": 0,
        "message": ""
    }

    client = chromadb.PersistentClient('./face_embedding_db')
    collection = client.get_or_create_collection(name='user_embeddings')
    facenet = FaceNet()
    faces = facenet.face_detection(image)

    if not faces:
        attendance_results["message"] = "Không phát hiện được khuôn mặt nào trong ảnh này."
        return attendance_results

    course = Courses.query.filter_by(course_id=course_id).first()
    if not course:
        attendance_results["message"] = f"Không thể tìm thấy lớp học {course_id}."
        return attendance_results

    unrecognized = 0
    current_time = datetime.now()
    allowed_check_in_time = course.start_time + timedelta(minutes=5)

    if current_time < course.start_time:
        attendance_results["message"] = "Lớp học chưa bắt đầu. Không thể điểm danh lúc này."
        return attendance_results
    elif current_time > allowed_check_in_time:
        attendance_results["message"] = "Đã quá thời gian điểm danh cho lớp học này (5 phút sau khi bắt đầu)."
        return attendance_results

    x, y, w, h = faces["bounding_box"]
    face_img = image[y:h, x:w]
    face_embedding = facenet.face_embedding(face_img).tolist()

    results = collection.query(
        query_embeddings=[face_embedding],
        n_results=1
    )

    if results["distances"][0][0] < 0.5:
        user_id = results["metadatas"][0][0]["user_id"]

        student = User.query.filter_by(user_id=user_id).first()

        if student and student.role == UserRole.STUDENT:
            enrollment = Course_Students.query.filter_by(
                course_id=course.course_id,
                student_id=student.user_id
            ).first()

            if enrollment:
                today_start = datetime.combine(current_time.date(), datetime.min.time())
                today_end = datetime.combine(current_time.date(), datetime.max.time())

                existing_attendance = Attendance.query.filter(
                    Attendance.student_id == user_id,
                    Attendance.course_id == course_id,
                    Attendance.attendance_time.between(today_start, today_end)
                ).first()

                if not existing_attendance:
                    attendance = Attendance(
                        student_id=user_id,
                        course_id=course_id,
                        status=Status.PRESENT,
                        attendance_time=current_time
                    )
                    db.session.add(attendance)
                    db.session.commit()

                    attendance_results["recognized_students"].append({
                        "student_id": user_id,
                        "name": student.name,
                        "status": "Present"
                    })
                else:
                    attendance_results["message"] = f"Sinh viên {student.name} đã điểm danh hôm nay."
            else:
                attendance_results["message"] = f"Sinh viên {student.name} không tồn tại trong lớp học này."
        else:
            unrecognized += 1
    else:
        unrecognized += 1
    attendance_results["unrecognized_faces"] = unrecognized

    if attendance_results["recognized_students"]:
        attendance_results["success"] = True
        attendance_results["message"] = "Điểm danh thành công."
    elif unrecognized > 0:
        attendance_results["message"] = f"Không có sinh viên này!"

    return attendance_results

def delete_attendance(student_id=None, course_id=None, date=None):
    """
    Xóa các bản ghi điểm danh theo điều kiện.

    Parameters:
        student_id (str): ID sinh viên cần xóa điểm danh (tùy chọn)
        course_id (str): ID lớp học cần xóa điểm danh (tùy chọn)
        date (datetime.date): Ngày điểm danh cần xóa (tùy chọn)

    Returns:
        dict: Thông báo kết quả
    """
    query = Attendance.query

    if student_id:
        query = query.filter(Attendance.student_id == student_id)
    if course_id:
        query = query.filter(Attendance.course_id == course_id)
    if date:
        date_start = datetime.combine(date, datetime.min.time())
        date_end = datetime.combine(date, datetime.max.time())
        query = query.filter(Attendance.attendance_time.between(date_start, date_end))

    deleted_count = query.delete(synchronize_session=False)
    db.session.commit()

    return {
        "success": True,
        "deleted": deleted_count,
        "message": f"Đã xóa {deleted_count} bản ghi điểm danh."
    }
