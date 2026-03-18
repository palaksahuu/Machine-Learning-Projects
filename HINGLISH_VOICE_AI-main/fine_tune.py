import openai
import os

#  OpenAI API key
openai.api_key = "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"


# Upload training dataset
upload_response = openai.File.create(
  file=open("dataset.jsonl", "rb"),
  purpose="fine-tune"
)

file_id = upload_response["id"]
print(f"Uploaded File ID: {file_id}")

# Start fine-tuning
fine_tune_response = openai.FineTune.create(
  training_file=file_id,
  model="gpt-3.5-turbo",
  n_epochs=2
)

print("Fine-tune job started:")
print(fine_tune_response)
