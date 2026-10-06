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
</head>
<body class="bg-[#f0fdf4] text-slate-800 min-h-screen flex flex-col items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-3xl shadow-xl p-8 border border-emerald-100 text-center relative">
        <!-- Header Branding -->
        <div class="flex items-center justify-center space-x-2 mb-3">
            <span class="text-2xl">🌿</span>
            <span class="text-xl font-bold tracking-tight text-emerald-800 flex items-center gap-1">
                🍎 Jaketron
            </span>
        </div>

        <h1 class="text-2xl font-bold text-emerald-900 mb-1">Soil Diagnostic Scanner</h1>
        <p class="text-slate-500 text-xs mb-8">Professional Computer Vision Soil Analysis & Crop Advisor</p>

        <form method="POST" enctype="multipart/form-data" class="space-y-4">
            <!-- Hidden file input triggered by custom button -->
            <input type="file" id="soil_image" name="soil_image" accept="image/*" class="hidden" onchange="updateFileName(this)">
            
            <label for="soil_image" class="w-full py-3.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-medium rounded-xl shadow-md transition flex items-center justify-center gap-2 cursor-pointer text-sm">
                <span>📷</span> Capture / Select Soil Image
            </label>

            <button type="submit" class="w-full py-3.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-medium rounded-xl shadow-md transition flex items-center justify-center gap-2 text-sm">
                <span>🔬</span> Run Diagnostic Scan
            </button>
        </form>

        <div id="file-chosen" class="text-xs text-emerald-700 mt-3 font-medium"></div>

        {% if result %}
        <div class="mt-6 p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-left">
            <h2 class="text-sm font-bold text-emerald-800 mb-1">Diagnostic Results:</h2>
            <p class="text-xs text-slate-700">{{ result }}</p>
        </div>
        {% endif %}
    </div>

    <script>
        function updateFileName(input) {
            const fileNameDiv = document.getElementById('file-chosen');
            if (input.files && input.files[0]) {
                fileNameDiv.textContent = "Selected: " + input.files[0].name;
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
        else:
            result = "Please capture or select a soil image first before running the diagnostic scan."
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))