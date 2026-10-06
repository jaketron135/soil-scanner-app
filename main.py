<style>
  /* Professional Laboratory Ambient Container */
  .scanner-viewport {
    position: relative;
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
    background: #0b0f0d;
  }

  /* Cinematic Botanical Aperture Shutter Effect */
  .botanical-shutter {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle, rgba(16, 185, 129, 0.15) 0%, rgba(6, 78, 59, 0.95) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 50;
    transition: transform 1.2s cubic-bezier(0.77, 0, 0.175, 1), opacity 0.8s ease-in-out;
  }

  .shutter-hidden {
    transform: scale(1.2);
    opacity: 0;
    pointer-events: none;
  }

  /* Biometric High-Precision Scanning Laser Beam */
  .scan-laser {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, transparent, #34d399, #10b981, #34d399, transparent);
    box-shadow: 0 0 20px #10b981, 0 0 40px #34d399;
    animation: laserScan 2.2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    z-index: 40;
  }

  @keyframes laserScan {
    0% { top: 0%; opacity: 0; }
    15% { opacity: 1; }
    85% { opacity: 1; }
    100% { top: 100%; opacity: 0; }
  }

  /* Holographic HUD Grid Overlay */
  .hud-grid {
    position: absolute;
    inset: 0;
    background-image: 
      linear-gradient(rgba(16, 185, 129, 0.05) 1px, transparent 1px),
      linear-gradient(90deg, rgba(16, 185, 129, 0.05) 1px, transparent 1px);
    background-size: 20px 20px;
    z-index: 30;
    pointer-events: none;
  }
</style>

<script>
  function triggerProfessionalScan() {
    const shutter = document.getElementById('botanicalShutter');
    const resultsPanel = document.getElementById('resultsPanel');
    
    // Play cinematic shutter open & laser sequence
    shutter.classList.remove('shutter-hidden');
    
    setTimeout(() => {
      shutter.classList.add('shutter-hidden');
      if(resultsPanel) {
        resultsPanel.style.display = 'block';
        resultsPanel.scrollIntoView({ behavior: 'smooth' });
      }
    }, 2200); // Matches professional scan frequency
  }
</script>