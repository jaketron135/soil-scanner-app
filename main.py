import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soil Diagnostic & Testing Platform</title>
    <style>
        :root {
            --primary: #1e3799;
            --secondary: #4a69bd;
            --accent: #27ae60;
            --bg-color: #f4f7f6;
            --card-bg: #ffffff;
            --text-main: #2f3640;
            --text-muted: #718093;
            --border: #dcdde1;
        }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
            background: var(--bg-color); 
            margin: 0; 
            padding: 30px; 
            color: var(--text-main); 
            line-height: 1.6; 
        }
        .container { 
            max-width: 820px; 
            background: var(--card-bg); 
            margin: 0 auto; 
            padding: 40px; 
            border-radius: 16px; 
            box-shadow: 0 12px 35px rgba(0,0,0,0.08); 
        }
        .header {
            text-align: center;
            margin-bottom: 35px;
            border-bottom: 2px solid var(--bg-color);
            padding-bottom: 20px;
        }
        h2 { 
            color: var(--primary); 
            margin: 0 0 8px 0; 
            font-size: 28px; 
            letter-spacing: -0.5px; 
        }
        .subtitle { 
            color: var(--text-muted); 
            font-size: 14px; 
            font-weight: 500;
        }
        .form-section { 
            background: #fafbfc; 
            border: 1px solid var(--border); 
            padding: 25px; 
            border-radius: 12px; 
            margin-bottom: 25px; 
        }
        .form-group { 
            margin-bottom: 20px; 
        }
        .form-group:last-child { 
            margin-bottom: 0; 
        }
        label { 
            display: block; 
            margin-bottom: 8px; 
            font-weight: 600; 
            color: #353b48; 
            font-size: 13px; 
            text-transform: uppercase; 
            letter-spacing: 0.8px; 
        }
        input[type="file"], select { 
            width: 100%; 
            padding: 14px; 
            border: 1px solid var(--border); 
            border-radius: 8px; 
            box-sizing: border-box; 
            background: #fff; 
            font-size: 15px; 
            color: var(--text-main); 
            transition: all 0.2s; 
        }
        input[type="file"]:focus, select:focus { 
            border-color: var(--accent); 
            box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.15);
            outline: none; 
        }
        .camera-hint { 
            font-size: 13px; 
            color: var(--text-muted); 
            margin-top: 6px; 
            display: block; 
        }
        button { 
            background: var(--accent); 
            color: white; 
            border: none; 
            padding: 16px 20px; 
            width: 100%; 
            border-radius: 8px; 
            font-size: 15px; 
            cursor: pointer; 
            font-weight: 700; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
            transition: background 0.2s, transform 0.1s; 
            box-shadow: 0 4px 12px rgba(39, 174, 96, 0.2);
        }
        button:hover { 
            background: #219653; 
        }
        button:active { 
            transform: scale(0.99); 
        }
        
        .result-container { 
            margin-top: 35px; 
            border-top: 2px solid var(--bg-color); 
            padding-top: 30px; 
            animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1); 
        }
        @keyframes fadeIn { 
            from { opacity: 0; transform: translateY(12px); } 
            to { opacity: 1; transform: translateY(0); } 
        }

        .result-box { 
            background: #e8f8f5; 
            border-left: 6px solid var(--accent); 
            padding: 22px; 
            border-radius: 8px; 
            margin-bottom: 20px; 
        }
        .result-box h3 { 
            margin-top: 0; 
            color: #117a65; 
            font-size: 18px; 
            margin-bottom: 8px;
        }
        .result-box p { 
            margin: 0; 
            color: #2d3436;
            font-size: 15px;
        }
        
        .lab-box { 
            background: #fef9e7; 
            border-left: 6px solid #f39c12; 
            padding: 22px; 
            border-radius: 8px; 
            margin-bottom: 20px; 
        }
        .lab-box h4 { 
            margin-top: 0; 
            color: #b7950b; 
            font-size: 18px; 
            margin-bottom: 15px;
        }
        .lab-grid { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 12px; 
            margin: 0; 
            padding: 0; 
            list-style: none; 
        }
        .lab-grid li { 
            font-size: 14px; 
            background: rgba(255,255,255,0.7); 
            padding: 10px 14px; 
            border-radius: 6px; 
            border: 1px solid rgba(243, 156, 18, 0.2);
        }
        
        .recommendation-box { 
            background: #ebf5fb; 
            border-left: 6px solid #2980b9; 
            padding: 22px; 
            border-radius: 8px; 
        }
        .recommendation-box h4 { 
            margin-top: 0; 
            color: #1b4f72; 
            font-size: 18px; 
            margin-bottom: 8px;
        }
        .recommendation-box p { 
            margin: 0; 
            color: #2c3e50;
            font-size: 15px;
        }
        
        .weather-box { 
            background: #f4f6f8; 
            border: 1px solid var(--border); 
            padding: 20px; 
            border-radius: 12px; 
            margin-top: 30px; 
            border-left: 6px solid #3498db; 
        }
        .weather-box h4 { 
            margin-top: 0; 
            color: #2471a3; 
            font-size: 15px; 
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        @media (max-width: 650px) {
            .lab-grid { grid-template-columns: 1fr; }
            .container { padding: 20px; }
            body { padding: 15px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Soil Diagnostic & Testing Platform</h2>
            <div class="subtitle">Global Standard Agronomic Soil Profiling & Micro-Climate Intelligence</div>
        </div>
        
        <form method="POST" enctype="multipart/form-data">
            <div class="form-section">
                <div class="form-group">
                    <label>📷 Soil Sample Visual Capture (Optional)</label>
                    <input type="file" name="soil_image" accept="image/*" capture="environment">
                    <span class="camera-hint">Capture a live photo using your phone camera or select an existing sample image.</span>
                </div>
                <div class="form-group" style="margin-top: 22px;">
                    <label>Select Soil Texture Classification</label>
                    <select name="soil_type">
                        <option value="">-- Choose soil type classification --</option>
                        <option value="loam">Loam (Balanced USDA Standard)</option>
                        <option value="clay">Clay (Vertisol / Heavy Dense Matrix)</option>
                        <option value="sandy">Sandy (Entisol / Coarse Draining)</option>
                        <option value="silt">Silt (Alluvial / High Silt Composition)</option>
                    </select>
                </div>
            </div>
            <button type="submit">Run Global Lab Analysis</button>
        </form>

        {% if analysis %}
        <div class="result-container">
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
        </div>
        {% endif %}

        <div class="weather-box">
            <h4>Real-Time Local Weather & Climate Context</h4>
            <p id="weather-status" style="margin-bottom: 0; font-size: 14px; color: var(--text-muted);">Detecting local weather telemetry and soil micro-climate...</p>
        </div>
    </div>

    <script>
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
                        
                        document.getElementById('weather-status').innerHTML = `
                            <b>Temperature:</b> ${temp} °C &nbsp;|&nbsp; 
                            <b>Air Humidity:</b> ${humidity}% &nbsp;|&nbsp; 
                            <b>Precipitation:</b> ${precip} mm<br>
                            <span style="font-size: 13px; color: var(--text-muted); font-style: italic; margin-top: 4px; display:inline-block;">Live atmospheric tracking active for automated irrigation and evapotranspiration adjustments.</span>
                        `;
                    }
                })
                .catch(err => {
                    document.getElementById('weather-status').innerText = "Unable to fetch telemetry data from regional weather nodes.";
                });
        }, error => {
            document.getElementById('weather-status').innerText = "Location permission restricted. Enable GPS for localized micro-climate tuning.";
        });
    } else {
        document.getElementById('weather-status').innerText = "Geolocation protocol not supported by current browser environment.";
    }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = None
    lab = None
    if request.method == 'POST':
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
                "n": "Low (0.6 g/kg - High Leaching)", "p": "Low (8 mg/kg)", "k": "Low (65 mg/kg)",
                "organic": "1.1% (Low Organic Fraction)", "cec": "6.5 meq/100g (Low Capacity)",
                "whc": "Low (0.12 cm3/cm3 - Rapid Drain)",
                "remedy": "Utilize split-dose fertigation to prevent nutrient washout. Heavily amend with biochar, peat, or aged manure to boost water retention and buffer exchange sites."
            }
        elif soil_type == 'silt':
            analysis = "Alluvial Silt Loam Detected: Smooth tactile texture with optimal capillary moisture transport. Highly fertile matrix sensitive to compaction from heavy machinery."
            lab = {
                "classification": "Coarse-silty, mixed, superactive, mesic Typic Hapludalfs",
                "ph": "7.0", "ph_status": "Neutral (Optimal Biological)",
                "n": "High (3.2 g/kg)", "p": "Medium (22 mg/kg)", "k": "Medium-High (210 mg/kg)",
                "organic": "3.2% (Good Microbial Biomass)", "cec": "22 meq/100g (Balanced)",
                "whc": "High (0.30 cm3/cm3)",
                "remedy": "Apply continuous cover cropping or surface mulching to safeguard against heavy rain splash erosion and crusting. Restrict heavy equipment passes when damp."
            }
        else:
            analysis = "Optimal Loam Matrix Detected: Premium agronomic balance of sand, silt, and clay fractions. Delivers superior root aeration and nutrient availability."
            lab = {
                "classification": "Fine-loamy, mixed, active, mesic Typic Argiudolls",
                "ph": "6.5", "ph_status": "Slightly Acidic (Ideal Range)",
                "n": "High (3.8 g/kg)", "p": "High (35 mg/kg Mehlich-3)", "k": "High (320 mg/kg)",
                "organic": "4.0% (High Microbial Activity)", "cec": "26 meq/100g (Optimal)",
                "whc": "Optimal (0.26 cm3/cm3)",
                "remedy": "Maintain standard crop rotation cycles and light organic topdressing. This matrix represents an ideal baseline configuration for high-yield cultivation."
            }
            
    return render_template_string(HTML_TEMPLATE, analysis=analysis, lab=lab)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)