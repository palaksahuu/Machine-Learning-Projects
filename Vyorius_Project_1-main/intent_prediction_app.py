import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle

st.set_page_config(page_title="Excel User Intent Prediction", layout="centered")
st.title(" Excel User Intent Predictor")

# Load models and encoders
@st.cache_resource
def load_model_and_encoders():
    with open("model/random_forest_intent_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("model/action_encoder.pkl", "rb") as f:
        action_encoder = pickle.load(f)
    with open("model/intent_encoder.pkl", "rb") as f:
        intent_encoder = pickle.load(f)
    return model, action_encoder, intent_encoder

model, action_encoder, intent_encoder = load_model_and_encoders()
sequence_length = 3

# Input 
st.subheader(" Input a Sequence of Excel Actions")
actions = []
for i in range(sequence_length):
    action_type = st.selectbox(f"Action {i+1} - Type", ["Key", "Button"], key=f"type_{i}")
    key_button = st.text_input(f"Action {i+1} - Key/Button", key=f"key_{i}")
    actions.append(f"{action_type}:{key_button}")

# Prediction logic
def predict_intent(new_sequence):
    encoded = [
        action_encoder.transform([a])[0] if a in action_encoder.classes_ else 0
        for a in new_sequence
    ]
    if len(encoded) < sequence_length:
        encoded += [0] * (sequence_length - len(encoded))
    X_input = np.array(encoded).reshape(1, -1)

    pred_encoded = model.predict(X_input)[0]
    confidence_scores = model.predict_proba(X_input)[0]

    predicted_intent = pred_encoded
    if pred_encoded in intent_encoder.classes_:
        predicted_intent = pred_encoded
    else:
        predicted_intent = "unknown"

    return predicted_intent, confidence_scores

# Predict button
if st.button(" Predict Intent"):
    predicted_encoded, scores = predict_intent(actions)
    intent_label = intent_encoder.inverse_transform([predicted_encoded])[0]

    st.success(f" **Predicted Intent:** `{intent_label}`")
    st.subheader(" Confidence Scores")
    for i, score in enumerate(scores):
        label = intent_encoder.inverse_transform([i])[0]
        st.write(f" {label}: **{score:.2%}**")

    # Visualization
    st.subheader(" Action Sequence Timeline")
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.plot(range(sequence_length), [1]*sequence_length, 'o-', color='blue', markersize=12, linewidth=2)
    for i, action in enumerate(actions):
        ax.text(i, 1.05, action, rotation=45, ha='right', fontsize=10)
    ax.set_title(f"Predicted Intent: {intent_label}")
    ax.axis('off')
    st.pyplot(fig)

# Optional Feedback Section
with st.expander(" Submit correct Intent (Feedback Loop)"):
    corrected_intent = st.text_input("Correct Intent (if prediction was wrong)")
    if st.button("Submit Feedback"):
        log_file = "feedback_log.csv"
        feedback_data = {
            "Sequence": str(actions),
            "Predicted": intent_encoder.inverse_transform([predicted_encoded])[0],
            "Corrected": corrected_intent
        }
        if not os.path.exists(log_file):
            pd.DataFrame([feedback_data]).to_csv(log_file, index=False)
        else:
            pd.concat([pd.read_csv(log_file), pd.DataFrame([feedback_data])], ignore_index=True).to_csv(log_file, index=False)
        st.success(" Feedback submitted")
