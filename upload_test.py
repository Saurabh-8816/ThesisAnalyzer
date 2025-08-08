import requests

# URL of your Flask upload endpoint
url = 'http://127.0.0.1:5000/upload'

# Path to your PDF file
file_path = 'Thesis.pdf'  # Change this to your actual file name

# Open the file in binary mode and send the POST request
with open(file_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, files=files)

# Print the server's response
print(response.status_code)
print(response.json())