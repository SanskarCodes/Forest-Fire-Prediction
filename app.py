import pickle

import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Load trained model
with open("models/ridge.pkl", "rb") as f:
    model = pickle.load(f)

# Load scaler
with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    """Predict the Fire Weather Index."""

    if request.method == "POST":
        try:
            temperature = float(request.form.get("Temperature"))
            rh = float(request.form.get("RH"))
            ws = float(request.form.get("Ws"))
            rain = float(request.form.get("Rain"))
            ffmc = float(request.form.get("FFMC"))
            dmc = float(request.form.get("DMC"))
            isi = float(request.form.get("ISI"))
            classes = float(request.form.get("Classes"))
            region = float(request.form.get("Region"))

            features = pd.DataFrame([{
                "Temperature": temperature,
                "RH": rh,
                "Ws": ws,
                "Rain": rain,
                "FFMC": ffmc,
                "DMC": dmc,
                "ISI": isi,
                "Classes": classes,
                "Region": region
            }])

            scaled_features = scaler.transform(features)
            prediction = round(model.predict(scaled_features)[0], 2)

# Risk Classification
            if prediction < 5:
                risk = "🟢 Low Fire Risk"
                recommendation = "Fire conditions are currently stable. Normal outdoor activities are considered safe."
                risk_color = "#4CAF50"

            elif prediction < 15:
                risk = "🟡 Moderate Fire Risk"
                recommendation = "Avoid unnecessary burning and stay updated with local weather conditions."
                risk_color = "#FFC107"

            elif prediction < 30:
                risk = "🟠 High Fire Risk"
                recommendation = "High possibility of wildfire spread. Outdoor burning is strongly discouraged."
                risk_color = "#FF9800"

            else:
                risk = "🔴 Extreme Fire Risk"
                recommendation = "Extreme fire danger. Immediate preventive measures are recommended."
                risk_color = "#F44336"

            return render_template(
                "home.html",
                results=prediction,
                risk=risk,
                recommendation=recommendation,
                risk_color=risk_color
            )
        
        except ValueError:
            return render_template(
            "home.html",
            error="Please enter valid numeric values."
            )

    return render_template("home.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
