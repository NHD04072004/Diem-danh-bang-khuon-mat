from typing import Tuple
import numpy as np
from src.models import *
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

# def create_embedding_for_user(avatar_img: np.ndarray):
#     facenet = FaceNet()
#     face = facenet.face_detection(avatar_img)
#     x, y, w, h = face["bounding_box"]
#     face_img = avatar_img[y:h, x:w]
#     embedding = facenet.face_embedding(face_img)
#

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
        img = load_image_from_url(avatar)
        facenet = FaceNet()
        face = facenet.face_detection(img)
        x, y, w, h = face["bounding_box"]
        face_img = img[y:h, x:w]
        avatar_embedding = facenet.face_embedding(face_img)
        avatar_embedding = avatar_embedding.tolist()
        collection.upsert(
            ids=[user_id],
            embeddings=[avatar_embedding],
            metadatas=[{"user_id": user_id}]
        )
        print("Has avatar")
    else:
        print("Has not avatar")
        db.session.commit()
    print(f"Added user: {user.user_id}")

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

def get_all_course():
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

def track(course_id: str, image: np.ndarray) -> Tuple[bool, str]:
    """
    Điểm danh bàng khuôn mặt rồi lưu vào bảng attendance
    :param course_id (str): ID của lớp học đó
    :param image (np.ndarray): Ảnh đầu vào từ camera
    :return: Tuple[bool, str]: Điểm danh thành công hay không, thông báo
    """
    facenet = FaceNet()
    client = chromadb.PersistentClient('./face_embedding_db')
    collection = client.get_or_create_collection(name='user_embeddings')

    face_detection = facenet.face_detection(image)
    confidence = face_detection['confidence']
    if confidence < 0.8:
        return False, f"Độ tin cậy thấp ({confidence:.2f})!"
    x, y, w, h = face_detection["bounding_box"]
    face_img = image[y:h, x:w]
    embedding = facenet.face_embedding(face_img)

    results = collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=1
    )
    if results["distances"][0][0] < 0.5:
        user_id = results['metadatas'][0][0]['user_id']
        user = db.session.query(User).filter_by(user_id=user_id).first()
        if user:
            today = datetime.now().date()
            existing = db.session.query(Attendance).filter(
                Attendance.student_id == user.id,
                Attendance.course_id == course_id,
                db.func.date(Attendance.attendance_time) == today
            ).first()
            if existing:
                return False, f"Sinh viên {user_id} đã điểm danh hôm nay!"
            attendance = Attendance(
                student_id=user.user_id,
                course_id=course_id,
                status=Status.PRESENT,
                attendance_time=datetime.now()
            )
            db.session.add(attendance)
            db.session.commit()
            return True, f"Điểm danh thành công cho {user_id}!"
    return False, "Không nhận diện được sinh viên!"