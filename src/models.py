from sqlalchemy import Column, Integer, Enum, String, DateTime, Text, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from src import db, app
from enum import Enum as PyEnum
from flask_login import UserMixin
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class UserRole(PyEnum):
    ADMIN = 1
    STUDENT = 2
    TEACHER = 3

class Status(PyEnum):
    PRESENT = 1
    ABSENT = 2

class User(BaseModel, UserMixin):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    user_id = Column(String(20), unique=True, nullable=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    avatar = Column(Text, default="https://st.quantrimang.com/photos/image/2017/04/08/anh-dai-dien-FB-200.jpg")
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    courses = relationship('Courses', backref='teacher', lazy=True)
    attendance = relationship('Attendance', backref='student', lazy=True)
    course_students = relationship('Course_Students', backref='student', lazy=True)

    def __str__(self):
        return self.name

class Courses(BaseModel):
    __tablename__ = 'courses'

    course_id = Column(String(50), nullable=False, unique=True)
    name_course = Column(String(100), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    teacher_id = Column(String(20), ForeignKey('user.user_id'), nullable=False)
    created_at = Column(DateTime, nullable=True, default=datetime.now())

    attendance = relationship('Attendance', backref='course', lazy=True)
    course_students = relationship('Course_Students', backref='course', lazy=True)

    def __str__(self):
        return self.name_course

class Attendance(BaseModel):
    __tablename__ = 'attendance'

    student_id = Column(String(20), ForeignKey('user.user_id'), nullable=False)
    status = Column(Enum(Status), nullable=True)
    attendance_time = Column(DateTime, nullable=True, default=datetime.now())
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)

    __table_args__ = (
        Index('attendance_time_index', 'attendance_time'),
        UniqueConstraint('student_id', 'attendance_time', 'course_id', name='unique_student_attendance'),
    )

    def __str__(self):
        return self.status

class Course_Students(BaseModel):
    __tablename__ = 'course_students'

    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return f"Course id: {self.course_id} - Student id {self.student_id}"

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        print("drop done")
        db.create_all()
    #
    #     admin = User(
    #         user_id = "ADMIN001",
    #         name = "Nguyễn Hải Đăng",
    #         email = "nguyenhaidang04072004@gmail.com",
    #         password_hash = "password",
    #         avatar = "../data/images/dang.jpg",
    #         role = UserRole.ADMIN
    #     )
    #     student1 = User(
    #         user_id="SV001",
    #         name="Nguyễn Văn A",
    #         email="nguyenvana@gmail.com",
    #         password_hash="password",
    #         role=UserRole.STUDENT
    #     )
    #     student2 = User(
    #         user_id="SV002",
    #         name="Nguyễn Văn B",
    #         email="nguyenvanb@gmail.com",
    #         password_hash="password",
    #         role=UserRole.STUDENT
    #     )
    #     student3 = User(
    #         user_id="SV003",
    #         name="Nguyễn Văn C",
    #         email="nguyenvanc@gmail.com",
    #         password_hash="password",
    #         role=UserRole.STUDENT
    #     )
    #     teacher1 = User(
    #         user_id="GV001",
    #         name="Nguyễn Thị A",
    #         email="nguyenthia@gmail.com",
    #         password_hash="password",
    #         role=UserRole.TEACHER
    #     )
    #     teacher2 = User(
    #         user_id="GV002",
    #         name="Nguyễn Thị B",
    #         email="nguyenthib@gmail.com",
    #         password_hash="password",
    #         role=UserRole.TEACHER
    #     )
    #     student4 = User(
    #         user_id="SV004",
    #         name="Nguyễn Văn D",
    #         email="nguyenvand@gmail.com",
    #         password_hash="password",
    #         role=UserRole.STUDENT
    #     )
    #     db.session.add_all([admin, student1, student2, student3, student4, teacher1, teacher2])
    #     db.session.commit()
    #
    #     course1 = Courses(
    #         course_id="TRR0012024",
    #         name_course = "Toán rời rạc",
    #         start_time = datetime.strptime("14-08-2024 7:30", '%d-%m-%Y %H:%M'),
    #         end_time = datetime.strptime("14-08-2024 10:30", '%d-%m-%Y %H:%M'),
    #         teacher_id = teacher1.id,
    #         created_at = datetime.strptime("14-08-2024", '%d-%m-%Y').date()
    #     )
    #     course2 = Courses(
    #         course_id="CTDLAGT0012024",
    #         name_course = "Cấu trúc dữ liệu và giải thuật",
    #         start_time = datetime.strptime("15-08-2024 7:30", '%d-%m-%Y %H:%M'),
    #         end_time = datetime.strptime("15-08-2024 10:30", '%d-%m-%Y %H:%M'),
    #         teacher_id = teacher1.id,
    #         created_at = datetime.strptime("15-08-2024", '%d-%m-%Y').date()
    #     )
    #     course3 = Courses(
    #         course_id="CSDL0012024",
    #         name_course="Cơ sở dữ liệu",
    #         start_time=datetime.strptime("16-08-2024 7:30", '%d-%m-%Y %H:%M'),
    #         end_time=datetime.strptime("16-08-2024 10:30", '%d-%m-%Y %H:%M'),
    #         teacher_id=teacher2.id,
    #         created_at=datetime.strptime("16-08-2024", '%d-%m-%Y').date()
    #     )
    #     db.session.add_all([course1, course2, course3])
    #     db.session.commit()
    #
    # print("Xong rồi!")