from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def calculate_wind_chill(T, Wind):
    """Calculate Wind Chill using Fahrenheit and mph."""
    return round(35.74 + (0.6215 * T) - (35.75 * (Wind ** 0.16)) + (0.4275 * T * (Wind ** 0.16)), 2)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            temp = float(request.form["temperature"])
            wind_speed = float(request.form["wind_speed"])
            wind_chill = calculate_wind_chill(temp, wind_speed)
            return render_template("index.html", wind_chill=wind_chill)
        except ValueError:
            return render_template("index.html", wind_chill="Invalid input. Please enter numeric values.")
    
    # Ensures wind chill doesn't persist on refresh
    return render_template("index.html", wind_chill=None)

if __name__ == "__main__":
    app.run(debug=True)
