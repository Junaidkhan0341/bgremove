import os
import subprocess
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the upload directory and allowed extensions
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/remove-background', methods=['POST'])
def remove_background():
    # Check if the POST request contains the 'image' file
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400
    
    file = request.files['image']
    
    # Check if the file is not empty and has an allowed file extension
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Define output file path for processed image
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'output.png')
        
        # Replace with your background removal command or function
        command = f'backgroundremover -i "{filepath}" -o "{output_filepath}"'
        
        try:
            # Execute the background removal command
            subprocess.run(command, shell=True, check=True)
            
            return jsonify({'success': True, 'processedImagePath': output_filepath}), 200
        
        except subprocess.CalledProcessError as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    else:
        return jsonify({'success': False, 'message': 'File type not allowed'}), 400

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
