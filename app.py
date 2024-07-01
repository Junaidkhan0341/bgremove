import os
from flask import Flask, request, jsonify, send_file
import io
from backgroundremover.remove_background import remove_background  # Adjust this import as necessary
from waitress import serve
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow requests from any origin

@app.route('/api/remove_background', methods=['POST'])
def remove_background_from_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    image_bytes = file.read()

    try:
        result_image = remove_background(image_bytes)
        result_image_io = io.BytesIO(result_image)
        result_image_io.seek(0)
        return send_file(result_image_io, mimetype='image/png', as_attachment=True, download_name='output.png')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use Waitress to serve the app
    port = int(os.environ.get('PORT', 10000))
    serve(app, host='0.0.0.0', port=port)
