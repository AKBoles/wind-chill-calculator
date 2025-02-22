from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_wind_chill(T, Wind):
    """Calculate Wind Chill in Fahrenheit."""
    return round(35.74 + (0.6215 * T) - (35.75 * (Wind ** 0.16)) + (0.4275 * T * (Wind ** 0.16)), 2)

def fahrenheit_to_celsius(f):
    """Convert Fahrenheit to Celsius."""
    return round((f - 32) * 5/9, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    wind_chill_f, wind_chill_c = None, None

    if request.method == "POST":
        try:
            temp = float(request.form["temperature"])
            wind_speed = float(request.form["wind_speed"])
            wind_chill_f = calculate_wind_chill(temp, wind_speed)
            wind_chill_c = fahrenheit_to_celsius(wind_chill_f)
        except ValueError:
            wind_chill_f, wind_chill_c = "Invalid input", None

    return render_template("index.html", wind_chill_f=wind_chill_f, wind_chill_c=wind_chill_c)

if __name__ == "__main__":
    app.run(debug=True)
