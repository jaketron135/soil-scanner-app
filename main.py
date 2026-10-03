import os
import sqlite3
from datetime import datetime
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

DB_FILE = "soil_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            soil_type TEXT,
            moisture TEXT,
            topography TEXT,
            edge_density REAL,
            brightness REAL,
            saturation REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def analyze_soil_image(image_bytes: bytes) -> dict:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not decode image")

    img = cv2.resize(img, (300, 300))

    # 1. Color & Saturation Analysis in HSV Space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    avg_saturation = np.mean(hsv[:, :, 1])
    avg_value = np.mean(hsv[:, :, 2])

    # Calibrated Moisture Ranges
    if avg_value < 85:
        moisture_status = "Wet / Very Moist"
    elif avg_value < 135:
        moisture_status = "Moderate Moisture"
    else:
        moisture_status = "Dry Surface"

    # 2. Texture Analysis: Pre-blur to reduce noise & micro-cracks
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Canny Edge Detection with smoothed image
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
    edge_density = np.sum(edges > 0) / (300 * 300)

    # Calibrated Edge Thresholds for Soil Classification
    if edge_density > 0.18:
        topography = "Coarse / Granular / Gravelly Surface"
        soil_type = "Sandy / Gravelly"
        nutrients = "High drainage, low organic retention; requires frequent organic composting."
        crops = ["Carrots", "Radish", "Potatoes", "Peanuts"]
    elif edge_density > 0.05:
        topography = "Clumpy / Aggregated / Compacted Texture"
        soil_type = "Loam / Clay Loam"
        nutrients = "Balanced organic matter and strong NPK nutrient retention capacity."
        crops = ["Tomatoes", "Peppers", "Maize", "Leafy Greens"]
    else:
        topography = "Smooth / Fine / Dense Surface"
        soil_type = "Clay / Heavy Clay"
        nutrients = "Rich in minerals (K, Ca), but prone to surface compaction and waterlogging."
        crops = ["Rice", "Cabbage", "Broccoli", "Squash", "Beans"]

    return {
        "soil_type": soil_type,
        "topography": topography,
        "moisture": moisture_status,
        "nutrients": nutrients,
        "crops": crops,
        "cv_metrics": {
            "edge_density": round(float(edge_density), 4),
            "avg_brightness": round(float(avg_value), 2),
            "avg_saturation": round(float(avg_saturation), 2)
        }
    }


def save_scan_to_history(results: dict):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scan_history (timestamp, soil_type, moisture, topography, edge_density, brightness, saturation)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        results["soil_type"],
        results["moisture"],
        results["topography"],
        results["cv_metrics"]["edge_density"],
        results["cv_metrics"]["avg_brightness"],
        results["cv_metrics"]["avg_saturation"]
    ))
    conn.commit()
    conn.close()


@app.get("/", response_class=HTMLResponse)
async def read_index():
    if os.path.exists("static/index.html"):
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    elif os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>index.html not found</h1>")


@app.post("/api/v1/diagnose")
async def diagnose_soil(file: UploadFile = File(...)):
    image_bytes = await file.read()
    results = analyze_soil_image(image_bytes)
    save_scan_to_history(results)

    return {
        "status": "success",
        "soil_type": results["soil_type"],
        "topography": results["topography"],
        "moisture": results["moisture"],
        "nutrients": results["nutrients"],
        "crops": results["crops"],
        "cv_metrics": results["cv_metrics"]
    }


@app.get("/api/v1/history")
async def get_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, soil_type, moisture, topography, edge_density, brightness FROM scan_history ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    history = [
        {
            "timestamp": row[0],
            "soil_type": row[1],
            "moisture": row[2],
            "topography": row[3],
            "edge_density": row[4],
            "brightness": row[5]
        }
        for row in rows
    ]
    return {"history": history}