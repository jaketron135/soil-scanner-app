@app.route("/manifest.json")
def manifest():
    return jsonify({
        "name": "Soil Diagnostic Scanner - Jaketron",
        "short_name": "Soil Scanner",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#059669",
        "description": "Professional computer vision soil analysis & crop advisor tool.",
        "icons": [
            {
                "src": "data:image/jpeg;base64," + APPLE_B64,
                "sizes": "192x192 512x512",
                "type": "image/jpeg",
                "purpose": "any maskable"
            }
        ]
    })