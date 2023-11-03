import cv2

SOURCE = 0

def get_center():
    cam = cv2.VideoCapture(SOURCE)
    ret, image = cam.read()
    height, width, _ = image.shape
    center_x = width // 2
    center_y = height // 2
    print(f"Center coordinates: ({center_x}, {center_y})")
    cam.release()

if __name__ == "__main__":
    get_center()