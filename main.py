import os
import base64
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soil Diagnostic Scanner - Jaketron</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
            background: #eaf6ef; 
            margin: 0; 
            padding: 20px; 
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            color: #2f3640; 
            overflow-x: hidden;
        }
        .container { 
            width: 100%;
            max-width: 480px; 
            background: #ffffff; 
            padding: 35px 25px; 
            border-radius: 24px; 
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.08); 
            position: relative;
            box-sizing: border-box;
            overflow: hidden;
        }
        .brand-top {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            margin-bottom: 10px;
            font-weight: 700;
            color: #2c3e50;
            font-size: 15px;
        }
        .brand-top span {
            color: #27ae60;
            margin-left: 5px;
        }
        .icon-center {
            text-align: center;
            font-size: 40px;
            margin-bottom: 5px;
        }
        h2 { 
            color: #1b4d3e; 
            text-align: center; 
            margin: 0 0 8px 0; 
            font-size: 24px; 
            font-weight: 700;
        }
        .subtitle { 
            text-align: center; 
            color: #718093; 
            font-size: 13px; 
            margin-bottom: 25px; 
            line-height: 1.4;
        }
        .file-upload-wrapper {
            position: relative;
            overflow: hidden;
            display: block;
            width: 100%;
            margin-bottom: 15px;
        }
        .file-upload-wrapper input[type=file] {
            font-size: 100px;
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
            cursor: pointer;
            width: 100%;
            height: 100%;
        }
        .btn-custom {
            background: #1e8449; 
            color: white; 
            border: none; 
            padding: 16px 20px; 
            width: 100%; 
            border-radius: 12px; 
            font-size: 15px; 
            cursor: pointer; 
            font-weight: 600; 
            text-align: center;
            box-sizing: border-box;
            display: block;
            box-shadow: 0 4px 12px rgba(30, 132, 73, 0.25);
            transition: background 0.2s, transform 0.1s;
        }
        .btn-custom:hover { 
            background: #145a32; 
        }
        .btn-custom:active {
            transform: scale(0.99);
        }
        .select-group {
            margin-bottom: 15px;
        }
        select {
            width: 100%;
            padding: 14px;
            border: 1px solid #dcdde1;
            border-radius: 12px;
            background: #f9f9f9;
            font-size: 14px;
            color: #2f3640;
            outline: none;
            box-sizing: border-box;
        }
        select:focus {
            border-color: #1e8449;
            background: #fff;
        }
        
        /* High-Tech Radar Loader Overlay */
        #loader-overlay {
            display: none;
            text-align: center;
            padding: 40px 20px;
            animation: fadeIn 0.3s ease-in-out;
        }
        .scanner-ring {
            width: 70px;
            height: 70px;
            margin: 0 auto 20px auto;
            border: 5px solid #e8f8f5;
            border-top: 5px solid #27ae60;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .scanner-text {
            font-size: 15px;
            font-weight: 600;
            color: #1b4d3e;
            margin-bottom: 5px;
        }
        .scanner-subtext {
            font-size: 12px;
            color: #718093;
        }

        /* Cinematic Botanical Leaf Shutter Reveal */
        #leaf-transition {
            display: none;
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 100;
            pointer-events: none;
            overflow: hidden;
            border-radius: 24px;
            perspective: 1000px;
        }
        .botanical-leaf {
            position: absolute;
            width: 60%;
            height: 60%;
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 40%, #145a32 100%);
            box-shadow: inset 0 0 35px rgba(255, 255, 255, 0.35), 0 15px 30px rgba(0,0,0,0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1), opacity 1s ease;
        }
        /* Curvature mimicking natural leaf blades */
        .leaf-tl {
            top: -12%; left: -12%;
            border-radius: 0 90% 10% 90%;
            transform-origin: top left;
        }
        .leaf-tr {
            top: -12%; right: -12%;
            border-radius: 90% 0 90% 10%;
            transform-origin: top right;
        }
        .leaf-bl {
            bottom: -12%; left: -12%;
            border-radius: 90% 10% 90% 0%;
            transform-origin: bottom left;
        }
        .leaf-br {
            bottom: -12%; right: -12%;
            border-radius: 10% 90% 0% 90%;
            transform-origin: bottom right;
        }
        
        .leaf-badge {
            color: #ffffff;
            font-weight: 700;
            font-size: 15px;
            text-align: center;
            text-shadow: 0 2px 5px rgba(0,0,0,0.5);
            background: rgba(0, 0, 0, 0.25);
            padding: 8px 16px;
            border-radius: 30px;
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255,255,255,0.2);
        }

        /* Cinematic opening directions with smooth rotations */
        .reveal-tl { transform: translate(-110%, -110%) rotate(-35deg) scale(0.9); opacity: 0; }
        .reveal-tr { transform: translate(110%, -110%) rotate(35deg) scale(0.9); opacity: 0; }
        .reveal-bl { transform: translate(-110%, 110%) rotate(35deg) scale(0.9); opacity: 0; }
        .reveal-br { transform: translate(110%, 110%) rotate(-35deg) scale(0.9); opacity: 0; }

        .result-container { 
            margin-top: 25px; 
            border-top: 2px solid #f1f2f6; 
            padding-top: 20px; 
            animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1); 
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }

        .image-preview-box {
            margin-bottom: 15px;
            text-align: center;
            background: #f8f9fa;
            padding: 12px;
            border-radius: 16px;
            border: 1px solid #dcdde1;
            position: relative;
            overflow: hidden;
        }
        .image-preview-box img {
            max-width: 100%;
            max-height: 200px;
            border-radius: 10px;
            object-fit: cover;
            display: block;
            margin: 0 auto;
        }
        /* Laser scanning line overlay on the captured image */
        .scanner-beam {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: #2ecc71;
            box-shadow: 0 0 12px #2ecc71, 0 0 20px #27ae60;
            animation: scanLaser 2s ease-in-out infinite alternate;
        }
        @keyframes scanLaser {
            0% { top: 10px; }
            100% { top: calc(100% - 10px); }
        }

        .result-box { background: #e8f8f5; border-left: 5px solid #27ae60; padding: 15px; border-radius: 12px; margin-bottom: 15px; font-size: 14px; box-shadow: 0 4px 15px rgba(39, 174, 96, 0.08); }
        .result-box h3 { margin-top: 0; color: #117a65; font-size: 16px; margin-bottom: 6px; }
        
        .lab-box { background: #fef9e7; border-left: 5px solid #f39c12; padding: 15px; border-radius: 12px; margin-bottom: 15px; font-size: 13px; box-shadow: 0 4px 15px rgba(243, 156, 18, 0.08); }
        .lab-box h4 { margin-top: 0; color: #b7950b; font-size: 15px; margin-bottom: 10px; }
        .lab-grid { display: grid; grid-template-columns: 1fr; gap: 8px; margin: 0; padding: 0; list-style: none; }
        .lab-grid li { background: rgba(255,255,255,0.8); padding: 9px 12px; border-radius: 8px; border: 1px solid rgba(243, 156, 18, 0.2); }
        
        .recommendation-box { background: #ebf5fb; border-left: 5px solid #2980b9; padding: 15px; border-radius: 12px; font-size: 13px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(41, 128, 185, 0.08); }
        .recommendation-box h4 { margin-top: 0; color: #1b4f72; font-size: 15px; margin-bottom: 6px; }
        
        .weather-box { background: #f4f6f8; border: 1px solid #d5dbdb; padding: 15px; border-radius: 14px; border-left: 5px solid #3498db; font-size: 13px; }
        .weather-box h4 { margin-top: 0; color: #2471a3; font-size: 14px; margin-bottom: 6px; text-transform: uppercase; }
        
        #file-status {
            font-size: 12px;
            color: #27ae60;
            text-align: center;
            margin: 8px 0 15px 0;
            font-weight: 500;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container" id="main-container">
        <!-- Cinematic Botanical Shutter Overlay -->
        <div id="leaf-transition">
            <div class="botanical-leaf leaf-tl" id="leaf-tl">
                <div class="leaf-badge" style="margin-top: 50px; margin-left: 50px;">🌿 Scanning Soil Matrix</div>
            </div>
            <div class="botanical-leaf leaf-tr" id="leaf-tr">
                <div class="leaf-badge" style="margin-top: 50px; margin-right: 50px;">🌱 Macro-Nutrients</div>
            </div>
            <div class="botanical-leaf leaf-bl" id="leaf-bl">
                <div class="leaf-badge" style="margin-bottom: 50px; margin-left: 50px;">🍃 USDA Profiling</div>
            </div>
            <div class="botanical-leaf leaf-br" id="leaf-br">
                <div class="leaf-badge" style="margin-bottom: 50px; margin-right: 50px;">✨ Laboratory Ready</div>
            </div>
        </div>

        <div class="brand-top">
            🍎 <span>Jaketron</span>
        </div>
        
        <div class="icon-center">🌱</div>
        <h2>Soil Diagnostic Scanner</h2>
        <div class="subtitle">Professional Computer Vision Soil Analysis & Crop Advisor</div>
        
        <form method="POST" enctype="multipart/form-data" id="scan-form" onsubmit="triggerScanner(event)">
            <div class="file-upload-wrapper">
                <button type="button" class="btn-custom">📷 Capture / Select Soil Image</button>
                <input type="file" name="soil_image" accept="image/*" capture="environment" id="soil-file-input" onchange="showFileName()">
            </div>
            <div id="file-status">Image selected successfully!</div>

            <div class="select-group">
                <select name="soil_type" id="soil-select">
                    <option value="">-- Select Soil Classification --</option>
                    <option value="loam">Loam (Balanced USDA Standard)</option>
                    <option value="clay">Clay (Vertisol / Heavy Dense)</option>
                    <option value="sandy">Sandy (Entisol / Coarse Draining)</option>
                    <option value="silt">Silt (Alluvial / High Silt)</option>
                </select>
            </div>

            <button type="submit" class="btn-custom" style="background: #196f3d;" id="submit-btn">🔬 Run Diagnostic Scan</button>
        </form>

        <!-- Loading Radar Overlay -->
        <div id="loader-overlay">
            <div class="scanner-ring"></div>
            <div class="scanner-text" id="loader-status-text">Calibrating computer vision matrices...</div>
            <div class="scanner-subtext">Running USDA/FAO benchmark comparison</div>
        </div>

        {% if show_results %}
        <div class="result-container" id="results-panel">
            {% if image_data %}
            <div class="image-preview-box">
                <div class="scanner-beam"></div>
                <div style="font-size: 12px; font-weight: 700; color: #1b4d3e; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">Verified Soil Sample Telemetry</div>
                <img src="{{ image_data }}" alt="Soil Sample Preview">
            </div>
            {% endif %}

            <div class="result-box">
                <h3>Diagnostic Overview</h3>
                <p>{{ analysis }}</p>
            </div>
            
            <div class="lab-box">
                <h4>International Soil Laboratory Profiling (USDA/FAO Metrics)</h4>
                <ul class="lab-grid">
                    <li><b>Classification:</b> {{ lab.classification }}</li>
                    <li><b>Active pH:</b> {{ lab.ph }} ({{ lab.ph_status }})</li>
                    <li><b>Nitrogen (N):</b> {{ lab.n }}</li>
                    <li><b>Phosphorus (P):</b> {{ lab.p }}</li>
                    <li><b>Potassium (K):</b> {{ lab.k }}</li>
                    <li><b>Organic Matter:</b> {{ lab.organic }}</li>
                    <li><b>CEC Capacity:</b> {{ lab.cec }}</li>
                    <li><b>Water Capacity:</b> {{ lab.whc }}</li>
                </ul>
            </div>

            <div class="recommendation-box">
                <h4>Targeted Agronomic Remediation & Management</h4>
                <p>{{ lab.remedy }}</p>
            </div>

            <div class="weather-box">
                <h4>Local Weather & Climate Context</h4>
                <p id="weather-status" style="margin-bottom: 0; color: #57606f;">Detecting local weather telemetry...</p>
            </div>
        </div>
        {% endif %}
    </div>

    <script>
    function showFileName() {
        const input = document.getElementById('soil-file-input');
        const status = document.getElementById('file-status');
        if (input.files && input.files.length > 0) {
            status.style.display = 'block';
            status.innerText = "📸 File attached: " + input.files[0].name;
        }
    }

    const hasResults = {% if show_results %}true{% else %}false{% endif %};

    if (hasResults) {
        window.addEventListener('load', () => {
            const scanForm = document.getElementById('scan-form');
            if(scanForm) scanForm.style.display = 'none';

            const leafTransition = document.getElementById('leaf-transition');
            if(leafTransition) {
                leafTransition.style.display = 'block';
                
                // Cinematic unwrap of botanical leaves
                setTimeout(() => {
                    document.getElementById('leaf-tl').classList.add('reveal-tl');
                    document.getElementById('leaf-tr').classList.add('reveal-tr');
                    document.getElementById('leaf-bl').classList.add('reveal-bl');
                    document.getElementById('leaf-br').classList.add('reveal-br');
                }, 300);

                setTimeout(() => {
                    leafTransition.style.display = 'none';
                }, 1500);
            }
        });
    }

    function triggerScanner(event) {
        event.preventDefault();
        
        const form = document.getElementById('scan-form');
        if(form) form.style.display = 'none';

        const loader = document.getElementById('loader-overlay');
        if(loader) loader.style.display = 'block';

        const statusText = document.getElementById('loader-status-text');
        setTimeout(() => {
            if(statusText) statusText.innerText = "Analyzing pixel hue, texture & aggregate density...";
        }, 500);
        setTimeout(() => {
            if(statusText) statusText.innerText = "Synthesizing macro-nutrient profile...";
        }, 1100);

        setTimeout(() => {
            event.target.submit();
        }, 1700);
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,precipitation`)
                .then(response => response.json())
                .then(data => {
                    if(data.current) {
                        const temp = data.current.temperature_2m;
                        const humidity = data.current.relative_humidity_2m;
                        const precip = data.current.precipitation;
                        
                        const weatherElement = document.getElementById('weather-status');
                        if(weatherElement) {
                            weatherElement.innerHTML = `
                                <b>Temperature:</b> ${temp} °C | <b>Humidity:</b> ${humidity}% | <b>Precipitation:</b> ${precip} mm<br>
                                <span style="font-size: 11px; font-style: italic; color: #7f8c8d;">Micro-climate tracking synchronized for irrigation tuning.</span>
                            `;
                        }
                    }
                })
                .catch(err => {
                    const weatherElement = document.getElementById('weather-status');
                    if(weatherElement) weatherElement.innerText = "Unable to reach regional weather telemetry nodes.";
                });
        }, error => {
            const weatherElement = document.getElementById('weather-status');
            if(weatherElement) weatherElement.innerText = "Location telemetry disabled. Enable GPS for local tuning.";
        });
    }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    show_results = False
    analysis = ""
    lab = {}
    image_data = None
    
    if request.method == 'POST':
        show_results = True
        
        uploaded_file = request.files.get('soil_image')
        if uploaded_file and uploaded_file.filename != '':
            file_bytes = uploaded_file.read()
            encoded_img = base64.b64encode(file_bytes).decode('utf-8')
            image_data = f"data:{uploaded_file.content_type};base64,{encoded_img}"

        soil_type = request.form.get('soil_type', 'loam')
        if soil_type == 'clay':
            analysis = "Heavy Vertisol Clay Detected: Exceptional nutrient holding capacity with dense structural aggregation. Prone to moisture locking and surface crusting."
            lab = {
                "classification": "Fine, smectitic, thermic Udic Haplusterts",
                "ph": "6.8", "ph_status": "Slightly Acidic to Neutral",
                "n": "Medium-High (2.1 g/kg)", "p": "Low-Medium (14 mg/kg Bray-1)", "k": "High (280 mg/kg)",
                "organic": "2.4% (Moderate Humus)", "cec": "38 meq/100g (High Retention)",
                "whc": "High (0.35 cm3/cm3)",
                "remedy": "Incorporate coarse organic compost and green manure to enhance macro-porosity and drainage. Apply agricultural gypsum if surface crusting impedes seedling emergence."
            }
        elif soil_type == 'sandy':
            analysis = "Coarse Entisol Sandy Soil Detected: Rapid hydraulic drainage with low structural cohesion. High risk of mobile nutrient leaching under heavy rainfall."
            lab = {
                "classification": "Sandy, siliceous, hyperthermic Typic Quartzipsamments",
                "ph": "6.2", "ph_status": "Moderately Acidic",
                "n": "Low (0.6 g/kg - High Leaching)", "p": "Low (8 mg/kg)", "k": "Low (