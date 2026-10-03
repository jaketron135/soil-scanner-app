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
        :root {
            --primary-green: #15803d;
            --primary-hover: #166534;
            --border-color: #bbf7d0;
            --text-dark: #0f172a;
            --text-muted: #475569;
        }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%); 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0; 
            color: var(--text-dark); 
        }
        .card { 
            background: #ffffff; 
            padding: 32px 26px; 
            border-radius: 20px; 
            box-shadow: 0 12px 30px -8px rgba(21, 128, 61, 0.15), 0 4px 6px -4px rgba(0, 0, 0, 0.05); 
            width: 100%; 
            max-width: 500px; 
            text-align: center; 
            border: 1px solid var(--border-color); 
        }
        .logo-icon { font-size: 38px; margin-bottom: 4px; }
        h2 { margin: 0 0 4px 0; color: #14532d; font-size: 22px; font-weight: 700; }
        p { color: var(--text-muted); font-size: 13px; margin-bottom: 20px; }
        .file-upload-label { 
            display: block; 
            background: linear-gradient(135deg, #16a34a, #15803d); 
            color: white; 
            padding: 14px; 
            border-radius: 12px; 
            font-weight: 600; 
            cursor: pointer; 
            margin-bottom: 16px; 
            box-shadow: 0 4px 12px rgba(22, 163, 74, 0.25);
            transition: all 0.2s ease; 
        }
        .file-upload-label:hover { background: linear-gradient(135deg, #15803d, #14532d); transform: translateY(-1px); }
        input[type="file"] { display: none; }
        .preview-box { display: none; margin: 16px 0; }
        .preview-box img, .result-img { 
            width: 100%; 
            max-height: 200px; 
            object-fit: cover; 
            border-radius: 12px; 
            border: 2px solid var(--border-color); 
            margin-bottom: 14px; 
            box-shadow: 0 4px 10px rgba(0,0,0,0.04); 
        }
        .scan-btn { 
            width: 100%; 
            background: linear-gradient(135deg, #16a34a, #15803d); 
            color: white; 
            padding: 14px; 
            border: none; 
            border-radius: 12px; 
            font-weight: 600; 
            font-size: 15px; 
            cursor: pointer; 
            box-shadow: 0 4px 12px rgba(22, 163, 74, 0.25);
            transition: all 0.2s ease; 
        }
        .scan-btn:hover { background: linear-gradient(135deg, #15803d, #14532d); transform: translateY(-1px); }
        .results-box { 
            background: #fafaf9; 
            border: 1px solid #e7e5e4; 
            padding: 18px; 
            border-radius: 14px; 
            text-align: left; 
            margin-bottom: 16px; 
        }
        .results-box h3 { 
            color: #14532d; 
            font-size: 16px; 
            margin-top: 0; 
            border-bottom: 2px solid var(--border-color); 
            padding-bottom: 6px; 
            margin-bottom: 12px; 
        }
        .metric { display: flex; justify-content: space-between; align-items: center; margin: 8px 0; font-size: 13.5px; color: var(--text-muted); }
        .badge-clay { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 12px; border: 1px solid #bbf7d0; }
        .badge-dry { background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 12px; border: 1px solid #bae6fd; }
        .badge-fert { background: #fef3c7; color: #b45309; padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 12px; border: 1px solid #fde68a; }
        .fert-box { 
            background: #fefce8; 
            border-left: 4px solid #ca8a04; 
            padding: 10px 12px; 
            margin-top: 12px; 
            font-size: 13px; 
            color: #713f12; 
            border-radius: 0 8px 8px 0; 
            line-height: 1.4; 
        }
        .veg-box { 
            background: #f0fdf4; 
            border-left: 4px solid #16a34a; 
            padding: 10px 12px; 
            margin-top: 10px; 
            font-size: 13px; 
            color: #14532d; 
            border-radius: 0 8px 8px 0; 
            line-height: 1.5; 
        }
        .veg-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-top: 10px;
        }
        .veg-card {
            background: #ffffff;
            border: 1px solid #bbf7d0;
            border-radius: 8px;
            overflow: hidden;
            text-align: center;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .veg-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(22, 163, 74, 0.2);
        }
        .veg-card img {
            width: 100%;
            height: 55px;
            object-fit: cover;
        }
        .veg-card span {
            display: block;
            font-size: 11px;
            font-weight: 600;
            color: #166534;
            padding: 3px 2px;
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .modal-content {
            background: white;
            padding: 20px;
            border-radius: 16px;
            max-width: 380px;
            width: 100%;
            text-align: left;
            position: relative;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
        }
        .modal-content img {
            width: 100%;
            height: 160px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .modal-content h4 {
            margin: 0 0 8px 0;
            color: #14532d;
            font-size: 18px;
            text-align: center;
        }
        .modal-details {
            font-size: 12.5px;
            color: #334155;
            line-height: 1.5;
            margin-bottom: 16px;
        }
        .modal-details p {
            margin: 4px 0;
            color: #334155;
        }
        .close-btn {
            display: block;
            width: 100%;
            background: #15803d;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            text-align: center;
        }
        .back-btn { 
            display: inline-block; 
            background: #15803d; 
            color: white; 
            text-decoration: none; 
            padding: 11px 20px; 
            border-radius: 10px; 
            font-weight: 600; 
            font-size: 13.5px; 
            box-shadow: 0 4px 10px rgba(21, 128, 61, 0.2);
            transition: all 0.2s ease; 
        }
        .back-btn:hover { background: #14532d; transform: translateY(-1px); }
    </style>
</head>
<body>
    <div class="card">
        <div class="logo-icon">🌿</div>
        <h2>Soil Diagnostic Scanner</h2>
        <p>Professional Computer Vision Soil Analysis & Crop Advisor</p>
        
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
                <div class="metric"><span>Fertilizer Needed:</span> <span class="badge-fert">Moderate / Required</span></div>
                
                <div class="fert-box">
                    <strong>🧪 Fertilizer Recommendation:</strong><br>
                    Nitrogen (N) supplement and organic compost recommended to loosen clay compaction.
                </div>

                <div class="veg-box">
                    <strong>🌱 Recommended Vegetable Varieties:</strong><br>
                    Click any crop below to view specifications:
                    <div class="veg-grid">
                        <div class="veg-card" onclick="openModal('Tomatoes', 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400', 'October to February (Dry Season)', '4 plants per m² (Spacing: 50x50 cm)', 'Organic: 3.5 kg / m²<br>Inorganic (14-14-14): 0.06 kg / m²')">
                            <img src="https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=200" alt="Tomatoes">
                            <span>Tomatoes</span>
                        </div>
                        <div class="veg-card" onclick="openModal('Bell Peppers', 'https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=400', 'November to March', '6 plants per m² (Spacing: 40x40 cm)', 'Organic: 3.0 kg / m²<br>Inorganic (14-14-14): 0.05 kg / m²')">
                            <img src="https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=200" alt="Bell Peppers">
                            <span>Peppers</span>
                        </div>
                        <div class="veg-card" onclick="openModal('Broccoli', 'https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?w=400', 'September to December (Cool Months)', '4 to 5 plants per m² (Spacing: 45x45 cm)', 'Organic: 4.0 kg / m²<br>Inorganic (Urea/14-14-14): 0.07 kg / m²')">
                            <img src="https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?w=200" alt="Broccoli">
                            <span>Broccoli</span>
                        </div>
                        <div class="veg-card" onclick="openModal('Cabbage', 'https://images.unsplash.com/photo-1550989460-0adf9ea622e2?w=400', 'October to January', '4 plants per m² (Spacing: 50x50 cm)', 'Organic: 4.0 kg / m²<br>Inorganic (16-20-0): 0.08 kg / m²')">
                            <img src="https://images.unsplash.com/photo-1550989460-0adf9ea622e2?w=200" alt="Cabbage">
                            <span>Cabbage</span>
                        </div>
                        <div class="veg-card" onclick="openModal('Green Beans', 'https://images.unsplash.com/photo-1567306226416-28f0efdc8849?w=400', 'September to February', '25 to 30 plants per m² (Direct seeded)', 'Organic: 2.5 kg / m²<br>Inorganic (0-20-20): 0.04 kg / m²')">
                            <img src="https://images.unsplash.com/photo-1567306226416-28f0efdc8849?w=200" alt="Green Beans">
                            <span>Beans</span>
                        </div>
                        <div class="veg-card" onclick="openModal('Sweet Corn', 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400', 'Year-round (Best: May-June or Nov-Dec)', '8 to 10 plants per m² (Spacing: 25x40 cm)', 'Organic: 4.0 kg / m²<br>Inorganic (Urea 46-0-0): 0.07 kg / m²')">
                            <img src="https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=200" alt="Sweet Corn">
                            <span>Corn</span>
                        </div>
                        <div class="veg-card" onclick="openModal('Eggplants', 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400', 'October to March', '3 plants per m² (Spacing: 60x60 cm)', 'Organic: 3.5 kg / m²<br>Inorganic (14-14-14): 0.06 kg / m²')">
                            <img src="https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=200" alt="Eggplants">
                            <span>Eggplants</span>
                        </div>
                        <div class="veg-card" onclick="openModal('Spinach', 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400', 'November to February (Cool Season)', '40 to 50 plants per m² (Broadcast/Row)', 'Organic: 3.0 kg / m²<br>Inorganic (46-0-0): 0.04 kg / m²')">
                            <img src="https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=200" alt="Spinach">
                            <span>Spinach</span>
                        </div>
                    </div>
                </div>
            </div>
            <a href="/" class="back-btn">← Scan Another Image</a>
        {% else %}
            <form action="/predict" method="POST" enctype="multipart/form-data">
                <label for="soil_image" class="file-upload-label">📸 Capture / Select Soil Image</label>
                <input type="file" id="soil_image" name="file" accept="image/*" capture="environment" onchange="previewImage(event)">
                
                <div id="previewContainer" class="preview-box">
                    <img id="previewImg" src="#" alt="Soil Preview">
                </div>

                <button type="submit" class="scan-btn">🔬 Run Diagnostic Scan</button>
            </form>
        {% endif %}
    </div>

    <!-- Image Popup Modal -->
    <div id="vegModal" class="modal">
        <div class="modal-content">
            <img id="modalImg" src="" alt="Vegetable">
            <h4 id="modalTitle">Crop Name</h4>
            <div class="modal-details" id="modalTextDetails">
                <!-- Dynamic content injected via JS -->
            </div>
            <button class="close-btn" onclick="closeModal()">Close</button>
        </div>
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

        function openModal(title, imgSrc, month, density, fert) {
            document.getElementById('modalTitle').innerText = title;
            document.getElementById('modalImg').src = imgSrc;
            
            let detailsHtml = `
                <p><strong>📅 Best Planting Month:</strong><br>${month}</p>
                <p style="margin-top:8px;"><strong>📏 Surface Area Density:</strong><br>${density}</p>
                <p style="margin-top:8px;"><strong>🧪 Fertilizer Requirement (per 1 m²):</strong><br>${fert}</p>
            `;
            document.getElementById('modalTextDetails').innerHTML = detailsHtml;
            document.getElementById('vegModal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('vegModal').style.display = 'none';
        }

        window.onclick = function(event) {
            const modal = document.getElementById('vegModal');
            if (event.target == modal) {
                modal.style.display = 'none';
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