from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import PyPDF2
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


extracted_text = {}

# Set your Gemini API key
GEMINI_API_KEY = os.environ.get("AIzaSyA2LQA-9MFL8cxhZeYmFuFaggS46Wgw9gY")  

@app.route('/')
def home():
    return "Thesis Analyzer Backend Running!"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Extract text from each page
    pdf_reader = PyPDF2.PdfReader(file_path)
    pages_text = []
    for page_num, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        pages_text.append(text if text else "")

    # Store in memory (keyed by filename)
    extracted_text[filename] = pages_text

    return jsonify({
        'message': 'File uploaded and text extracted successfully',
        'file_path': file_path,
        'num_pages': len(pages_text)
    })

@app.route('/upload', methods=['GET'])
def upload_form():
    return '''
    <form method="post" enctype="multipart/form-data" action="/upload">
      <input type="file" name="file">
      <input type="submit">
    </form>
    '''

@app.route('/search_keywords', methods=['POST'])
def search_keywords():
    data = request.get_json()
    filename = data.get('filename')
    keywords = data.get('keywords', [])

    if not filename or filename not in extracted_text:
        return jsonify({'error': 'File not found or not processed'}), 400
    if not keywords:
        return jsonify({'error': 'No keywords provided'}), 400

    pages_with_keywords = []
    for i, page_text in enumerate(extracted_text[filename]):
        if any(keyword.lower() in (page_text or "").lower() for keyword in keywords):
            pages_with_keywords.append({
                'page_number': i + 1,  # 1-based index for user-friendliness
                'text': page_text
            })

    return jsonify({
        'filename': filename,
        'keywords': keywords,
        'matched_pages': pages_with_keywords
    })

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    filename = data.get('filename')
    question = data.get('question')

    if not filename or filename not in extracted_text:
        return jsonify({'error': 'File not found or not processed'}), 400
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    thesis_text = "\n".join(extracted_text[filename])
    prompt = f"This is a thesis:\n{thesis_text}\n\nQuestion: {question}\nAnswer:"

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        answer = result['candidates'][0]['content']['parts'][0]['text']
        return jsonify({'answer': answer})
    else:
        return jsonify({'error': response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)