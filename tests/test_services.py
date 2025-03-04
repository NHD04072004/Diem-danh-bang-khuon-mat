from src import app
from src.services import *
from src.models import *
import cv2

def test_get_all_user(role):
    list_sinhvien = get_all_user_by_role(role)
    for sinhvien in list_sinhvien:
        print(sinhvien)

def test_add_user():
    # add_user("GV001", "Nguyen Van A", "nguyenvana@gmail.com", "1234", role=UserRole.TEACHER)
    add_user("22A1001D0049", "Nguyễn Hải Đăng", "22a1001d0049@hou.edu.vn", 'dang', role='student', avatar='https://github.com/NHD04072004/Diem-danh-bang-khuon-mat/blob/main/data/images/dang.jpg?raw=true')

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

def test_track():
    img = cv2.imread('../data/images/z6370478038827_79df70a4186542485a50e4d4a2fe4522.jpg')
    track(img)

if __name__ == "__main__":
    with app.app_context():
        # test_get_all_user('student')
        # test_add_user()
        # test_load_avatar_from_db_by_id()
        # test_add_course()
        # test_get_all_course()
        test_track()