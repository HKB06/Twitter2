from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Charger le modèle entraîné
model = tf.keras.models.load_model("emotion_recognition_model.h5")

emotions = ['joie', 'tristesse', 'colère', 'surprise', 'dégoût', 'peur', 'neutre']

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Lire l'image et la prétraiter
    image = Image.open(io.BytesIO(await file.read())).convert('L').resize((48, 48))
    img_array = np.array(image) / 255.0
    img_array = img_array.reshape(1, 48, 48, 1)

    # Faire une prédiction avec le modèle
    prediction = model.predict(img_array)
    emotion_detectee = emotions[np.argmax(prediction)]

    return {"emotion": emotion_detectee}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
