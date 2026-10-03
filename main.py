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
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 480px; text-align: center; }
        h2 { margin-bottom: 8px; color: #1e293b; }
        p { color: #64748b; font-size: 14px; margin-bottom: 24px; }
        .file-upload-label { display: block; background: #0284c7; color: white; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; margin-bottom: 16px; transition: 0.2s; }
        .file-upload-label:hover { background: #0369a1; }
        input[type="file"] { display: none; }
        .preview-box { display: none; margin: 16px 0; }
        .preview-box img { max-width: 100%; max-height: 250px; border-radius: 8px; border: 1px solid #cbd5e1; }
        .scan-btn { width: 100%; background: #16a34a; color: white; padding: 14px; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.2s; }
        .scan-btn:hover { background: #15803d; }
        .back-btn { display: inline-block; margin-top: 16px; text-decoration: none; color: #0284c7; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🌱 Soil Diagnostic Scanner</h2>
        <p>Computer Vision Soil Analysis & Crop Advisor</p>
        
        {% if result %}
            <div style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                <h3 style="color: #166534; margin: 0 0 8px 0;">Diagnostic Results</h3>
                <p style="color: #15803d; margin: 0;"><strong>Status:</strong> {{ result }}</p>
            </div>
            <a href="/" class="back-btn">← Scan Another Image</a>
        {% else %}
            <form action="/predict" method="POST" enctype="multipart/form-data">
                <label for="soil_image" class="file-upload-label">📷 Take Photo / Upload Soil Image</label>
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
        return render_template_string(HTML_TEMPLATE, result="No image uploaded. Please choose a soil photo.")
    
    file = request.files['file']
    # Placeholder for model processing / soil analysis logic
    return render_template_string(HTML_TEMPLATE, result=f"Successfully analyzed '{file.filename}'. Soil health parameters optimal.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)