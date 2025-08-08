import requests

url = 'http://127.0.0.1:5000/ask'
data = {
    'filename': 'Thesis.pdf',  # Use the filename you uploaded
    'question': 'What is the summary of this thesis?'  # Replace with your question
}
response = requests.post(url, json=data)
print(response.status_code)
print(response.text)  # <-- Print raw response for debugging
