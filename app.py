"""
AnkiDex - Main Flask Application
Generate Anki flashcards from PDF and text using AI
"""

import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile

from pdf_extractor import extract_text_from_bytes
from flashcard_generator import generate_flashcards
from anki_builder import export_to_apkg

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """Generate flashcards from PDF or text input."""
    try:
        # Get parameters
        deck_name = request.form.get('deck_name', 'AnkiDex Deck')
        num_cards = int(request.form.get('num_cards', 10))
        api_key = request.form.get('api_key', '')
        
        text_content = ""
        
        # Check for PDF file
        if 'pdf_file' in request.files:
            file = request.files['pdf_file']
            if file and file.filename and allowed_file(file.filename):
                pdf_bytes = file.read()
                text_content = extract_text_from_bytes(pdf_bytes)
        
        # Check for text input (use if no PDF or append to PDF text)
        text_input = request.form.get('text_input', '').strip()
        if text_input:
            if text_content:
                text_content += "\n\n" + text_input
            else:
                text_content = text_input
        
        if not text_content:
            return jsonify({'error': 'Please provide a PDF file or text input'}), 400
        
        # Generate flashcards using AI
        flashcards = generate_flashcards(text_content, num_cards, api_key)
        
        if not flashcards:
            return jsonify({'error': 'Failed to generate flashcards from the content'}), 500
        
        # Create temporary .apkg file
        with tempfile.NamedTemporaryFile(suffix='.apkg', delete=False) as tmp:
            tmp_path = tmp.name
        
        export_to_apkg(flashcards, tmp_path, deck_name)
        
        # Return flashcards preview and file path
        return jsonify({
            'success': True,
            'flashcards': flashcards,
            'file_path': tmp_path,
            'deck_name': deck_name
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download')
def download():
    """Download the generated .apkg file."""
    file_path = request.args.get('file_path')
    deck_name = request.args.get('deck_name', 'AnkiDex_Deck')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    # Sanitize deck name for filename
    safe_name = "".join(c for c in deck_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f"{safe_name}.apkg"
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype='application/octet-stream'
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
