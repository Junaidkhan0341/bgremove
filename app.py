from flask import Flask, request, jsonify, send_file
import io
import subprocess
import tempfile
import os

app = Flask(__name__)

# Configure the path to the background remover tool
BACKGROUND_REMOVER_TOOL = 'backgroundremover'

@app.route('/api/remove_background', methods=['POST'])
def remove_background_from_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Validate the file type (for example, only allow PNG and JPEG)
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({'error': 'Invalid file type. Only PNG and JPEG are allowed.'}), 400
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as input_file:
        input_file.write(file.read())
        input_file_path = input_file.name
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as output_file:
        output_file_path = output_file.name
    
    try:
        result = subprocess.run(
            [BACKGROUND_REMOVER_TOOL, '-i', input_file_path, '-o', output_file_path],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        
        with open(output_file_path, 'rb') as f:
            result_image = f.read()
        
        result_image_io = io.BytesIO(result_image)
        result_image_io.seek(0)
        return send_file(result_image_io, mimetype='image/png', as_attachment=True, download_name='output.png')
    
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Command failed with error: {e.stderr.decode() if e.stderr else "Unknown error"}'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if os.path.exists(input_file_path):
            os.remove(input_file_path)
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
