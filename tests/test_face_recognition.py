from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import cv2
from src.face_recognizer import FaceNet

def test_face_detection(faces):
    img = cv2.imread('../data/images/dang.jpg')
    face_detections = faces.face_detection(img)
    print(face_detections)
    x, y, w, h = face_detections['bounding_box']
    img_cropped = img[y:h, x:w]
    # cv2.imshow("frame", img_cropped)
    # cv2.waitKey(0)
    # faces.face_display(img, face_detections)

    embedding = faces.face_embedding(img_cropped)
    print(embedding)

if __name__ == "__main__":
    faces = FaceNet()
    test_face_detection(faces)