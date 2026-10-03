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