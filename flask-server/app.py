from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def calculate_reading_time(text, words_per_minute=200):
    words = text.split()
    num_words = len(words)
    reading_time = num_words / words_per_minute
    return reading_time

@app.route('/')
def home():
    return "Welcome to the Reading Time Calculator API"

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            app.logger.error('No file part')
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            app.logger.error('No selected file')
            return jsonify({'error': 'No selected file'}), 400
        if file:
            try:
                text = file.read().decode('utf-8')
            except Exception as e:
                app.logger.error(f'Error reading file: {e}')
                return jsonify({'error': f'Error reading file: {e}'}), 500

            app.logger.info(f'File content: {text[:100]}...')  # Log first 100 characters of the file
            reading_time = calculate_reading_time(text)
            app.logger.info(f'Reading time: {reading_time}')
            return jsonify({'reading_time': f'{reading_time:.2f} minutes'})
        app.logger.error('File not allowed')
        return jsonify({'error': 'File not allowed'}), 400
    except Exception as e:
        app.logger.error(f'Error processing file: {e}')
        app.logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal Server Error: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)