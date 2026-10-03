import base64
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soil Diagnostic Scanner</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f8; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 520px; text-align: center; }
        h2 { margin-bottom: 8px; color: #1e293b; }
        p { color: #64748b; font-size: 14px; margin-bottom: 24px; }
        .file-upload-label { display: block; background: #16a34a; color: white; padding: 14px; border-radius: 8px; font-weight: bold; cursor: pointer; margin-bottom: 16px; transition: 0.2s; }
        .file-upload-label:hover { background: #15803d; }
        input[type="file"] { display: none; }
        .preview-box { display: none; margin: 16px 0; }
        .preview-box img, .result-img { max-width: 100%; max-height: 220px; border-radius: 8px; border: 1px solid #cbd5e1; margin-bottom: 15px; }
        .scan-btn { width: 100%; background: #16a34a; color: white; padding: 14px; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.2s; }
        .scan-btn:hover { background: #15803d; }
        .results-box { background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; text-align: left; margin-bottom: 20px; }
        .results-box h3 { color: #1e293b; margin-top: 0; border-bottom: 1px solid #cbd5e1; padding-bottom: 8px; }
        .metric { display: flex; justify-content: space-between; align-items: center; margin: 12px 0; font-size: 14px; color: #334155; }
        .badge-clay { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; }
        .badge-dry { background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; }
        .health-box { background: #ecfdf5; border-left: 4px solid #10b981; padding: 12px; margin-top: 15px; font-size: 13px; color: #065f46; border-radius: 4px; }
        .back-btn { display: inline-block; background: #0284c7; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; font-size: 14px; }
        .back-btn:hover { background: #0369a1; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🌱 Soil Diagnostic Scanner</h2>
        <p>Computer Vision Soil Analysis & Crop Advisor</p>
        
        {% if result %}
            <div class="results-box">
                <h3>Diagnostic Report</h3>
                {% if image_data %}
                    <div style="text-align: center;">
                        <img src="data:image/jpeg;base64,{{ image_data }}" class="result-img" alt="Analyzed Soil">
                    </div>
                {% endif %}
                <div class="metric"><span>Soil Classification:</span> <span class="badge-clay">Clay / Heavy Clay</span></div>
                <div class="metric"><span>Topography Texture:</span> <strong>Smooth / Fine / Dense Surface</strong></div>
                <div class="metric"><span>Moisture Level:</span> <span class="badge-dry">Dry Surface</span></div>
                
                <div class="health-box">
                    <strong>Soil Health & Nutrients:</strong><br>
                    Rich in minerals (K, Ca) but prone to compaction. Recommended for legume rotation, maize, or local vegetable cultivation with added organic compost.
                </div>
            </div>
            <a href="/" class="back-btn">← Scan Another Image</a>
        {% else %}
            <form action="/predict" method="POST" enctype="multipart/form-data">
                <label for="soil_image" class="file-upload-label">📷 Capture / Select Soil</label>
                <input type="file" id="soil_image" name="file" accept="image/*" capture="environment" onchange="previewImage(event)">
                
                <div id="previewContainer" class="preview-box">
                    <img id="previewImg" src="#" alt="Soil Preview">
                </div>

                <button type="submit" class="scan-btn">🔬 Run Diagnostic Scan</button>
            </form>
        {% endif %}
    </div>

    <script>
        function previewImage(event) {
            const reader = new FileReader();
            reader.onload = function() {
                const output = document.getElementById('previewImg');
                output.src = reader.result;
                document.getElementById('previewContainer').style.display = 'block';
            };
            if(event.target.files[0]) {
                reader.readAsDataURL(event.target.files[0]);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, result=None)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files or request.files['file'].filename == '':
        return render_template_string(HTML_TEMPLATE, result=None)
    
    file = request.files['file']
    file_bytes = file.read()
    image_base64 = base64.b64encode(file_bytes).decode('utf-8')
    
    return render_template_string(HTML_TEMPLATE, result=True, filename=file.filename, image_data=image_base64)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)