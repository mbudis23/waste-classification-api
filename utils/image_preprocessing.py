from PIL import Image
import numpy as np
import io

def preprocess_image(image_bytes, img_size=128):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((img_size, img_size))
    image_array = np.array(image).reshape(1, -1) / 255.0
    return image_array
