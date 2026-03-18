import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# processed sliding window dataset
sliding_data = pd.read_csv("processed_window_data.csv")


with open('model/intent_encoder.pkl', 'rb') as f:
    intent_encoder = pickle.load(f)
#window size
n = 3

# feature
X = sliding_data[[f'action_{i+1}' for i in range(n)]]
y = sliding_data['intent']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)


clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# predictions
y_pred = clf.predict(X_test)

# Evaluation metrics
print("\nModel Evaluation Results:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# save trained model
with open('model/random_forest_intent_model.pkl', "wb") as f:
    pickle.dump(clf, f)
