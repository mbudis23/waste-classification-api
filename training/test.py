from ultralytics import YOLO
import cv2
import os

image_path = '/home/budi-setiawan/Downloads/TSK-304-1000px-b40ff2a3.jpg'
output_dir = 'cropped_objects'       
model_path = 'models/weight/bindetection-yolov8n.pt'            

os.makedirs(output_dir, exist_ok=True)
image = cv2.imread(image_path)
img_height, img_width = image.shape[:2]

model = YOLO(model_path)

results = model(image_path)[0]

for idx, box in enumerate(results.boxes.xyxy):
    x1, y1, x2, y2 = map(int, box)
    cropped = image[y1:y2, x1:x2]

    class_id = int(results.boxes.cls[idx])
    filename = f'class{class_id}_obj{idx}.jpg'
    output_path = os.path.join(output_dir, filename)
    cv2.imwrite(output_path, cropped)
    print(f"Saved: {output_path}")
