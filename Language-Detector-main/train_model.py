import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# ✅ Load dataset
df = pd.read_csv("language.csv")

# ✅ Check if column names are correct
print("CSV Columns:", df.columns)

# ✅ Ensure correct column names
texts = df["Text"].astype(str)  # Update if needed
labels = df["language"]

# ✅ Train vectorizer on complete dataset
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(texts)

# ✅ Train Naive Bayes model
model = MultinomialNB()
model.fit(X_train, labels)

# ✅ Save trained model and vectorizer
with open("vectorizer.pkl", "wb") as vec_file:
    pickle.dump(vectorizer, vec_file)

with open("language_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

# ✅ Debug: Check vocabulary size
print("Vectorizer Vocabulary Size:", len(vectorizer.get_feature_names_out()))
print("✅ Model training completed!")
