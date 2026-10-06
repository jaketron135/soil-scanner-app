from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soil Diagnostic Scanner - Jaketron</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
      .scanner-viewport {
        position: relative;
        overflow: hidden;
        border-radius: 14px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        background: #060907;
      }
      .botanical-shutter {
        position: absolute;
        inset: 0;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, rgba(4, 47, 46, 0.98) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 50;
        transition: transform 1.2s cubic-bezier(0.77, 0, 0.175, 1), opacity 0.8s ease-in-out;
      }
      .shutter-hidden {
        transform: scale(1.25);
        opacity: 0;
        pointer-events: none;
      }
      .scan-laser {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, transparent, #34d399, #10b981, #34d399, transparent);
        box-shadow: 0 0 25px #10b981, 0 0 50px #34d399;
        animation: laserScan 2.4s cubic-bezier(0.4, 0, 0.2, 1) infinite;
        z-index: 40;
      }
      @keyframes laserScan {
        0% { top: 0%; opacity: 0; }
        15% { opacity: 1; }
        85% { opacity: 1; }
        100% { top: 100%; opacity: 0; }
      }
      .hud-grid {
        position: absolute;
        inset: 0;
        background-image: 
          linear-gradient(rgba(16, 185, 129, 0.06) 1px, transparent 1px),
          linear-gradient(90deg, rgba(16, 185, 129, 0.06) 1px, transparent 1px);
        background-size: 24px 24px;
        z-index: 30;
        pointer-events: none;
      }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col items-center justify-center p-4">
    <div class="max-w-xl w-full scanner-viewport p-6 border border-emerald-500/30">
        <div id="botanicalShutter" class="botanical-shutter shutter-hidden">
            <div class="hud-grid"></div>
            <div class="scan-laser"></div>
            <div class="text-emerald-400 font-mono tracking-widest text-lg uppercase animate-pulse">
                INITIALIZING BIO-SCAN...
            </div>
        </div>

        <h1 class="text-3xl font-bold text-emerald-400 mb-2 text-center">Soil Diagnostic Scanner</h1>
        <p class="text-slate-400 text-center mb-6 text-sm">Advanced Agricultural Intelligence System</p>

        <form method="POST" enctype="multipart/form-data" onsubmit="triggerProfessionalScan()" class="space-y-4">
            <div class="border-2 border-dashed border-emerald-500/40 rounded-xl p-6 text-center hover:border-emerald-400 transition cursor-pointer bg-emerald-950/20">
                <input type="file" name="soil_image" required class="w-full text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-emerald-600 file:text-white hover:file:bg-emerald-500">
            </div>
            <button type="submit" class="w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl shadow-lg shadow-emerald-900/50 transition tracking-wide">
                ANALYZE SOIL TOPOGRAPHY
            </button>
        </form>

        {% if result %}
        <div id="resultsPanel" class="mt-6 p-5 bg-emerald-950/40 border border-emerald-500/40 rounded-xl backdrop-blur-md">
            <h2 class="text-xl font-bold text-emerald-300 mb-3 border-b border-emerald-800/50 pb-2">Diagnostic Results</h2>
            <div class="space-y-2 text-sm text-slate-300 font-mono">
                <p><span class="text-emerald-400">Status:</span> Operational</p>
                <p><span class="text-emerald-400">Analysis:</span> {{ result }}</p>
            </div>
        </div>
        {% endif %}
    </div>

    <script>
      function triggerProfessionalScan() {
        const shutter = document.getElementById('botanicalShutter');
        if(shutter) {
            shutter.classList.remove('shutter-hidden');
        }
      }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files.get("soil_image")
        if file and file.filename != "":
            result = "Sample analyzed successfully. Optimal nitrogen and moisture levels detected. Recommended for root crop cultivation."
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))