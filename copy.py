import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Get the token from the environment variable
api_token = os.getenv("HUGGINGFACE_TOKEN")

# Set the model name you want to download
model_name = "bert-base-uncased"

# Download the model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_name, use_auth_token=api_token)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=api_token)

# Now the model and tokenizer are downloaded and ready to use
print("Model and tokenizer downloaded successfully!")
