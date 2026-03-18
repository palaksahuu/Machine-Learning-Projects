# Doctor Availability and Survey Prediction API

## Project Overview

This project builds a machine learning-based system to identify doctors who are most likely to attend a survey at a given time. The system uses historical activity data such as login time, logout time, usage duration, and survey attempts to predict doctor availability and engagement.

The project includes:

- Model training using Random Forest
- Backend API using Flask Blueprint
- Data preprocessing and feature engineering
- CSV output generation for predicted doctors

The system takes a time input and returns a list of doctors who are active and likely to participate in the survey.

---

## Objectives

The main goals of this project are:

- Identify doctors available at a specific time
- Predict survey participation likelihood
- Automate doctor targeting for surveys
- Provide an API for real-time predictions

---

## Technologies Used

- Python
- Pandas
- Scikit-learn
- Flask
- Joblib
- Random Forest Classifier

---

## Dataset

The dataset contains doctor activity and profile information.

Key columns include:

- NPI
- Speciality
- Region
- Login Time
- Logout Time
- Usage Time (mins)
- Count of Survey Attempts

These features are used to determine availability and likelihood of participation.

---

### Features Used

- Login Time
- Logout Time
- Usage Time (mins)
- Count of Survey Attempts
- Speciality
- Region

### Target Variable

- Count of Survey Attempts (used to infer engagement level)

---

## Model Saving

The trained model and encoders are saved using joblib.

```
joblib.dump(model, "data/model.pkl")
joblib.dump(le_speciality, "data/le_speciality.pkl")
joblib.dump(le_region, "data/le_region.pkl")
```

---

## API Implementation

The backend API is implemented using Flask Blueprint.

### Endpoint

```
POST /predicted_doctors
```

### Input Format

```
{
    "time": "10:00"
}
```

---

## API Workflow

1. Extract user input time
2. Convert time into hour format
3. Filter doctors active at that time
4. Encode categorical variables
5. Select relevant features
6. Predict using trained model
7. Filter doctors with positive predictions
8. Return results as a CSV file

---

## Output

The API generates a CSV file containing predicted doctors.

Columns in output:

- NPI
- Speciality
- Region



---
