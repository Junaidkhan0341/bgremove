from flask import Flask, request, jsonify, send_file
import io
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/api/remove_background', methods=['POST'])
def remove_background_from_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Create a temporary file for the uploaded image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as input_file:
        input_file.write(file.read())
        input_file_path = input_file.name
    
    # Create a temporary file for the output image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as output_file:
        output_file_path = output_file.name
    
    # Run the backgroundremover CLI command
    try:
        result = subprocess.run(['backgroundremover', '--input', input_file_path, '--output', output_file_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Read the resulting image file
        with open(output_file_path, 'rb') as f:
            result_image = f.read()
        
        # Return the resulting image
        result_image_io = io.BytesIO(result_image)
        result_image_io.seek(0)
        return send_file(result_image_io, mimetype='image/png', as_attachment=True, download_name='output.png')
    
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Command failed with error: {e.stderr.decode() if e.stderr else "Unknown error"}'}), 500
    
    finally:
        # Clean up temporary files
        os.remove(input_file_path)
        os.remove(output_file_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
