# Hinglish Voice-AI Fine-Tuning Project

##  Overview
Fine-tuning GPT-3.5 to understand and respond in casual Hinglish dialogue for Voice-AI applications.

##  Setup Instructions
1. Install dependencies:

    pip install openai

2. Set your OpenAI API key:
  
    export OPENAI_API_KEY="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"
 

3. Run fine-tuning script:

    python fine_tune.py


4. Once fine-tuned, run inference:

    python inference.py



##  Dataset (`dataset.jsonl`)
- 15 examples** of casual Hinglish conversations.
- Topics: Daily activities, plans, food, mood, etc.
- Format:** JSONL with "prompt" and "completion".



##  Design Rationale

### Dataset Selection
- Hinglish style for natural user queries.
- Covered daily conversations: friends, food, plans, emotions.

### Model & Hyperparameters
- Model: `gpt-3.5-turbo` for cost-efficiency, speed, and dialogue strength.
- Epochs: 2 epochs (small dataset; more could overfit).
- Learning rate: Default (managed by OpenAI).

### Prompt Formatting
- Prompt begins with `User: ...` and Assistant reply is the completion.
- Makes dialogue flow natural during inference.

### Inference Settings
- Temperature: 0.7 to allow slight creativity without making answers too random.
- Model generates natural casual responses.

### Evaluation Plan
- Manual human review initially.
- Later stages can automate with metrics like BLEU, ROUGE, or human-in-the-loop testing.



## 📊 Sample Outputs
Example inference for unseen input:

Prompt: 
User: Kal Sunday hai, kya karein?

Assistant Reply: 
Chalo friends ke saath outing plan karte hain ya movie dekhte hain!


