import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import pickle


data = pd.read_csv("Action_logs.csv")

data['action_token'] = data['Action Type'] + ":" + data['Key/Button']

scaler = MinMaxScaler()
data[['cursor_x_norm', 'cursor_y_norm']] = scaler.fit_transform(data[['Cursor X', 'Cursor Y']])

# Create sliding window sequences 
n = 3
sequences = []
intents = []

for i in range(len(data) - n + 1):
    window = data['action_token'].iloc[i:i+n].tolist()
    label = data['Intent'].iloc[i+n-1] 

    if pd.notna(label) and label.strip() != "":
        sequences.append(window)
        intents.append(label.strip())

# Convert to DataFrame
sliding_df = pd.DataFrame(sequences, columns=[f'action_{i+1}' for i in range(n)])
sliding_df['intent'] = intents

# Encode actions using LabelEncoder
action_encoder = LabelEncoder()
all_actions = sliding_df[[f'action_{i+1}' for i in range(n)]].values.flatten()
action_encoder.fit(all_actions)

for i in range(n):
    col = f'action_{i+1}'
    sliding_df[col] = action_encoder.transform(sliding_df[col])

# Encode intents
intent_encoder = LabelEncoder()
sliding_df['intent_encoded'] = intent_encoder.fit_transform(sliding_df['intent'])

# Save processed dataset and encoders
sliding_df.to_csv("processed_window_data.csv", index=False)
"Cursor X" and "Cursor Y" 
with open('model/action_encoder.pkl', 'wb') as f:
    pickle.dump(action_encoder, f)

with open('model/intent_encoder.pkl', 'wb') as f:
    pickle.dump(intent_encoder, f)

print(sliding_df.head())




print("Encoded intents:", intent_encoder.classes_)
