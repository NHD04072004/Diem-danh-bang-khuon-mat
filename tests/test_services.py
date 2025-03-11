from src import app
from src.services import *
from src.models import *
import cv2

def test_get_all_user(role):
    list_sinhvien = get_all_user_by_role(role)
    for sinhvien in list_sinhvien:
        print(sinhvien)

def test_add_user():
    add_user("GV001", "Nguyen Van A", "nguyenvana@gmail.com", "1234", role=UserRole.TEACHER)
    add_user("22A1001D0049", "Nguyễn Hải Đăng", "22a1001d0049@hou.edu.vn", 'dang', role='student', avatar='du_lieu_test/z6369860169727_eb3e3a6c973400ff110e785900d05f70.jpg')
    add_user("sv1", "thai", "23a1001d0049@hou.edu.vn", 'dang', role='student', avatar='du_lieu_test/z6370478038827_79df70a4186542485a50e4d4a2fe4522.jpg')

def test_load_avatar_from_db_by_id():
    print(get_avatar_from_db_by_user_id("22A1001D0049"))

def test_add_course():
    add_course(
        course_id='CSDL0012024',
        name_course="Cơ sở dữ liệu",
        start_time="16-08-2024 7:30",
        end_time="16-08-2024 10:30",
        teacher_id="GV001"
    )

def test_get_all_course():
    list_course = get_all_course()
    for course in list_course:
        print(course)

def test_get_all_attendance():
    attendance = get_all_attendance()
    print(attendance)

def test_check_in():
    img = cv2.imread("du_lieu_test/dang.jpg")
    check = check_in(img, "CSDL0012024")
    print(check)

def test_add_student_course():
    add_user_to_course("22A1001D0049", "CSDL0012024")


def test_get_all_student_by_course_id():
    a = get_all_student_by_course_id("CSDL0012024")
    for i in a:
        print(i)

def test_chromadb():
    client = chromadb.PersistentClient("./face_embedding_db")
    collection = client.get_or_create_collection(name="user_embeddings")

    # Lấy tất cả bản ghi trong collection
    all_records = collection.get()

    # Hiển thị kết quả
    print(all_records["embeddings"])
    print(all_records)

if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        # db.create_all()
        # test_get_all_user('teacher')
        # test_get_all_user('student')
        # test_add_user()
        # test_load_avatar_from_db_by_id()
        # test_add_course()
        # test_get_all_course()
        # test_track()
        # test_get_all_attendance()
        test_check_in()
        # test_add_student_course()
        # test_get_all_student_by_course_id()
        # test_chromadb()
        # pass
    # img = cv2.imread("du_lieu_test/z6369860169727_eb3e3a6c973400ff110e785900d05f70.jpg")
    # print(img)