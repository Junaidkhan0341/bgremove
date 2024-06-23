from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files['image']
    try:
        input_image = Image.open(image)
    except Exception as e:
        return jsonify({"error": f"Invalid image: {e}"}), 400

    try:
        output_image = remove(input_image)
        buffered = io.BytesIO()
        output_image.save(buffered, format="PNG")
        buffered.seek(0)
        return send_file(buffered, mimetype='image/png', as_attachment=True, attachment_filename='output.png')
    except Exception as e:
        return jsonify({"error": f"Background removal failed: {e}"}), 500

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=10002)
