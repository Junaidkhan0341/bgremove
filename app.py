from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image
import io
import base64

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
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return jsonify({"image": img_str}), 200
    except Exception as e:
        return jsonify({"error": f"Background removal failed: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
