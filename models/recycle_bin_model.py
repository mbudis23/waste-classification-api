import joblib

# Load model dan labels saat modul dipanggil
model = joblib.load("models/weight/color_classifier_model.pkl")
labels = joblib.load("models/weight/color_labels.pkl")
