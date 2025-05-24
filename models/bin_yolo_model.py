from ultralytics import YOLO
import numpy as np
from sklearn.cluster import KMeans
import cv2

model = YOLO("models/weight/bindetection-yolov8n.pt")

def get_dominant_color(image_crop: np.ndarray, k: int = 3):
    if image_crop.size == 0:
        return np.array([0, 0, 0])
    
    hsv_img = cv2.cvtColor(image_crop, cv2.COLOR_RGB2HSV)
    pixels = hsv_img.reshape((-1, 3))
    mask = (pixels[:, 2] > 30) & (pixels[:, 2] < 220)
    filtered_pixels = pixels[mask]
    
    if len(filtered_pixels) == 0:
        filtered_pixels = pixels 
    
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(filtered_pixels)
    
    counts = np.bincount(kmeans.labels_)
    dominant_hsv = kmeans.cluster_centers_[np.argmax(counts)]
    
    dominant_rgb = cv2.cvtColor(np.uint8([[dominant_hsv]]), cv2.COLOR_HSV2RGB)[0][0]
    return dominant_rgb.astype(int)

def classify_color(color_rgb):
    hsv_color = cv2.cvtColor(np.uint8([[color_rgb]]), cv2.COLOR_RGB2HSV)[0][0]
    h, s, v = hsv_color

    if 35 <= h <= 85 and s > 50:
        return "Organik (Hijau)"
    elif (h < 10 or h > 170) and s > 50:
        return "B3 (Merah)"
    elif 20 <= h <= 30 and s > 50:
        return "Anorganik (Kuning)"
    elif v < 30:
        return "Tidak Dikenali (Gelap)"
    elif s < 30:
        return "Tidak Dikenali (Abu-abu)"
    return "Tempat Sampah Lain"

def crop_image_by_box(image_np: np.ndarray, box_coords):
    x1, y1, x2, y2 = map(int, box_coords)
    height, width = image_np.shape[:2]
    
    pad_x = int(0.05 * (x2 - x1))
    pad_y = int(0.05 * (y2 - y1))
    
    x1 = max(0, x1 - pad_x)
    y1 = max(0, y1 - pad_y)
    x2 = min(width, x2 + pad_x)
    y2 = min(height, y2 + pad_y)
    
    return image_np[y1:y2, x1:x2]

def detect_and_classify_bin(image_np: np.ndarray):
    if image_np.shape[2] == 4:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
    elif len(image_np.shape) == 2: 
        image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
    
    results = model.predict(image_np)[0]
    detections = []

    for box in results.boxes:
        cropped = crop_image_by_box(image_np, box.xyxy[0])
        if cropped.size == 0:
            continue
            
        color = get_dominant_color(cropped)
        label = classify_color(color)
        
        detections.append({
            # "bbox": list(map(int, box.xyxy[0])),
            # "dominant_rgb": color.tolist(),
            "category": label,
            "confidence": float(box.conf[0])  # Add confidence score
        })

    return detections