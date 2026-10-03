import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_diagnostic_model(image_path):
    # Simulated Computer Vision Soil Analysis Output
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
        body { font-family: Arial, sans-serif; background-color: #f4f6f8; display: flex; justify-content: center; padding: 40px; margin: 0; }
        .card { background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 480px; width: 100%; text-align: center; }
        .btn { background-color: #2e7d32; color: #fff; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 16px; width: 100%; margin-top: 15px; display: block; box-sizing: border-box; text-decoration: none; }
        .btn:hover { background-color: #1b5e20; }
        .img-preview { width: 100%; max-height: 250px; object-fit: cover; border-radius: 8px; margin: 15px 0; display: none; }
        .badge { background: #e8f5e9; color: #2e7d32; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
        .row { display: flex; justify-content: space-between; margin: 10px 0; text-align: left; }
    </style>
</head>
<body>

<div class="card">
    <h2>🌱 Soil Diagnostic Scanner</h2>
    <p>Computer Vision Soil Analysis & Crop Advisor</p>

    {% if results %}
        <div style="text-align: left;">
            <h3>Diagnostic Report</h3>
            <img src="/{{ image_url }}" alt="Soil Sample Preview" class="img-preview" style="display: block;">

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

            <a href="/" class="btn" style="text-align: center;">🔬 Run Another Scan</a>
        </div>
    {% else %}
        <!-- MANUAL SUBMISSION FORM -->
        <form action="/predict" method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required onchange="showPreview(event)">
            
            <!-- Live Preview Element -->
            <img id="preview-box" class="img-preview" alt="Selected Soil Sample">

            <!-- Manual Trigger Button (Form only submits when clicked) -->
            <button type="submit" class="btn">🔬 Run Diagnostic Scan</button>
        </form>

        <script>
            // Displays preview locally in browser; strictly does NOT submit the form
            function showPreview(event) {
                const input = event.target;
                if (input.files && input.files[0]) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const preview = document.getElementById('preview-box');
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    };
                    reader.readAsDataURL(input.files[0]);
                }
            }
        </script>
    {% endif %}
</div>

</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE, results=None)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return redirect(url_for('index'))

    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        if allowed_file(file.filename):
            from werkzeug.utils import secure_filename
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            results = run_diagnostic_model(filepath)
            return render_template_string(HTML_TEMPLATE, results=results, image_url=filepath)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)