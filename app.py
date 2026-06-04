from flask import Flask, request, jsonify, render_template
import os
import json
import PyPDF2
import requests
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__, template_folder='thesis-frontend')
CORS(app)

UPLOAD_FOLDER = 'uploads'
TEXT_FOLDER = 'texts'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEXT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_text_path(filename):
    # Save extracted text as JSON per file
    base = os.path.splitext(filename)[0]
    return os.path.join(TEXT_FOLDER, f"{base}.json")


extracted_text = {}

# OpenRouter API config (GPT-4)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = "openai/gpt-4"

@app.route('/')
def home():
    return render_template('index.html')

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
    for page in pdf_reader.pages:
        text = page.extract_text()
        pages_text.append(text if text else "")

    # Save extracted text to a JSON file
    text_path = get_text_path(filename)
    with open(text_path, "w", encoding="utf-8") as f:
        json.dump(pages_text, f)

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

    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    text_path = get_text_path(filename)
    if not os.path.exists(text_path):
        return jsonify({'error': 'File not found or not processed'}), 400
    if not keywords:
        return jsonify({'error': 'No keywords provided'}), 400

    # Load extracted text from file
    with open(text_path, "r", encoding="utf-8") as f:
        pages_text = json.load(f)

    pages_with_keywords = []
    for i, page_text in enumerate(pages_text):
        if any(keyword.lower() in (page_text or "").lower() for keyword in keywords):
            pages_with_keywords.append({
                'page_number': i + 1,
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

    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Read extracted text from JSON file (matches what /upload writes)
    text_path = get_text_path(filename)
    if not os.path.exists(text_path):
        return jsonify({'error': 'File not found or not processed. Upload it first.'}), 400

    with open(text_path, "r", encoding="utf-8") as f:
        pages_text = json.load(f)

    thesis_text = "\n".join(pages_text)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that answers questions about a thesis document."},
            {"role": "user", "content": f"This is a thesis:\n{thesis_text}\n\nQuestion: {question}\nAnswer:"}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        answer = result['choices'][0]['message']['content']
        return jsonify({'answer': answer})
    else:
        return jsonify({'error': response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)