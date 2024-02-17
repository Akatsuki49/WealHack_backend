# emotion_analysis_model.py
import pickle
from facerecog import analysis1
import requests


def analyze_emotion(image_path):
    # Implement emotion analysis logic here
    # This could involve using computer vision or machine learning techniques
    # For now, returning a placeholder emotion
    with open("facerecog1.pkl", "rb") as f:
        analysis_function = pickle.load(f)
    # img_path="./assets/download.jpg"
    result = analysis_function(image_path)
    print(result)

    return result

# analyze_emotion()
