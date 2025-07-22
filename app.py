from flask import Flask, render_template, request, jsonify, send_from_directory
import math
from datetime import datetime, timedelta

# Create Flask app with explicit static folder configuration
app = Flask(__name__, static_folder='static', static_url_path='/static')

class WeatherCalculator:
    """Comprehensive weather calculation utilities that work offline"""
    
    @staticmethod
    def wind_chill(temp_f, wind_mph):
        """Calculate wind chill in Fahrenheit"""
        if temp_f > 50 or wind_mph < 3:
            return temp_f
        return round(35.74 + (0.6215 * temp_f) - (35.75 * (wind_mph ** 0.16)) + (0.4275 * temp_f * (wind_mph ** 0.16)), 1)
    
    @staticmethod
    def heat_index(temp_f, humidity):
        """Calculate heat index (feels like temperature) in Fahrenheit"""
        if temp_f < 80:
            return temp_f
        
        T = temp_f
        RH = humidity
        
        # Simplified heat index formula for temperatures >= 80°F
        if temp_f >= 80:
            # Rothfusz regression (simplified version)
            HI = -42.379 + 2.04901523*T + 10.14333127*RH - 0.22475541*T*RH
            HI += -0.00683783*T*T - 0.05481717*RH*RH + 0.00122874*T*T*RH
            HI += 0.00085282*T*RH*RH - 0.00000199*T*T*RH*RH
            
            # For very high humidity, add correction
            if RH > 85 and T >= 80 and T <= 87:
                HI += ((RH-85)/10) * ((87-T)/5)
            
            # For very low humidity, subtract correction
            elif RH < 13 and T >= 80 and T <= 112:
                HI -= ((13-RH)/4) * math.sqrt((17-abs(T-95.))/17)
                
            return round(HI, 1)
        
        return temp_f
    
    @staticmethod
    def dew_point(temp_f, humidity):
        """Calculate dew point in Fahrenheit"""
        temp_c = (temp_f - 32) * 5/9
        a = 17.27
        b = 237.7
        alpha = ((a * temp_c) / (b + temp_c)) + math.log(humidity / 100.0)
        dew_point_c = (b * alpha) / (a - alpha)
        return round((dew_point_c * 9/5) + 32, 1)
    
    @staticmethod
    def apparent_temperature(temp_f, humidity, wind_mph):
        """Calculate apparent temperature (Australian apparent temperature)"""
        temp_c = (temp_f - 32) * 5/9
        wind_ms = wind_mph * 0.44704
        vapor_pressure = (humidity / 100) * 6.105 * math.exp((17.27 * temp_c) / (237.7 + temp_c))
        apparent_c = temp_c + 0.33 * vapor_pressure - 0.7 * wind_ms - 4.0
        return round((apparent_c * 9/5) + 32, 1)
    
    @staticmethod
    def pressure_altitude(pressure_mb):
        """Calculate pressure altitude in feet"""
        return round((1 - (pressure_mb / 1013.25) ** 0.190284) * 145366.45, 0)
    
    @staticmethod
    def uv_index_estimate(hour, month, latitude=40):
        """Estimate UV index based on time and location (approximate)"""
        if hour < 6 or hour > 20:
            return 0
        
        # Simple model based on solar elevation
        solar_declination = 23.45 * math.sin(math.radians(360 * (284 + month * 30) / 365))
        hour_angle = 15 * (hour - 12)
        elevation = math.asin(
            math.sin(math.radians(latitude)) * math.sin(math.radians(solar_declination)) +
            math.cos(math.radians(latitude)) * math.cos(math.radians(solar_declination)) * 
            math.cos(math.radians(hour_angle))
        )
        
        if elevation <= 0:
            return 0
        
        uv = 12 * math.sin(elevation) * (1 + 0.1 * (month - 6.5))
        return max(0, min(12, round(uv, 1)))

class WeatherSafety:
    """Weather safety assessments and recommendations"""
    
    @staticmethod
    def wind_chill_safety(wind_chill_f):
        if wind_chill_f > 32:
            return {"level": "safe", "warning": "No wind chill concerns", "time": None, "color": "green"}
        elif wind_chill_f > 16:
            return {"level": "caution", "warning": "Slight discomfort possible", "time": None, "color": "yellow"}
        elif wind_chill_f > 0:
            return {"level": "warning", "warning": "Frostbite possible with prolonged exposure", "time": "60+ minutes", "color": "orange"}
        elif wind_chill_f > -19:
            return {"level": "danger", "warning": "Frostbite warning - exposed skin can freeze", "time": "30 minutes", "color": "red"}
        elif wind_chill_f > -39:
            return {"level": "extreme", "warning": "Severe frostbite risk", "time": "10-15 minutes", "color": "darkred"}
        else:
            return {"level": "extreme", "warning": "Extreme frostbite risk - skin can freeze in minutes", "time": "Under 5 minutes", "color": "darkred"}
    
    @staticmethod
    def heat_index_safety(heat_index_f):
        if heat_index_f < 80:
            return {"level": "safe", "warning": "No heat concerns", "color": "green"}
        elif heat_index_f < 90:
            return {"level": "caution", "warning": "Fatigue possible with prolonged exposure", "color": "yellow"}
        elif heat_index_f < 105:
            return {"level": "warning", "warning": "Heat exhaustion and cramps possible", "color": "orange"}
        elif heat_index_f < 130:
            return {"level": "danger", "warning": "Heat exhaustion and cramps likely; heat stroke possible", "color": "red"}
        else:
            return {"level": "extreme", "warning": "Heat stroke highly likely with continued exposure", "color": "darkred"}
    
    @staticmethod
    def uv_safety(uv_index):
        if uv_index < 3:
            return {"level": "low", "warning": "Minimal protection needed", "color": "green"}
        elif uv_index < 6:
            return {"level": "moderate", "warning": "Protection required - seek shade during midday", "color": "yellow"}
        elif uv_index < 8:
            return {"level": "high", "warning": "Protection required - avoid sun 10am-4pm", "color": "orange"}
        elif uv_index < 11:
            return {"level": "very high", "warning": "Extra protection required - minimize outdoor exposure", "color": "red"}
        else:
            return {"level": "extreme", "warning": "Avoid outdoor exposure - stay indoors if possible", "color": "purple"}

class ClothingAdvisor:
    """Clothing and activity recommendations based on weather conditions"""
    
    @staticmethod
    def get_clothing_advice(temp_f, wind_chill_f, heat_index_f, humidity, wind_mph):
        if heat_index_f > 85:
            return {
                "primary": "🌞 Light, breathable clothing recommended",
                "details": [
                    "Light-colored, loose-fitting clothes",
                    "Hat and sunglasses",
                    "Sunscreen SPF 30+",
                    "Plenty of water"
                ]
            }
        elif wind_chill_f < 32:
            if wind_chill_f < -20:
                return {
                    "primary": "🧊 Extreme cold gear required",
                    "details": [
                        "Multiple layers including base layer",
                        "Insulated winter coat",
                        "Warm hat covering ears",
                        "Insulated gloves/mittens",
                        "Scarf or face mask",
                        "Warm, waterproof boots",
                        "Limit outdoor exposure"
                    ]
                }
            elif wind_chill_f < 0:
                return {
                    "primary": "❄️ Heavy winter clothing needed",
                    "details": [
                        "Winter coat or heavy jacket",
                        "Hat and gloves",
                        "Scarf recommended",
                        "Warm boots",
                        "Long pants"
                    ]
                }
            else:
                return {
                    "primary": "🧥 Jacket and warm accessories",
                    "details": [
                        "Jacket or coat",
                        "Long pants",
                        "Closed-toe shoes",
                        "Light gloves if windy"
                    ]
                }
        elif temp_f < 50:
            return {
                "primary": "🧥 Light jacket recommended",
                "details": [
                    "Light jacket or sweater",
                    "Long pants",
                    "Closed-toe shoes"
                ]
            }
        elif temp_f < 70:
            return {
                "primary": "👔 Comfortable layered clothing",
                "details": [
                    "Light layers",
                    "Long or short sleeves",
                    "Comfortable shoes"
                ]
            }
        else:
            return {
                "primary": "👕 Light, comfortable clothing",
                "details": [
                    "T-shirt or light shirt",
                    "Shorts or light pants",
                    "Comfortable shoes",
                    "Hat for sun protection"
                ]
            }

# ============================================================================
# ROUTES - Explicit and clean route definitions
# ============================================================================

@app.route("/", methods=["GET"])
def home():
    """Main weather calculator page - EXPLICIT GET route"""
    return render_template("index.html")

@app.route("/index")
@app.route("/index.html")
def index_alt():
    """Alternative routes to main page"""
    return render_template("index.html")

@app.route("/tools", methods=["GET"])
def tools():
    """Additional weather tools page"""
    return render_template("tools.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    """Weather calculation API endpoint"""
    try:
        data = request.get_json()
        
        # Get input values
        temperature = float(data.get('temperature', 70))
        humidity = float(data.get('humidity', 50))
        wind_speed = float(data.get('wind_speed', 5))
        pressure_mb = float(data.get('pressure', 1013.25))
        hour = int(data.get('hour', 12))
        month = int(data.get('month', 6))
        units = data.get('units', 'imperial')
        
        # Convert to Fahrenheit and mph for calculations if input is metric
        if units == 'metric':
            temp_f = (temperature * 9/5) + 32  # Convert Celsius to Fahrenheit
            wind_mph = wind_speed / 1.60934    # Convert km/h to mph
        else:
            temp_f = temperature
            wind_mph = wind_speed
        
        calc = WeatherCalculator()
        safety = WeatherSafety()
        advisor = ClothingAdvisor()
        
        # Calculate all weather metrics
        wind_chill_f = calc.wind_chill(temp_f, wind_mph)
        heat_index_f = calc.heat_index(temp_f, humidity)
        dew_point_f = calc.dew_point(temp_f, humidity)
        apparent_temp_f = calc.apparent_temperature(temp_f, humidity, wind_mph)
        uv_index = calc.uv_index_estimate(hour, month)
        
        # Prepare output values based on units
        if units == 'metric':
            output_temp = round((temp_f - 32) * 5/9, 1)
            output_wind_chill = round((wind_chill_f - 32) * 5/9, 1)
            output_heat_index = round((heat_index_f - 32) * 5/9, 1)
            output_dew_point = round((dew_point_f - 32) * 5/9, 1)
            output_apparent_temp = round((apparent_temp_f - 32) * 5/9, 1)
            output_wind_speed = round(wind_speed, 1)  # Already in km/h
        else:
            output_temp = round(temp_f, 1)
            output_wind_chill = round(wind_chill_f, 1)
            output_heat_index = round(heat_index_f, 1)
            output_dew_point = round(dew_point_f, 1)
            output_apparent_temp = round(apparent_temp_f, 1)
            output_wind_speed = round(wind_speed, 1)  # Already in mph
        
        # Safety assessments
        wind_chill_safety = safety.wind_chill_safety(wind_chill_f)
        heat_safety = safety.heat_index_safety(heat_index_f)
        uv_safety = safety.uv_safety(uv_index)
        
        # Clothing advice
        clothing = advisor.get_clothing_advice(temp_f, wind_chill_f, heat_index_f, humidity, wind_mph)
        
        # Prepare response
        result = {
            'calculations': {
                'temperature': output_temp,
                'wind_chill': output_wind_chill,
                'heat_index': output_heat_index,
                'dew_point': output_dew_point,
                'apparent_temperature': output_apparent_temp,
                'wind_speed': output_wind_speed,
                'humidity': humidity,
                'uv_index': uv_index
            },
            'safety': {
                'wind_chill': wind_chill_safety,
                'heat': heat_safety,
                'uv': uv_safety
            },
            'clothing': clothing,
            'units': units
        }
        
        return jsonify(result)
        
    except (ValueError, KeyError) as e:
        return jsonify({'error': 'Invalid input data'}), 400

# Health check endpoint for deployment
@app.route("/health")
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "app": "Weather Utility Pro"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
