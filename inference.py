import os
import cv2
import torch
import argparse
from facenet_pytorch import MTCNN, InceptionResnetV1
from src.utils import *

def get_args():
    parser = argparse.ArgumentParser("Face verification")
    parser.add_argument("--data_path", "-p", type=str, default='data')
    parser.add_argument("--image_size", "-i", type=int, default=224)

    return parser.parse_args()

def inference(args):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    mtcnn = MTCNN(image_size=args.image_size, device=device)
    resnet = InceptionResnetV1(pretrained='vggface2').eval()

    df = pd.read_excel(os.path.join(args.data_path, 'class-list.xlsx'))
    student_embeddings = {}
    for i, r in df.iterrows():
        if os.path.exists(r["image_path"]):
            image = cv2.imread(r["image_path"])
            face_tensor = mtcnn(image)
            if face_tensor is not None:
                face_tensor = face_tensor.unsqueeze(0)
                with torch.no_grad():
                    embedding = resnet(face_tensor).detach()
                student_embeddings[r["id"]] = embedding

    cap = cv2.VideoCapture(0)
    attendance = {}

    while True:
        ret, frame = cap.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        boxes, _ = mtcnn.detect(rgb_frame)
        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2 = [int(b) for b in box]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                face_img = rgb_frame[y1:y2, x1:x2]
                face_tensor = mtcnn(face_img)
                if face_tensor is not None:
                    face_tensor = face_tensor.unsqueeze(0)
                    with torch.no_grad():
                        embedding = resnet(face_tensor).detach()
                    matched_id, distance = find_match(embedding, student_embeddings, threshold=0.9)
                    if matched_id is not None:
                        name = df.loc[df['id'] == matched_id, 'name'].values[0]
                        if matched_id not in attendance:
                            attendance[matched_id] = {'name': name, 'time': datetime.now().strftime("%H:%M:%S")}
                        cv2.putText(frame, f"{name}", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.imshow('Điểm danh', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    save_to_excel(attendance)

if __name__ == "__main__":
    opt = get_args()
    inference(opt)