import requests

# Define the Mistral API endpoint and your API key
mistral_endpoint = "https://api.eleuther.ai/completion/mistral-cra"
api_key = "T0krPQPq0lNykTpOJIjF3BdEjA4srEB7"
headers = {"Authorization": f"Bearer {api_key}"}

# Define the prompt
prompt = "Once upon a time, in a land far away, "

# Make a POST request to the Mistral API
data = {"prompt": prompt}
response = requests.post(mistral_endpoint, json=data, headers=headers, verify=False)

# Process the response
if response.status_code == 200:
    generated_text = response.json()["text"]
    print(generated_text)
else:
    print("Error:", response.status_code)
