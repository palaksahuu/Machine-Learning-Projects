

from flask import Blueprint, request, jsonify, send_file
import pandas as pd
import joblib
import os

# Create a Flask Blueprint
api_app = Blueprint("api", __name__)

# Get the absolute path to the backend folder
base_dir = os.path.dirname(os.path.abspath(__file__))  # backend/
data_dir = os.path.join(base_dir, "data")  # backend/data/

# Load the model and encoders using the correct path
model = joblib.load(os.path.join(data_dir, "model.pkl"))
le_speciality = joblib.load(os.path.join(data_dir, "le_speciality.pkl"))
le_region = joblib.load(os.path.join(data_dir, "le_region.pkl"))

# Load the Excel file
excel_path = os.path.join(data_dir, "dummy_npi_data.xlsx")
df = pd.read_excel(excel_path)

@api_app.route("/predicted_doctors", methods=["POST"])
def predicted_doctors():

    try:
        # Get input time from request
        data = request.json
        user_time = data.get("time")
        user_hour = int(user_time.split(":")[0])

        # Convert times to comparable format
        df["Login Time"] = pd.to_datetime(df["Login Time"]).dt.hour
        df["Logout Time"] = pd.to_datetime(df["Logout Time"]).dt.hour

        # Filter doctors active 
        available_doctors = df[(df["Login Time"] <= user_hour) & (df["Logout Time"] >= user_hour)]

        # Encode categorical data
        available_doctors["Speciality"] = le_speciality.transform(available_doctors["Speciality"])
        available_doctors["Region"] = le_region.transform(available_doctors["Region"])

        # Select features for prediction
        features = available_doctors[["Login Time", "Logout Time", "Usage Time (mins)", "Count of Survey Attempts", "Speciality", "Region"]]
        
        # Predict probability of attendance
        available_doctors["Prediction"] = model.predict(features)

        # Filter only likely attendees
        final_doctors = available_doctors[available_doctors["Prediction"] == 1][["NPI", "Speciality", "Region"]]

        # Save as CSV
        output_file = os.path.join(data_dir, "predicted_doctors.csv")
        final_doctors.to_csv(output_file, index=False)

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

