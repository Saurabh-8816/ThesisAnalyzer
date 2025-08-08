import requests

# URL of your Flask keyword search endpoint
url = 'http://127.0.0.1:5000/search_keywords'

# Data to send: filename and keywords
data = {
    'filename': 'Thesis.pdf',  # Use the exact filename you uploaded
    'keywords': ['introduction', 'conclusion', 'navigate']  # Replace with your keywords
}

# Send POST request
response = requests.post(url, json=data)

# Print the response from the server
print(response.status_code)
print(response.json())
