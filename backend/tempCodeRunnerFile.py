@app.route('/messages/face', methods=['POST'])
def analyze_image():
    # Assuming the image is sent as a file
    image_file = request.form['image']
    text_input = request.form['text_input']

    base64_to_jpg(image_file, 'temp_image.jpg')
    # Save the image temporarily
    image_path = 'temp_image.jpg'
    # image_file.save(image_path)

    # Analyze face
    results = analyze_emotion(image_path)

    send_results = {
        'emotion': results,
        'text_input': text_input
    }

    # Remove the temporary image file
    os.remove(image_path)

    # Post results to /prompt endpoint
    prompt_url = "http://172.16.128.173:5000/prompt"
    response = requests.post(prompt_url, json=send_results)

    return response.text, response.status_code