from flask import Flask
from workers import wsgi

app = Flask(__name__)


@app.get("/")
def home():
    return {
        "status": "online",
        "service": "ESP AI Cloud",
        "message": "ESP32-CAM API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict():
    return {
        "status": "success",
        "prediction": "not_ready",
        "confidence": 0.0,
        "message": "Image received successfully"
    }


class Default:
    pass


Default = wsgi.entrypoint(app)