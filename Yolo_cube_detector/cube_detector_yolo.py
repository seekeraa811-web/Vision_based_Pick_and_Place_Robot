import cv2
import time
from ultralytics import YOLO

MODELS = {
    "1": ("YOLOv8", "Yolo_cube_detector/runs/detect/train/weights/best.pt"),
    "2": ("YOLO11", "Yolo_cube_detector/runs/yolo11_cubes/weights/best.pt"),
    "3": ("YOLO26", "Yolo_cube_detector/runs/yolo26_cubes/weights/best.pt"),
}

current_key = "1"
model_name, model_path = MODELS[current_key]
model = YOLO(model_path)

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

prev_time = time.time()

print("Controls:")
print("1 = YOLOv8")
print("2 = YOLO11")
print("3 = YOLO26")
print("q = quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera frame failed.")
        break

    results = model.predict(
        frame,
        imgsz=640,
        conf=0.25,
        device=0,
        verbose=False
    )

    annotated = results[0].plot()

    now = time.time()
    fps = 1 / (now - prev_time)
    prev_time = now

    cv2.putText(annotated, f"Model: {model_name}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.putText(annotated, f"FPS: {fps:.1f}", (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("YOLO Model Compare - Creative F200", annotated)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    pressed = chr(key) if key != 255 else None

    if pressed in MODELS and pressed != current_key:
        current_key = pressed
        model_name, model_path = MODELS[current_key]
        print(f"Switching to {model_name}: {model_path}")
        model = YOLO(model_path)
        prev_time = time.time()

cap.release()
cv2.destroyAllWindows()