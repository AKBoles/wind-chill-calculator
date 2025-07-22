# Weather Utility Pro 🌤️

A comprehensive offline weather utility app that provides detailed weather calculations, safety assessments, and practical recommendations without requiring an internet connection.

## Features ✨

### Main Weather Calculator
- **Wind Chill Calculator** - Accurate wind chill calculations with safety warnings
- **Heat Index Calculator** - "Feels like" temperature accounting for humidity
- **Dew Point Calculator** - Humidity condensation point calculations
- **Apparent Temperature** - Australian apparent temperature model
- **Pressure Altitude** - Aviation altitude calculations from barometric pressure
- **UV Index Estimator** - Solar UV risk estimation based on time and season

### Safety Features 🚨
- **Cold Weather Alerts** - Frostbite risk assessments with time estimates
- **Heat Safety Warnings** - Heat exhaustion and heat stroke risk levels
- **UV Protection Guidance** - Sun safety recommendations by UV index
- **Detailed Clothing Recommendations** - Weather-appropriate clothing advice

### Additional Tools 🛠️
- **Temperature Converter** - Fahrenheit, Celsius, Kelvin, Rankine
- **Wind Speed Converter** - mph, km/h, m/s, knots, ft/s
- **Pressure Converter** - mb, hPa, inHg, mmHg, psi, atm
- **Visibility Categories** - Fog and visibility safety analysis
- **Beaufort Wind Scale** - Traditional wind scale with descriptions
- **Cloud Base Estimator** - Estimated cloud height calculations

### Offline Capabilities 📱
- **Progressive Web App (PWA)** - Install on any device
- **Complete Offline Functionality** - No internet required
- **Service Worker Caching** - Fast loading and reliability
- **Responsive Design** - Works on desktop, tablet, and mobile

### Units Support 🔄
- **Imperial & Metric** - Seamless switching between unit systems
- **Real-time Conversion** - Automatic unit updates throughout the interface

## Installation & Usage 🚀

### Local Development
```bash
# Install dependencies
pip install flask

# Run the application
python app.py

# Access at http://localhost:5000
```

### Production Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Deploy with gunicorn (included in requirements)
gunicorn app:app
```

### PWA Installation
- Visit the app in a modern web browser
- Look for "Install" or "Add to Home Screen" option
- Enjoy full offline functionality

## Weather Calculations 📊

### Wind Chill Formula
Uses the official National Weather Service formula:
```
WC = 35.74 + 0.6215T - 35.75(V^0.16) + 0.4275T(V^0.16)
```

### Heat Index Formula
Implements the full National Weather Service heat index calculation with adjustments for extreme conditions.

### Dew Point Calculation
Uses the Magnus formula for accurate dew point determination across all temperature ranges.

### UV Index Estimation
Approximates UV index based on solar elevation angle, time of day, and seasonal variation.

## Safety Standards 🛡️

All safety recommendations are based on:
- National Weather Service guidelines
- World Health Organization UV safety standards
- Aviation weather standards
- International meteorological practices

## Browser Support 🌐

- Chrome/Edge 60+
- Firefox 55+
- Safari 11+
- Mobile browsers with PWA support

## Features for Emergency Use 🆘

Perfect for:
- **Power Outages** - Works completely offline
- **Remote Locations** - No internet required
- **Emergency Preparedness** - Critical weather calculations
- **Aviation** - Pressure altitude and wind calculations
- **Outdoor Activities** - UV and safety assessments
- **HVAC/Construction** - Dew point and comfort calculations

## Technical Details ⚙️

- **Backend**: Python Flask
- **Frontend**: Vanilla JavaScript with modern CSS
- **Caching**: Service Worker for offline functionality
- **Storage**: Browser local storage for preferences
- **Performance**: Optimized for instant calculations

## License 📄

This project is open source. See the LICENSE file for details.

## Contributing 🤝

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

*Weather Utility Pro - Your comprehensive offline weather companion*