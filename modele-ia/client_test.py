import cv2
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont

API_URL = "http://127.0.0.1:8000/predict"

font_path = "arial.ttf"  
font = ImageFont.truetype(font_path, 32)

# Initialiser la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir l'image en niveaux de gris et la redimensionner
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_frame = cv2.resize(gray_frame, (48, 48))

    _, img_encoded = cv2.imencode('.jpg', resized_frame)
    response = requests.post(API_URL, files={'file': img_encoded.tobytes()})

    emotion = response.json().get('emotion', 'Inconnu')

    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(frame_pil)

    text = f"Émotion : {emotion}"
    draw.text((50, 50), text, font=font, fill=(0, 255, 0))

    frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)

    cv2.imshow("Détection des émotions", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
