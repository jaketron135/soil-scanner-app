import cv2
import numpy as np

def analyze_soil_image(image_bytes: bytes) -> dict:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Could not decode image")

    img = cv2.resize(img, (300, 300))
    
    # 1. Color Analysis in HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    avg_saturation = np.mean(hsv[:, :, 1])
    avg_value = np.mean(hsv[:, :, 2])
    
    if avg_value < 90:
        moisture_status = "Moist / Wet"
    elif avg_value < 140:
        moisture_status = "Moderate Moisture"
    else:
        moisture_status = "Dry / Low Moisture"

    # 2. Texture Analysis via Canny Edge Detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)
    edge_density = np.sum(edges > 0) / (300 * 300)
    
    if edge_density > 0.12:
        topography = "Coarse / Granular Surface"
        soil_type = "Sandy / Gravelly"
        nutrients = "High drainage, low organic retention; requires frequent composting."
        crops = ["Carrots", "Radish", "Potatoes", "Peanuts"]
    elif edge_density > 0.06:
        topography = "Rough / Clumpy / Aggregated"
        soil_type = "Loamy"
        nutrients = "Balanced organic matter and strong NPK nutrient retention."
        crops = ["Tomatoes", "Peppers", "Maize", "Leafy Greens"]
    else:
        topography = "Smooth / Fine / Dense Surface"
        soil_type = "Clay"
        nutrients = "Rich in minerals (K, Ca), but prone to compaction and waterlogging."
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