import cv2
from src.utils import load_image_from_url

if __name__ == "__main__":
    image_url = "https://github.com/NHD04072004/Diem-danh-bang-khuon-mat/blob/main/data/images/dang.jpg?raw=true"
    try:
        img = load_image_from_url(image_url)
        print(img)

        # Hiển thị ảnh bằng OpenCV
        cv2.imshow("Ảnh từ URL", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Lưu ảnh nếu muốn
        # cv2.imwrite("downloaded_image.jpg", img)
        # print("Đã tải và lưu ảnh thành công!")
    except Exception as e:
        print(f"Lỗi: {e}")