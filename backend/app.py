from flask import Flask, request, jsonify
from emo_model import analyze_emotion
import os
import requests
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

app = Flask(__name__)

# Mock function to simulate ML model for face analysis


def analyze_face(image):
    # Your face analysis code here
    # This is a mock function, replace it with your actual ML model
    return {"emotion": "happy", "age": 25}

# Endpoint to receive image and send results to /prompt


@app.route('/')
def test_route():
    return "Hello, World!"


@app.route('/messages/face', methods=['POST'])
def analyze_image():
    # Assuming the image is sent as a file
    image_file = request.files['image']

    # Save the image temporarily
    image_path = 'temp_image.jpg'
    image_file.save(image_path)

    # Analyze face
    results = analyze_emotion(image_path)

    # Remove the temporary image file
    os.remove(image_path)

    # Post results to /prompt endpoint
    prompt_url = "http://localhost:5000/prompt"
    response = requests.post(prompt_url, json=results)

    return response.text, response.status_code

    # return results

# Endpoint to receive text message and generate prompt


@app.route('/prompt', methods=['POST'])
def generate_prompt():
    # Assuming the text message is sent as JSON

    analysis_result = request.json  # this will be coming from ml model analysis
    data_input = "I have been feeling very low lately, my cat passed away, he was my best friend for the last 10 years.He was the best thing that ever happened to me. I wanna kill myself"

    # Your prompt generation logic here
    # This is just a placeholder
    prompt = f"Your face analysis shows {analysis_result} emotion. Your message: {data_input}, based on this give me an appropriate response"

    # Send prompt to Mistral (replace this with your actual implementation)

    api_key = "T0krPQPq0lNykTpOJIjF3BdEjA4srEB7"
    model = "mistral-tiny"

    client = MistralClient(api_key=api_key)

    messages = [
        ChatMessage(role="user", content=prompt)
    ]

    # No streaming
    chat_response = client.chat(
        model=model,
        messages=messages,
    )

    # print(chat_response.choices[0].message.content)
    mistral_response = chat_response.choices[0].message.content

    return jsonify({"prompt": prompt, "mistral_response": mistral_response})


if __name__ == '__main__':
    app.run(debug=True)
