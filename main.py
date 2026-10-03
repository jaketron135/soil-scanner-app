import sqlite3
import csv
import io
import datetime
import cv2
import numpy as np
import base64
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Database initialization with automatic column migration
def init_db():
    conn = sqlite3.connect("soil_data.db")
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            classification TEXT,
            topography TEXT,
            moisture TEXT,
            image_base64 TEXT
        )
    """)
    
    # Ensure image_base64 column exists if database was created by an older version
    cursor.execute("PRAGMA table_info(scans)")
    columns = [column[1] for column in cursor.fetchall()]
    if "image_base64" not in columns:
        cursor.execute("ALTER TABLE scans ADD COLUMN image_base64 TEXT")
        
    conn.commit()
    conn.close()

init_db()

def analyze_soil_opencv(image_bytes):
    """Processes uploaded soil image using OpenCV for texture, moisture heuristic analysis, and crop recommendations."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return "Unknown", "Unclear Texture", "Undetermined", "Unable to process image matrix.", "None", ""

    _, buffer = cv2.imencode('.jpg', img)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    mean_brightness = np.mean(gray)
    if mean_brightness < 80:
        moisture = "Moist / High Retention"
    elif mean_brightness < 140:
        moisture = "Moderate Moisture"
    else:
        moisture = "Dry Surface"

    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / (img.shape[0] * img.shape[1])
    
    if edge_density > 0.08:
        topography = "Coarse / Rough"
        classification = "Sandy / Gravelly Loam"
        nutrients = "High aeration, moderate drainage. Benefits from organic compost addition."
        crops = "Sweet Potatoes, Cassava, Peanuts, Watermelon, Legumes"
    elif edge_density > 0.03:
        topography = "Moderate Grain"
        classification = "Loam Soil"
        nutrients = "Balanced mineral profile (N-P-K friendly). Ideal for a wide range of crops."
        crops = "Rice, Corn, Sugarcane, Vegetables (Tomatoes, Eggplant, Peppers)"
    else:
        topography = "Smooth / Fine / Dense"
        classification = "Clay / Heavy Clay"
        nutrients = "Rich in minerals (K, Ca) but prone to compaction and poor drainage."
        crops = "Paddy Rice, Taro (Gabi), Bananas, Citrus"

    return classification, topography, moisture, nutrients, crops, image_base64

@app.get("/")
def read_root():
    # Retrieve recent scan history from database
    conn = sqlite3.connect("soil_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, classification, topography, moisture FROM scans ORDER BY id DESC LIMIT 5")
    recent_scans = cursor.fetchall()
    conn.close()

    # Generate HTML table rows for history
    history_rows = ""
    if recent_scans:
        for row in recent_scans:
            history_rows += f"""
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd; font-size: 0.85rem;">{row[0]}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold; color: #2e7d32;">{row[1]}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd; font-size: 0.85rem;">{row[2]}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd; font-size: 0.85rem;">{row[3]}</td>
                </tr>
            """
    else:
        history_rows = """
            <tr>
                <td colspan="4" style="padding: 12px; text-align: center; color: #888;">No recent scans found. Perform a scan above to log history!</td>
            </tr>
        """

    return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Soil Diagnostic Scanner</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 20px; }}
                .container {{ max-width: 550px; margin: 0 auto; background: #fff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center; }}
                .header {{ color: #2e7d32; margin-bottom: 20px; }}
                .upload-box {{ border: 2px dashed #2e7d32; padding: 20px; border-radius: 10px; background: #f9fbf9; margin-bottom: 20px; }}
                .btn {{ display: inline-block; background-color: #2e7d32; color: white; padding: 12px 20px; text-decoration: none; border-radius: 8px; font-weight: bold; border: none; cursor: pointer; width: 100%; box-sizing: border-box; font-size: 1rem; }}
                .btn:hover {{ background-color: #1b5e20; }}
                .btn-cam {{ background-color: #2e7d32; display: block; text-align: center; margin-bottom: 15px; width: 100%; padding: 12px; font-weight: bold; border-radius: 8px; color: white; cursor: pointer; }}
                .btn-csv {{ background-color: #0288d1; margin-top: 10px; display: block; text-align: center; width: 100%; box-sizing: border-box; }}
                .history-card {{ margin-top: 30px; text-align: left; background: #fafafa; border: 1px solid #e0e0e0; border-radius: 10px; padding: 15px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th {{ text-align: left; padding: 8px; border-bottom: 2px solid #2e7d32; font-size: 0.85rem; color: #2e7d32; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🌱 Soil Diagnostic Scanner</h2>
                    <p style="color: #666; font-size: 0.9rem;">Computer Vision Soil Analysis & Crop Advisor</p>
                </div>

                <form id="scan-form" action="/predict" method="post" enctype="multipart/form-data" class="upload-box">
                    <input type="file" id="soil-file" name="file" accept="image/*" capture="environment" required style="display: none;" onchange="document.getElementById('scan-form').submit()">
                    
                    <button type="button" class="btn btn-cam" onclick="document.getElementById('soil-file').click()">📸 Capture / Select Soil</button>
                    
                    <button type="submit" class="btn">🔬 Run Diagnostic Scan</button>
                </form>

                <div class="history-card">
                    <h3 style="margin-top:0; color: #2c3e50; font-size: 1.1rem;">📊 Recent Scan History</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Type</th>
                                <th>Texture</th>
                                <th>Moisture</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history_rows}
                        </tbody>
                    </table>
                    <a href="/export-csv" class="btn btn-csv">📥 Download Full Scan History (CSV)</a>
                </div>
            </div>
        </body>
        </html>
    """)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    
    classification, topography, moisture, nutrients, crops, image_base64 = analyze_soil_opencv(contents)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("soil_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scans (timestamp, classification, topography, moisture, image_base64) VALUES (?, ?, ?, ?, ?)",
        (timestamp, classification, topography, moisture, image_base64)
    )
    conn.commit()
    conn.close()

    return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Soil Diagnostic Report</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 20px; }}
                .container {{ max-width: 550px; margin: 0 auto; background: #fff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center; }}
                .header {{ color: #2e7d32; margin-bottom: 20px; }}
                .soil-preview {{ width: 100%; max-width: 300px; height: auto; border-radius: 10px; margin: 15px auto; display: block; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
                .report-card {{ background: #fafafa; border: 1px solid #e0e0e0; border-radius: 10px; padding: 18px; margin-top: 15px; text-align: left; }}
                .metric {{ margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #eee; padding-bottom: 8px; }}
                .label {{ font-weight: 600; color: #555; }}
                .badge {{ background: #e8f5e9; color: #2e7d32; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 0.9rem; }}
                .badge-moisture {{ background: #e3f2fd; color: #1565c0; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 0.9rem; }}
                .info-box {{ background: #f9fbe7; border-left: 4px solid #c0ca33; padding: 12px; border-radius: 4px; margin-top: 15px; font-size: 0.95rem; color: #333; }}
                .crop-box {{ background: #eef9f1; border-left: 4px solid #2e7d32; padding: 12px; border-radius: 4px; margin-top: 10px; font-size: 0.95rem; color: #333; }}
                .btn {{ display: block; text-align: center; background-color: #2e7d32; color: white; padding: 12px; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 20px; }}
                .btn:hover {{ background-color: #1b5e20; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🌱 Soil Diagnostic Scanner</h2>
                    <p style="color: #666; font-size: 0.9rem;">Computer Vision Soil Analysis & Crop Advisor</p>
                </div>

                <img src="data:image/jpeg;base64,{image_base64}" alt="Soil Sample Preview" class="soil-preview">

                <div class="report-card">
                    <h3 style="margin-top:0; color: #2c3e50;">Diagnostic Report</h3>
                    <p style="font-size: 0.85rem; color: #888;">Scanned on: {timestamp} | File: {file.filename}</p>
                    
                    <div class="metric">
                        <span class="label">Soil Classification:</span>
                        <span class="badge">{classification}</span>
                    </div>

                    <div class="metric">
                        <span class="label">Topography Texture:</span>
                        <span style="font-weight: 500; text-align: right; max-width: 60%;">{topography}</span>
                    </div>

                    <div class="metric">
                        <span class="label">Moisture Level:</span>
                        <span class="badge-moisture">{moisture}</span>
                    </div>

                    <div class="info-box">
                        <strong>🌱 Soil Health & Nutrients:</strong><br>
                        {nutrients}
                    </div>

                    <div class="crop-box">
                        <strong>🌽 Recommended Crops:</strong><br>
                        {crops}
                    </div>
                </div>

                <a href="/" class="btn">🔬 Run Another Scan</a>
            </div>
        </body>
        </html>
    """)

@app.get("/export-csv")
def export_csv():
    conn = sqlite3.connect("soil_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, classification, topography, moisture FROM scans ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Timestamp", "Classification", "Topography", "Moisture"])
    writer.writerows(rows)

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=soil_scan_history.csv"}
    )