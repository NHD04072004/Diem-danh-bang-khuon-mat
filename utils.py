import pandas as pd
from datetime import datetime

def find_match(embedding, db_embeddings, threshold=0.9):
    min_distance = float('inf')
    matched_id = None
    for student_id, db_emb in db_embeddings.items():
        distance = (embedding - db_emb).norm().item()
        if distance < min_distance:
            min_distance = distance
            matched_id = student_id
    if min_distance < threshold:
        return matched_id, min_distance
    else:
        return None, None

def save_to_excel(attendance):
    if attendance:
        df = pd.DataFrame([
            {"id": sid, "name": info["name"], "time": info["time"]}
            for sid, info in attendance.items()
        ])
        df['date'] = datetime.now().strftime("%d-%m-%y")
        df.to_excel("attendance.xlsx", index=False)
        print("Điểm danh thành công!")
    else:
        print("Không điểm danh được, hãy điểm danh lại!")
