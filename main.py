<!-- Add this section to your report container -->
<div class="weather-box" style="background: #f4f6f8; padding: 15px; border-radius: 8px; margin-top: 15px;">
    <h4>📍 Local Weather & Climate Context</h4>
    <p id="weather-status">Detecting local weather and soil micro-climate...</p>
</div>

<script>
// Automatically fetch browser geolocation and query local weather
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        
        // Fetch free real-time weather data from Open-Meteo
        fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,precipitation`)
            .then(response => response.json())
            .then(data => {
                if(data.current) {
                    const temp = data.current.temperature_2m;
                    const humidity = data.current.relative_humidity_2m;
                    const precip = data.current.precipitation;
                    
                    document.getElementById('weather-status').innerHTML = `
                        <b>Temperature:</b> ${temp}°C | 
                        <b>Air Humidity:</b> ${humidity}% | 
                        <b>Current Precipitation:</b> ${precip} mm<br>
                        <span style="font-size: 0.9em; color: #555;"><i>Adjusting watering and evaporation recommendations based on local climate.</i></span>
                    `;
                }
            })
            .catch(err => {
                document.getElementById('weather-status').innerText = "Unable to fetch live weather data.";
            });
    }, error => {
        document.getElementById('weather-status').innerText = "Location access denied. Enable GPS for localized agronomic advice.";
    });
} else {
    document.getElementById('weather-status').innerText = "Geolocation is not supported by your browser.";
}
</script>