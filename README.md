# waste-classification-api

Dibuat oleh kelompok senior project B3 17:

1. Brandon Rafael Lovelyno – 22/500359/TK/54847
2. Muhammad Budi Setiawan – 22/505064/TK/55254
3. Yodha Raya Nayaala – 22/498215/TK/54641

---

## API ini menyediakan layanan deteksi dan klasifikasi jenis sampah menggunakan berbagai model machine learning dan deep learning, termasuk YOLO, EfficientNet, dan klasifikasi warna tempat sampah. Sistem ini ditujukan untuk aplikasi pengelolaan sampah yang cerdas dan otomatis.

## Base URL

```bash
GET /
```

Response:

```json
{
  "Status": "Active",
  "Message": "Welcome to the Waste Detection API"
}
```

## Endpoints

1. Waste Classification with EfficientNet
   `POST /waste-classification/efficientnet`
   Mengklasifikasikan jenis sampah menjadi organik, anorganik, atau b3 menggunakan model EfficientNet.
   Request: file gambar
   Response:

```json
{
  "prediction": "organik",
  "confidence": 0.8725
}
```

2. Trash Bin Detection
   `POST /detect-bin`
   Mendeteksi lokasi tempat sampah di gambar dan mengklasifikasikan jenisnya berdasarkan warna dominan.
   Request: file gambar
   Response:

```json
{
  "detections": [
    {
      "category": "Organik (Hijau)",
      "confidence": 0.91
    }
  ]
}
```

## Instalasi

1. Menjalankan menggunakan uvicorn

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

2. Metode Docker

```bash
sudo docker build -t waste-classification-api .
sudo docker run -p 8001:8001 waste-classification-api
```
