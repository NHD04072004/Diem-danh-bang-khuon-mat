import numpy as np
import requests
import cv2

def load_image_from_url(url: str) -> np.ndarray:
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Không tải được ảnh từ URL: {url}")

    image_array = np.frombuffer(response.content, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Không thể decode ảnh từ dữ liệu tải về!")

    return image