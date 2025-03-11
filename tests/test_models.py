from src.routes import app, db
from sqlalchemy.exc import IntegrityError

def user_test():
    user = User(
        user_id="SV001",
        name="Nguyen Van A",
        email="nva@example.com",
        password_hash="hashed_password",
        role=UserRole.STUDENT
    )
    db.session.add(user)
    db.session.commit()
    queried_user = User.query.filter_by(user_id="SV001").first()
    print(queried_user.name, "-", "Nguyen Van A")
    print(queried_user.role, "-", UserRole.STUDENT)
    print(str(queried_user), "-", "Nguyen Van A")
    print(queried_user.user_id)
    print(queried_user.id)

def courses_test():
    teacher = User(
        user_id="GV001",
        name="Tran Thi B",
        email="ttb@example.com",
        password_hash="hashed_password",
        role=UserRole.TEACHER
    )
    db.session.add(teacher)
    db.session.commit()

    course = Courses(
        name_course="Python 101",
        start_time=datetime(2025, 3, 1, 9, 0),
        end_time=datetime(2025, 3, 1, 11, 0),
        teacher_id=teacher.id
    )
    db.session.add(course)
    db.session.commit()

    queried_course = Courses.query.filter_by(name_course="Python 101").first()
    print(queried_course.teacher.user_id)
    print(queried_course)
    print(queried_course.start_time)
    print(queried_course.end_time)
    print(queried_course.teacher.id)

def attendance_test():
    student = User(user_id="SV002", name="Le Van C", email="lvc@example.com",
                   password_hash="hashed_password", role=UserRole.STUDENT)
    teacher = User(user_id="GV002", name="Pham Thi D", email="ptd@example.com",
                   password_hash="hashed_password", role=UserRole.TEACHER)
    db.session.add_all([student, teacher])
    db.session.commit()

    course = Courses(name_course="AI Basics", start_time=datetime(2025, 3, 2, 14, 0),
                     end_time=datetime(2025, 3, 2, 16, 0), teacher_id=teacher.id)
    db.session.add(course)
    db.session.commit()

    attendance = Attendance(student_id=student.id, course_id=course.id, status=Status.PRESENT)
    db.session.add(attendance)
    db.session.commit()

    queried_attendance = Attendance.query.filter_by(student_id=student.id).first()
    print(queried_attendance.course.name_course)
    print(queried_attendance.attendance_time)
    print(queried_attendance.student.role)
    print(queried_attendance.student.id)
    print(queried_attendance.course.teacher.id)

def unique_attendance_test():
    student = User(user_id="SV004", name="Tran Van G", email="tvg@example.com",
                   password_hash="hashed_password", role=UserRole.STUDENT)
    course = Courses(name_course="Math", start_time=datetime(2025, 3, 4, 8, 0),
                     end_time=datetime(2025, 3, 4, 10, 0), teacher_id=1)
    db.session.add_all([student, course])
    db.session.commit()

    attendance1 = Attendance(student_id=student.id, course_id=course.id, status=Status.PRESENT)
    db.session.add(attendance1)
    db.session.commit()
    print(f"Thêm attendance1 thành công: {attendance1}")

    attendance2 = Attendance(student_id=student.id, course_id=course.id, status=Status.ABSENT)
    db.session.add(attendance2)
    try:
        db.session.commit()
        print("Lỗi: Đã thêm được attendance2, ràng buộc unique không hoạt động!")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Đã bắt được lỗi IntegrityError: {e}")
        print("Test thành công: Ràng buộc unique hoạt động đúng!")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # user_test()
        # courses_test()
        # attendance_test()
        # unique_attendance_test()
        db.session.remove()
        db.drop_all()
        print("drop done")