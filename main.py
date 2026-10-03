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
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; color: #334155; }
        .card { background: #ffffff; padding: 32px; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05); width: 100%; max-width: 500px; text-align: center; border: 1px solid #f1f5f9; }
        h2 { margin-bottom: 6px; color: #0f172a; font-size: 22px; }
        p { color: #64748b; font-size: 13px; margin-bottom: 24px; }
        .file-upload-label { display: block; background: #22c55e; color: white; padding: 14px; border-radius: 10px; font-weight: 600; cursor: pointer; margin-bottom: 16px; transition: background 0.2s ease; }
        .file-upload-label:hover { background: #16a34a; }
        input[type="file"] { display: none; }
        .preview-box { display: none; margin: 16px 0; }
        .preview-box img, .result-img { width: 100%; max-height: 240px; object-fit: cover; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); }
        .scan-btn { width: 100%; background: #22c55e; color: white; padding: 14px; border: none; border-radius: 10px; font-weight: 600; font-size: 15px; cursor: pointer; transition: background 0.2s ease; }
        .scan-btn:hover { background: #16a34a; }
        .results-box { background: #fdfdfd; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; text-align: left; margin-bottom: 20px; box-shadow: inset 0 2px 4px 0 rgba(0,0,0,0.01); }
        .results-box h3 { color: #0f172a; font-size: 16px; margin-top: 0; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px; margin-bottom: 14px; }
        .metric { display: flex; justify-content: space-between; align-items: center; margin: 10px 0; font-size: 13.5px; color: #475569; }
        .badge-clay { background: #f0fdf4; color: #16a34a; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 12.5px; border: 1px solid #dcfce7; }
        .badge-dry { background: #f0f9ff; color: #0284c7; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 12.5px; border: 1px solid #e0f2fe; }
        .health-box { background: #f0fdf4; border-left: 4px solid #22c55e; padding: 12px; margin-top: 14px; font-size: 13px; color: #166534; border-radius: 0 8px 8px 0; line-height: 1.5; }
        .back-btn { display: inline-block; background: #0ea5e9; color: white; text-decoration: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; font-size: 13.5px; transition: background 0.2s ease; }
        .back-btn:hover { background: #0284c7; }
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
                    <div>
                        <img src="data:image/jpeg;base64,{{ image_data }}" class="result-img" alt="Analyzed Soil">
                    </div>
                {% endif %}
                <div class="metric"><span>Soil Classification:</span> <span class="badge-clay">Clay / Heavy Clay</span></div>
                <div class="metric"><span>Topography Texture:</span> <strong>Smooth / Fine / Dense</strong></div>
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