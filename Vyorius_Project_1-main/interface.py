import pickle
import numpy as np

with open('model/action_encoder.pkl', 'rb') as f:
    action_encoder = pickle.load(f)

with open('model/intent_encoder.pkl', 'rb') as f:
    intent_encoder = pickle.load(f)

with open('model/random_forest_intent_model.pkl', 'rb') as f:
    model = pickle.load(f)


def transform_new_sequence(new_sequence, sequence_length):

    encoded = [
        action_encoder.transform([a])[0] if a in action_encoder.classes_ else 0
        for a in new_sequence
    ]
    if len(encoded) < sequence_length:
        encoded += [0] * (sequence_length - len(encoded))
    return np.array(encoded).reshape(1, -1)

# predict on a new input 
new_sequence = ["Key:Ctrl+C", "Key:Ctrl+V", "Key:Alt+N"]
sequence_length = 3

try:
    X_new = transform_new_sequence(new_sequence, sequence_length)
    predicted_encoded = model.predict(X_new)[0]

    if predicted_encoded in intent_encoder.classes_:
        predicted_intent = predicted_encoded
    else:
        predicted_intent = "unknown"


    # confidence scores
    confidence_scores = model.predict_proba(X_new)[0]

    # Output
    print(f"\n Predicted Intent: {predicted_intent}\n")
    print(" Confidence Scores:")



    for i, score in enumerate(confidence_scores):
        try:
            intent = intent_encoder.inverse_transform([i])[0]
        except:
            intent = f"unknown_class_{i}"
        print(f"  ➤ {intent:15}: {score:.4f}")


except Exception as e:
    print(" Error predicting intent:", e)
