import openai
import os

# Set your OpenAI API key
openai.api_key = "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"

#  fine-tuned model id
response = openai.ChatCompletion.create(
  model="ft-your-finetuned-model-id",
  messages=[
    {"role": "user", "content": "Kal Sunday hai, kya karein?"}
  ],
  temperature=0.7
)

print("Assistant:", response['choices'][0]['message']['content'])
