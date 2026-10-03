<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soil Diagnostic Scanner</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f7f6;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }
        .container {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 30px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 25px;
            font-size: 0.95em;
        }
        .upload-box {
            border: 2px dashed #3498db;
            padding: 20px;
            text-align: center;
            border-radius: 8px;
            background-color: #f9bf3b10;
            margin-bottom: 20px;
        }
        .btn {
            background-color: #2ecc71;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            margin-top: 10px;
        }
        .btn:hover {
            background-color: #27ae60;
        }
        .status-box {
            background-color: #e8f8f5;
            border-left: 5px solid #2ecc71;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        .status-box p {
            margin: 0;
            color: #27ae60;
            font-weight: bold;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 20px;
        }
        .metric-card {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 6px;
            border: 1fr solid #e9ecef;
        }
        .metric-label {
            font-size: 0.85em;
            color: #6c757d;
            text-transform: uppercase;
        }
        .metric-value {
            font-size: 1.05em;
            font-weight: bold;
            color: #212529;
            margin-top: 4px;
        }
        .recommendations {
            background-color: #fdfefe;
            border: 1px solid #e2e8f0;
            padding: 15px;
            border-radius: 6px;
        }
        .recommendations h3 {
            margin-top: 0;
            color: #2c3e50;
        }
        .recommendations ul {
            margin: 0;
            padding-left: 20px;
        }
        .recommendations li {
            margin-bottom: 8px;
            color: #34495e;
        }
        .reset-link {
            display: block;
            text-align: center;
            margin-top: 20px;
            color: #3498db;
            text-decoration: none;
        }
        .reset-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>🌱 Soil Diagnostic Scanner</h1>
    <div class="subtitle">Computer Vision Soil Analysis & Crop Advisor</div>

    {% if not results %}
        <form action="/predict" method="post" enctype="multipart/form-data">
            <div class="upload-box">
                <input type="file" name="file" accept="image/*" required>
                <br>
                <button type="submit" class="btn">Analyze Soil Image</button>
            </div>
        </form>
    {% else %}
        <div class="status-box">
            <p>Status: Successfully analyzed '{{ results.filename }}'. Soil health parameters optimal.</p>
        </div>

        <h3>Soil Health Metrics</h3>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Soil pH</div>
                <div class="metric-value">{{ results.metrics.ph_level }}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Moisture Level</div>
                <div class="metric-value">{{ results.metrics.moisture }}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Nitrogen (N)</div>
                <div class="metric-value">{{ results.metrics.nitrogen }}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Phosphorus (P)</div>
                <div class="metric-value">{{ results.metrics.phosphorus }}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Potassium (K)</div>
                <div class="metric-value">{{ results.metrics.potassium }}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Soil Classification</div>
                <div class="metric-value">{{ results.metrics.soil_type }}</div>
            </div>
        </div>

        <div class="recommendations">
            <h3>Crop & Agronomic Recommendations</h3>
            <ul>
                {% for rec in results.metrics.recommendations %}
                    <li>{{ rec }}</li>
                {% endfor %}
            </ul>
        </div>

        <a href="/" class="reset-link">← Scan Another Image</a>
    {% endif %}
</div>

</body>
</html>