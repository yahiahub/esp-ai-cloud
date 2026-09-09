from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# ==========================================
# SETTINGS
# ==========================================

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "service": "ESP32-CAM AI Cloud API",
        "message": "Server is running"
    })

# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })

# ==========================================
# RECEIVE IMAGE
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    # --------------------------------------
    # Check Content-Type
    # --------------------------------------

    content_type = request.content_type or ""

    if not content_type.startswith("image/"):
        return jsonify({
            "status": "error",
            "message": "Request must contain an image/jpeg"
        }), 400

    # --------------------------------------
    # Read image
    # --------------------------------------

    image_data = request.get_data()

    if not image_data:
        return jsonify({
            "status": "error",
            "message": "No image received"
        }), 400

    # --------------------------------------
    # Check image size
    # --------------------------------------

    if len(image_data) > MAX_IMAGE_SIZE:
        return jsonify({
            "status": "error",
            "message": "Image is too large"
        }), 413

    # --------------------------------------
    # Check JPEG header
    # --------------------------------------

    if len(image_data) < 2:
        return jsonify({
            "status": "error",
            "message": "Invalid image"
        }), 400

    # JPEG starts with FF D8

    if image_data[0] != 0xFF or image_data[1] != 0xD8:
        return jsonify({
            "status": "error",
            "message": "Invalid JPEG image"
        }), 400

    # --------------------------------------
    # Create temporary filename
    # --------------------------------------

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    filename = f"image_{timestamp}.jpg"

    # --------------------------------------
    # Temporary local storage
    # --------------------------------------

    os.makedirs("received_images", exist_ok=True)

    filepath = os.path.join(
        "received_images",
        filename
    )

    with open(filepath, "wb") as file:
        file.write(image_data)

    # --------------------------------------
    # Log
    # --------------------------------------

    print()
    print("====================================")
    print("IMAGE RECEIVED")
    print("====================================")

    print(f"Filename : {filename}")
    print(f"Size     : {len(image_data)} bytes")

    print("====================================")

    # --------------------------------------
    # AI PLACEHOLDER
    # --------------------------------------

    # AI model will be connected here later.

    prediction = "not_ready"
    confidence = 0.0

    # --------------------------------------
    # Response
    # --------------------------------------

    return jsonify({

        "status": "success",

        "prediction": prediction,

        "confidence": confidence,

        "message": "Image received successfully"

    })


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )