import cv2
from src.services import check_in
from src import app
import os

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
course_id = str(input("Nhập mã lớp: "))

while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("img.jpg", frame)
        print("Captured")
        break

cap.release()
cv2.destroyAllWindows()

img = cv2.imread("img.jpg")
with app.app_context():
    checked = check_in(img, course_id)
os.remove('img.jpg')
print(checked["message"])
