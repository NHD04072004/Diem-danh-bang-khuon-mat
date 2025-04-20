from typing import Dict, List
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import cv2
import numpy as np

class FaceNet:
    def __init__(self, pretrained_model: str = 'vggface2'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.mtcnn = MTCNN(image_size=224, thresholds=[0.7, 0.8, 0.8], device=self.device)
        self.resnet = InceptionResnetV1(pretrained=pretrained_model).eval().to(self.device)

    def face_detection(self, image: np.ndarray) -> Dict:
        """
        Phát hiện khuôn mặt từ ảnh đầu vào
        :param: image(np.ndarray): hình ảnh được đọc từ OpenCV
        :return: Dict: Tọa độ khuôn mặt, điểm confidence
        """
        faces = {}
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes, scores = self.mtcnn.detect(img=image_rgb)

        if boxes is not None:
            for box in boxes:
                x, y, w, h = map(int, box)
                faces.update({
                    'bounding_box': (x, y, w, h),
                    'confidence': scores[0]
                })

        return faces

    def face_display(self, img: np.ndarray, face: Dict) -> None:
        """
        Hiển thị khuôn mặt được phát hiện
        :param img: hình ảnh được đọc từ OpenCV.
        :param face: Danh sách các khuôn mặt được phát hiện.
        :return: None
        """
        # orig_h, orig_w = img.shape[:2]
        # new_w, new_h = 640, 480
        #
        # img_resized = cv2.resize(img, (new_w, new_h))
        #
        # scale_x = new_w / orig_w
        # scale_y = new_h / orig_h

        x, y, w, h = face["bounding_box"]
        confidence = face["confidence"]
        #
        # x = int(x * scale_x)
        # y = int(y * scale_y)
        # w = int(w * scale_x)
        # h = int(h * scale_y)

        cv2.rectangle(img, (x, y), (w, h), (0, 255, 0), 2)
        cv2.putText(img, f"{confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                    2)

        cv2.imshow("Detected faces", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def face_embedding(self, face_img: np.ndarray) -> torch.Tensor:
        """
        Embedding hình ảnh khuôn mặt
        :param face_img: Hình ảnh khuôn mặt sau khi được cắt [y:h, x:w]
        :return: torch.Tensor: embedding của khuôn mặt
        """
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        face_tensor = self.mtcnn(face_img)

        if face_tensor is not None:
            face_tensor = face_tensor.unsqueeze(0).to(self.device)
            with torch.no_grad():
                embedding = self.resnet(face_tensor)[0].detach().cpu()

        return embedding
