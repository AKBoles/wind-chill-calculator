from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_wind_chill(T, Wind):
    return round(35.74 + (0.6215 * T) - (35.75 * (Wind ** 0.16)) + (0.4275 * T * (Wind ** 0.16)), 2)

def fahrenheit_to_celsius(f):
    return round((f - 32) * 5/9, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    wind_chill_f, wind_chill_c = None, None
    frostbite_warning = None
    frostbite_time = None

    if request.method == "POST":
        try:
            temp = float(request.form["temperature"])
            wind_speed = float(request.form["wind_speed"])
            wind_chill_f = calculate_wind_chill(temp, wind_speed)
            wind_chill_c = fahrenheit_to_celsius(wind_chill_f)

            # Determine frostbite warning & time
            if wind_chill_f <= -40:
                frostbite_warning = "❄️ Extreme Frostbite Risk: Skin can freeze in under 5 minutes!"
                frostbite_time = "Estimated time to frostbite: Less than 5 minutes."
            elif wind_chill_f <= -20:
                frostbite_warning = "⚠️ Severe Frostbite Risk: Skin can freeze in 10-15 minutes!"
                frostbite_time = "Estimated time to frostbite: 10-15 minutes."
            elif wind_chill_f <= -10:
                frostbite_warning = "❄️ Frostbite Warning: Skin can freeze in about 30 minutes."
                frostbite_time = "Estimated time to frostbite: ~30 minutes."
            elif wind_chill_f <= 0:
                frostbite_warning = "⚠️ Frostbite Possible: Prolonged exposure may cause frostbite."
                frostbite_time = "Estimated time to frostbite: 1 hour or more."
        
        except ValueError:
            wind_chill_f, wind_chill_c = "Invalid input", None

    return render_template("index.html", wind_chill_f=wind_chill_f, wind_chill_c=wind_chill_c, 
                           frostbite_warning=frostbite_warning, frostbite_time=frostbite_time)

if __name__ == "__main__":
    app.run(debug=True)
