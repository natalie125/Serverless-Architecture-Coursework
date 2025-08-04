import json
import base64
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify

app = Flask(__name__)
cold_start = True

@app.route("/", methods=["POST"])
def resize():
    global cold_start
    try:
        body = request.get_json()
        image_data = base64.b64decode(body["image"])
        image = Image.open(BytesIO(image_data))
        resized_image = image.resize((100, 100))

        buffer = BytesIO()
        resized_image.save(buffer, format="PNG")
        buffer.seek(0)
        img_b64 = base64.b64encode(buffer.read()).decode("utf-8")
        start_type = "cold" if cold_start else "warm"
        cold_start = False

        return jsonify({
            "resized_image": img_b64,
            "start_type": start_type
        })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500
