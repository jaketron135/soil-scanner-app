import sqlite3
import csv
import io
import datetime
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize database table if it doesn't exist
def init_db():
    conn = sqlite3.connect("soil_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            classification TEXT,
            topography TEXT,
            moisture TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 1. Root route to serve main page
@app.get("/")
def read_root():
    return FileResponse("static/index.html")

# 2. Predict endpoint for image upload analysis
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read image contents
    contents = await file.read()
    
    # Simple mockup analysis (replace with your OpenCV/ML logic as needed)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    classification = "Loam Soil"
    topography = "Flat / Gentle Slope"
    moisture = "22.5% (Optimal)"

    # Save result into SQLite database
    conn = sqlite3.connect("soil_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scans (timestamp, classification, topography, moisture) VALUES (?, ?, ?, ?)",
        (timestamp, classification, topography, moisture)
    )
    conn.commit()
    conn.close()

    # Return structured result to browser
    return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Scan Results</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f4f7f6; padding: 20px; }}
                .card {{ max-width: 500px; margin: 0 auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                h2 {{ color: #27ae60; }}
                .btn {{ display: inline-block; background: #3498db; color: #fff; padding: 10px 15px; text-decoration: none; border-radius: 5px; margin-top: 15px; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>✅ Soil Analysis Complete</h2>
                <p><strong>File Name:</strong> {file.filename}</p>
                <p><strong>Timestamp:</strong> {timestamp}</p>
                <p><strong>Classification:</strong> {classification}</p>
                <p><strong>Topography:</strong> {topography}</p>
                <p><strong>Moisture Level:</strong> {moisture}</p>
                <hr>
                <a href="/" class="btn">⬅️ Perform Another Scan</a>
            </div>
        </body>
        </html>
    """)

# 3. Export CSV endpoint
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