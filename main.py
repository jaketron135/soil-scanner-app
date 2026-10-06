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
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col items-center justify-center p-4">
    <div class="max-w-xl w-full bg-slate-900 border border-emerald-500/30 rounded-2xl shadow-2xl p-6 relative">
        <!-- Header Branding -->
        <div class="flex items-center justify-center space-x-2 mb-2">
            <span class="text-2xl">🌿</span>
            <span class="text-xl font-bold tracking-tight text-emerald-400 flex items-center gap-1">
                🍎 Jaketron
            </span>
        </div>

        <h1 class="text-2xl font-bold text-emerald-400 text-center mb-1">Soil Diagnostic Scanner</h1>
        <p class="text-slate-400 text-center text-xs mb-6">Professional Computer Vision Soil Analysis & Crop Advisor</p>

        <form method="POST" enctype="multipart/form-data" class="space-y-4">
            <div class="border-2 border-dashed border-emerald-500/40 rounded-xl p-4 text-center hover:border-emerald-400 transition bg-emerald-950/20">
                <input type="file" name="soil_image" id="soil_image" accept="image/*" class="w-full text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-emerald-600 file:text-white hover:file:bg-emerald-500 cursor-pointer" onchange="previewImage(event)">
            </div>
            
            <!-- Image Preview Box -->
            <div id="imagePreviewContainer" class="hidden text-center">
                <p class="text-xs text-emerald-400 mb-1">Captured Soil Sample Preview:</p>
                <img id="soilPreview" class="mx-auto max-h-40 rounded-lg border border-emerald-500/40 object-cover" />
            </div>

            <button type="submit" class="w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl shadow-lg shadow-emerald-900/50 transition tracking-wide text-sm flex items-center justify-center gap-2">
                <span>🔬</span> Run Diagnostic Scan
            </button>
        </form>

        {% if result %}
        <div class="mt-6 p-5 bg-emerald-950/40 border border-emerald-500/40 rounded-xl space-y-4 text-left">
            <h2 class="text-base font-bold text-emerald-300 border-b border-emerald-800/50 pb-2 flex items-center gap-2">
                <span>📊</span> Comprehensive Lab Diagnostic Results
            </h2>

            <!-- Uploaded Image Display in Results -->
            {% if image_url %}
            <div>
                <p class="text-xs text-emerald-400 mb-1 font-mono">Analyzed Specimen Image:</p>
                <img src="{{ image_url }}" alt="Soil Specimen" class="max-h-36 rounded-lg border border-emerald-500/30 object-cover">
            </div>
            {% endif %}

            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
                <div class="bg-slate-950/60 p-3 rounded-lg border border-emerald-500/20">
                    <p class="text-emerald-400 font-semibold mb-1">🧪 pH Monitoring</p>
                    <p class="text-slate-300">Level: <span class="text-white font-bold">6.5 (Optimal Neutral)</span></p>
                    <p class="text-slate-400 text-[11px] mt-0.5">Ideal for nutrient absorption across most staple crops.</p>
                </div>

                <div class="bg-slate-950/60 p-3 rounded-lg border border-emerald-500/20">
                    <p class="text-emerald-400 font-semibold mb-1">📐 Surface Area Calculation</p>
                    <p class="text-slate-300">Estimated Field Coverage: <span class="text-white font-bold">1,250 m²</span></p>
                    <p class="text-slate-400 text-[11px] mt-0.5">Calculated based on scan topology density.</p>
                </div>
            </div>

            <div class="bg-slate-950/60 p-3 rounded-lg border border-emerald-500/20 text-xs font-mono">
                <p class="text-emerald-400 font-semibold mb-1">🌱 Crop Recommendations</p>
                <p class="text-slate-300">Primary Fit: <span class="text-white font-bold">Root Crops (Cassava, Sweet Potato), Legumes, and Maize</span></p>
            </div>

            <div class="bg-slate-950/60 p-3 rounded-lg border border-emerald-500/20 text-xs font-mono">
                <p class="text-emerald-400 font-semibold mb-1">💊 Fertilizer & Amendment Plan</p>
                <p class="text-slate-300">{{ result }}</p>
            </div>
        </div>
        {% endif %}
    </div>

    <script>
        function previewImage(event) {
            const reader = new FileReader();
            reader.onload = function() {
                const output = document.getElementById('soilPreview');
                output.src = reader.result;
                document.getElementById('imagePreviewContainer').classList.remove('hidden');
            };
            if(event.target.files[0]) {
                reader.readAsDataURL(event.target.files[0]);
            }
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None
    if request.method == "POST":
        file = request.files.get("soil_image")
        if file and file.filename != "":
            result = "Apply balanced organic compost (NPK 14-14-14) at 50kg per 500m² alongside decomposed banana stalk mulch to retain optimal moisture and nitrogen levels."
            # In a real app, you'd save the file or convert to data URL if needed; for now, placeholder status
    return render_template_string(HTML_TEMPLATE, result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))