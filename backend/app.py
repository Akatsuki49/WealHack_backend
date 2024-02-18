from flask import Flask, request, jsonify
from emo_model import analyze_emotion
import os
import base64
import requests
from mistralai.client import MistralClient
from storage import Storage
from mistralai.models.chat_completion import ChatMessage


app = Flask(__name__)

# Mock function to simulate ML model for face analysis


def analyze_face(image):
    # Your face analysis code here
    # This is a mock function, replace it with your actual ML model
    return {"emotion": "happy", "age": 25}

def base64_to_jpg(base64_string, output_file):
    # Decode base64 string to bytes
    image_bytes = base64.b64decode(base64_string)
    
    # Write bytes to a JPG file
    with open(output_file, "wb") as f:
        f.write(image_bytes)


# Endpoint to receive image and send results to /prompt


@app.route('/')
def test_route():
    return "Hello, World!"


@app.route('/messages/face', methods=['POST'])
def analyze_image():
    # Assuming the image is sent as a file
    image_file = request.form['image']
    text_input = request.form['text_input']

    base64_to_jpg(image_file,'temp_image.jpg')
    # Save the image temporarily
    image_path = 'temp_image.jpg'
    # image_file.save(image_path)

    # Analyze face
    results,age = analyze_emotion(image_path)

    send_results = {
        'emotion': results,
        'age':age,
        'text_input': text_input
    }

    # Remove the temporary image file
    os.remove(image_path)

    # Post results to /prompt endpoint
    prompt_url = "http://localhost:5000/prompt"
    response = requests.post(prompt_url, json=send_results)

    return response.text, response.status_code

    # return results

# Endpoint to receive text message and generate prompt


@app.route('/prompt', methods=['POST'])
def generate_prompt():
    # Assuming the text message is sent as JSON

    data = request.json  # this will be coming from ml model analysis
    # data_input = "I have been feeling very low lately, my cat passed away, he was my best friend for the last 10 years.He was the best thing that ever happened to me. I wanna kill myself"
    analyze_emotion = data['emotion']
    data_input = data['text_input']
    age=data['age']

    # Your prompt generation logic here
    # This is just a placeholder
    # storage.store_user_prompt(data_input)
    with open("prompts.txt","wb") as f:
        f.write(data_input+". ")
    txt1=""
    with open("prompt.txt","rb") as f:
        txt1=f.read()
    prompt = f"Your face analysis shows {analyze_emotion} emotion and you are {age} years. Your message: {txt1} , based on this give me one single appropriate response (no options), make sure to be as comforting in your answer as you can "
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
        max_tokens=120
    )

    # print(chat_response.choices[0].message.content)
    mistral_response = chat_response.choices[0].message.content
    colon_index = mistral_response.find(":")
    backslash_index = mistral_response.find("\\")
    extracted_content = mistral_response[colon_index + 1:backslash_index].strip()
    return jsonify({"prompt": prompt, "mistral_response": extracted_content})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
