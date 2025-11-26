from flask import Flask, request, render_template
import numpy as np
import pickle
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Load the trained model and scaler
model = pickle.load(open("rf_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# Feature order used during training (matches train_model.py)
feature_order = [
    "from_Florianopolis_SC", "from_Sao_Paulo_SP", "from_Salvador_BH", "from_Brasilia_DF", 
    "from_Rio_de_Janeiro_RJ", "from_Campo_Grande_MS", "from_Aracaju_SE", "from_Natal_RN", "from_Recife_PE",
    "destination_Florianopolis_SC", "destination_Sao_Paulo_SP", "destination_Salvador_BH", 
    "destination_Brasilia_DF", "destination_Rio_de_Janeiro_RJ", "destination_Campo_Grande_MS",
    "destination_Aracaju_SE", "destination_Natal_RN", "destination_Recife_PE",
    "flightType_economic", "flightType_firstClass", "flightType_premium",
    "agency_Rainbow", "agency_CloudFy", "agency_FlyingDrops",
    "month", "year", "day"
]

@app.route("/")
def home():
    return render_template("index.html", prediction=None)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get user input
        Departure = request.form["from"]
        Destination = request.form["destination"]
        FlightType = request.form["flightType"]
        Agency = request.form["agency"]
        month = int(request.form["month"])
        year = int(request.form["year"])
        day = int(request.form["day"])

        # Create a feature vector with correct ordering
        input_features = np.zeros(len(feature_order))  # Initialize all to 0

        # Normalize input to match feature names (remove spaces, parentheses, add underscores)
        def normalize_name(name):
            """Convert form input to feature name format"""
            # Handle special cases for city names
            name = name.replace(" (", "_").replace("(", "").replace(")", "").replace(" ", "_")
            return name
        
        # Encode categorical variables (Set index positions to 1 where applicable)
        departure_normalized = normalize_name(Departure)
        destination_normalized = normalize_name(Destination)
        
        from_feature = f"from_{departure_normalized}"
        dest_feature = f"destination_{destination_normalized}"
        flight_type_feature = f"flightType_{FlightType}"
        agency_feature = f"agency_{Agency}"
        
        if from_feature in feature_order:
            input_features[feature_order.index(from_feature)] = 1
        if dest_feature in feature_order:
            input_features[feature_order.index(dest_feature)] = 1
        if flight_type_feature in feature_order:
            input_features[feature_order.index(flight_type_feature)] = 1
        if agency_feature in feature_order:
            input_features[feature_order.index(agency_feature)] = 1
        
        # Assign numerical values (Month, Year, Day)
        input_features[feature_order.index("month")] = month
        input_features[feature_order.index("year")] = year
        input_features[feature_order.index("day")] = day

        # Scale input features
        input_scaled = scaler.transform([input_features])  # Ensure correct transformation

        # Make prediction
        prediction = model.predict(input_scaled)[0]
        
        # Generate visualization (Price Trend Graph)
        plt.figure(figsize=(5, 3))
        plt.bar(["Predicted Price"], [prediction], color="blue")
        plt.ylabel("Price ($)")
        plt.title("Flight Price Prediction")
        plt.grid(axis="y")

        # Convert plot to image
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template("index.html", prediction=round(prediction, 2), plot_url=plot_url)

    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print(error_msg)  # Print to console for debugging
        return f"<h2>Error occurred</h2><p>{str(e)}</p><pre>{traceback.format_exc()}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
