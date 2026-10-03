import os
from flask import Flask, render_template_string, request, redirect, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'soil_scanner_strict_key_999'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_diagnostic_model(image_path):
    return {
        "classification": "Sandy / Gravelly Loam",
        "texture": "Coarse / Rough",
        "moisture": "Moderate Moisture",
        "health_info": "High aeration, moderate drainage. Benefits from organic compost addition.",
        "recommended_crops": "Sweet Potatoes, Cassava, Peanuts, Watermelon, Legumes"
    }

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soil Diagnostic Scanner</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f8; display: flex; justify-content: center; padding: 40px; }
        .card { background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 480px; width: 100%; }
        .btn { background-color: #2e7d32; color: #fff; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 16px; width: 100%; margin-top: 15px; text-align: center; text-decoration: none; display: block; box-sizing: border-box; }
        .btn:hover { background-color: #1b5e20; }
        .error { color: #d32f2f; margin-bottom: 15px; }
        .img-preview { width: 100%; max-height: 250px; object-fit: cover; border-radius: 8px; margin-bottom: 15px; }
        .badge { background: #e8f5e9; color: #2e7d32; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
        .row { display: flex; justify-content: space-between; margin: 10px 0; }
    </style>
</head>
<body>

<div class="card">
    <h2>🌱 Soil Diagnostic Scanner</h2>
    <p>Computer Vision Soil Analysis & Crop Advisor</p>

    {% if results %}
        <h3>Diagnostic Report</h3>
        <img src="/{{ image_url }}" alt="Soil Sample Preview" class="img-preview">

        <div class="row">
            <span>Soil Classification:</span>
            <span class="badge">{{ results.classification }}</span>
        </div>
        <div class="row">
            <span>Topography Texture:</span>
            <span><b>{{ results.texture }}</b></span>
        </div>
        <div class="row">
            <span>Moisture Level:</span>
            <span><b>{{ results.moisture }}</b></span>
        </div>

        <hr>
        <p><b>🌱 Soil Health & Nutrients:</b><br>{{ results.health_info }}</p>
        <p><b>🌽 Recommended Crops:</b><br>{{ results.recommended_crops }}</p>

        <a href="/clear" class="btn">🔬 Run Another Scan</a>

    {% else %}
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}

        <!-- Explicit POST action to /predict -->
        <form action="/predict" method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required>
            <button type="submit" class="btn">🔬 Run Diagnostic Scan</button>
        </form>
    {% endif %}
</div>

</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    # Only reads session if user deliberately triggered a scan
    results = session.get('results')
    image_url = session.get('image_url')
    return render_template_string(HTML_TEMPLATE, results=results, image_url=image_url)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # If someone accesses /predict directly via GET or refreshes, force redirect to main home page
    if request.method == 'GET':
        return redirect(url_for('index'))

    # Process upload only on valid POST request
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        session['results'] = run_diagnostic_model(filepath)
        session['image_url'] = filepath
        return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/clear', methods=['GET'])
def clear():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)