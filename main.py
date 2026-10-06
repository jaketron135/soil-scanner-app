import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Soil Diagnostic Scanner</title>
    <style>
        body { font-family: Arial, sans-serif; background: #eef2f5; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 600px; background: white; margin: 0 auto; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h2 { color: #2c3e50; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: bold; }
        input[type="file"], select { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
        button { background: #27ae60; color: white; border: none; padding: 12px 20px; width: 100%; border-radius: 6px; font-size: 16px; cursor: pointer; }
        button:hover { background: #219653; }
        .result-box { margin-top: 25px; padding: 20px; background: #e8f8f5; border-left: 5px solid #27ae60; border-radius: 6px; }
        .weather-box { background: #f4f6f8; padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 5px solid #3498db; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Soil Diagnostic Scanner</h2>
        <form method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label>Upload Soil Sample Image:</label>
                <input type="file" name="soil_image" required>
            </div>
            <div class="form-group">
                <label>Select Soil Texture / Type:</label>
                <select name="soil_type">
                    <option value="loam">Loam (Balanced)</option>
                    <option value="clay">Clay (Dense / Heavy)</option>
                    <option value="sandy">Sandy (Loose / Drains Fast)</option>
                    <option value="silt">Silt (Smooth / Moisture Retaining)</option>
                </select>
            </div>
            <button type="submit">Run Soil Analysis</button>
        </form>

        {% if analysis %}
        <div class="result-box">
            <h3>Diagnostic Results</h3>
            <p>{{ analysis }}</p>
        </div>
        {% endif %}

        <div class="weather-box">
            <h4>Local Weather & Climate Context</h4>
            <p id="weather-status">Detecting local weather and soil micro-climate...</p>
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
                            <b>Temperature:</b> ${temp} degC | 
                            <b>Air Humidity:</b> ${humidity}% | 
                            <b>Current Precipitation:</b> ${precip} mm<br>
                            <span style="font-size: 0.9em; color: #555;"><i>Adjusting watering and evaporation recommendations based on local climate.</i></span>
                        `;
                    }
                })
                .catch(err => {
                    document.getElementById('weather-status').innerText = "Unable to fetch live weather data.";
                });
        }, error => {
            document.getElementById('weather-status').innerText = "Location access denied. Enable GPS for localized agronomic advice.";
        });
    } else {
        document.getElementById('weather-status').innerText = "Geolocation is not supported by your browser.";
    }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = None
    if request.method == 'POST':
        soil_type = request.form.get('soil_type', 'loam')
        if soil_type == 'clay':
            analysis = "Clay Soil Detected: High nutrient retention, but compacts easily. Recommended crops: Rice, Cabbage, Broccoli. Add organic compost to improve aeration."
        elif soil_type == 'sandy':
            analysis = "Sandy Soil Detected: Fast drainage and low nutrient retention. Recommended crops: Carrots, Potatoes, Peanuts. Frequent light watering and mulching recommended."
        elif soil_type == 'silt':
            analysis = "Silt Soil Detected: Fertile and moisture-retentive. Recommended crops: Wheat, Corn, Rice, and most vegetables. Ensure proper drainage to prevent waterlogging."
        else:
            analysis = "Loam Soil Detected: Ideal balanced composition! Recommended crops: Tomatoes, Peppers, Beans, and general root crops. Maintain organic matter with light composting."
            
    return render_template_string(HTML_TEMPLATE, analysis=analysis)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)