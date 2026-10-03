import sqlite3
import csv
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

# 1. Initialize FastAPI FIRST
app = FastAPI()

# 2. Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. Define routes AFTER app is created
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