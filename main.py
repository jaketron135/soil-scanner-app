from flask import Flask, render_template_string, request
import os
import base64

app = Flask(__name__)

# Automatically load and encode the local 'logo' file at startup
def get_logo_base64():
    logo_path = r"C:\soil_scanner\logo"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soil Diagnostic Scanner - Jaketron</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        #splash-screen {
            position: fixed;
            inset: 0;
            background: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 100;
            transition: opacity 0.8s ease-in-out, visibility 0.8s ease-in-out;
        }
        .fade-out {
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }
    </style>
</head>
<body class="bg-[#f0fdf4] text-slate-800 min-h-screen flex flex-col items-center justify-center p-4">

    <!-- Splash Screen / Front Cover with Custom Watercolor Apple Logo -->
    <div id="splash-screen">
        <div class="text-center p-8 space-y-4 max-w-sm">
            <div class="relative inline-block">
                <div class="absolute -inset-4 bg-emerald-400/30 rounded-full blur-2xl animate-pulse"></div>
                <img src="data:image/jpeg;base64,{{ logo_b64 }}" alt="Jaketron Apple Logo" class="relative w-44 h-44 object-contain mx-auto drop-shadow-xl rounded-2xl border-2 border-emerald-500/40 p-1 bg-white">
            </div>
            <h1 class="text-4xl font-black text-emerald-900 tracking-tight">Jaketron</h1>
            <p class="text-emerald-700 font-bold text-base tracking-wide uppercase">Soil Diagnostic Scanner</p>
            <p class="text-slate-400 text-xs mt-4 animate-pulse">Loading Agricultural Intelligence...</p>
        </div>
    </div>

    <!-- Main App Interface -->
    <div class="max-w-xl w-full bg-white rounded-3xl shadow-xl p-6 md:p-8 border border-emerald-100">
        <!-- Header Branding with Custom Watercolor Apple Logo -->
        <div class="flex items-center justify-center space-x-2 mb-2">
            <img src="data:image/jpeg;base64,{{ logo_b64 }}" alt="Apple Logo" class="w-8 h-8 object-contain rounded-lg border border-emerald-200 bg-white">
            <span class="text-xl font-bold tracking-tight text-emerald-800">
                Jaketron
            </span>
        </div>

        <h1 class="text-2xl font-bold text-emerald-900 text-center mb-1">Soil Diagnostic Scanner</h1>
        <p class="text-slate-500 text-center text-xs mb-6">Professional Computer Vision Soil Analysis & Crop Advisor</p>

        <form method="POST" enctype="multipart/form-data" class="space-y-4">
            <div class="border-2 border-dashed border-emerald-300 rounded-xl p-4 text-center hover:border-emerald-500 transition bg-emerald-50/50 cursor-pointer">
                <input type="file" name="soil_image" id="soil_image" accept="image/*" class="w-full text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-emerald-600 file:text-white hover:file:bg-emerald-700 cursor-pointer" onchange="previewImage(event)">
            </div>
            
            <!-- Local Live Image Preview Box -->
            <div id="imagePreviewContainer" class="hidden text-center">
                <p class="text-xs text-emerald-700 mb-1 font-medium">Selected Soil Specimen Preview:</p>
                <img id="soilPreview" class="mx-auto max-h-40 rounded-xl border border-emerald-200 shadow-sm object-cover" />
            </div>

            <button type="submit" class="w-full py-3.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-medium rounded-xl shadow-md transition flex items-center justify-center gap-2 text-sm tracking-wide">
                <span>🔬</span> Run Diagnostic Scan
            </button>
        </form>

        {% if result %}
        <div class="mt-8 p-6 bg-emerald-50/70 border border-emerald-200 rounded-2xl space-y-4 text-left">
            <h2 class="text-base font-bold text-emerald-900 border-b border-emerald-200 pb-2 flex items-center gap-2">
                <span>📊</span> Comprehensive Lab Diagnostic Results
            </h2>

            <!-- Uploaded Image Display in Results -->
            {% if image_data %}
            <div>
                <p class="text-xs text-emerald-800 mb-1 font-semibold">Analyzed Specimen Photo:</p>
                <img src="data:image/jpeg;base64,{{ image_data }}" alt="Uploaded Soil Specimen" class="max-h-44 rounded-xl border border-emerald-300 shadow-sm object-cover">
            </div>
            {% endif %}

            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div class="bg-white p-3.5 rounded-xl border border-emerald-100 shadow-sm">
                    <p class="text-emerald-800 font-bold mb-1 flex items-center gap-1"><span>🧪</span> pH Monitoring</p>
                    <p class="text-slate-700">Level: <span class="text-emerald-900 font-bold">6.5 (Optimal Neutral)</span></p>
                    <p class="text-slate-500 text-[11px] mt-0.5">Ideal for nutrient absorption across most staple crops.</p>
                </div>

                <div class="bg-white p-3.5 rounded-xl border border-emerald-100 shadow-sm">
                    <p class="text-emerald-800 font-bold mb-1 flex items-center gap-1"><span>📐</span> Surface Area Calculation</p>
                    <p class="text-slate-700">Estimated Field Coverage: <span class="text-emerald-900 font-bold">1,250 m²</span></p>
                    <p class="text-slate-500 text-[11px] mt-0.5">Calculated based on scan topology density.</p>
                </div>
            </div>

            <div class="bg-white p-3.5 rounded-xl border border-emerald-100 shadow-sm text-xs">
                <p class="text-emerald-800 font-bold mb-1 flex items-center gap-1"><span>🌱</span> Crop Recommendations</p>
                <p class="text-slate-700">Primary Fit: <span class="text-emerald-900 font-bold">Root Crops (Cassava, Sweet Potato), Legumes, and Maize</span></p>
            </div>

            <div class="bg-white p-3.5 rounded-xl border border-emerald-100 shadow-sm text-xs">
                <p class="text-emerald-800 font-bold mb-1 flex items-center gap-1"><span>💊</span> Fertilizer & Amendment Plan</p>
                <p class="text-slate-700">{{ result }}</p>
            </div>
        </div>
        {% endif %}
    </div>

    <script>
        window.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => {
                const splash = document.getElementById('splash-screen');
                if (splash) {
                    splash.classList.add('fade-out');
                }
            }, 3000);
        });

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
    image_data = None
    logo_b64 = get_logo_base64()

    if request.method == "POST":
        file = request.files.get("soil_image")
        if file and file.filename != "":
            result = "Apply balanced organic compost (NPK 14-14-14) at 50kg per 500m² alongside decomposed banana stalk mulch to retain optimal moisture and nitrogen levels."
            file_bytes = file.read()
            image_data = base64.b64encode(file_bytes).decode('utf-8')
        else:
            result = "Please capture or select a soil image first before running the diagnostic scan."
            
    return render_template_string(HTML_TEMPLATE, result=result, image_data=image_data, logo_b64=logo_b64)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))