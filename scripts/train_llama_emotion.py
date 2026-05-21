from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import torch

# Load dataset from your .jsonl file
dataset = load_dataset("json", data_files="D:/jarvis_project/data/jarvis_emotion.jsonl")

# Split into train and test
dataset = dataset["train"].train_test_split(test_size=0.2)

# Use small pretrained model
model_name = "distilbert-base-uncased"  # small, fast for testing

tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    return tokenizer(batch["prompt"], padding="max_length", truncation=True)


dataset = dataset.map(tokenize, batched=True)

# Map emotions to numbers
labels = list(set(dataset["train"]["completion"]))
label2id = {label.strip(): i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}

def encode_labels(example):
    example["label"] = label2id[example["completion"].strip()]
    return example


dataset = dataset.map(encode_labels)

# Load model
model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=len(labels), id2label=id2label, label2id=label2id
)

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Training setup
training_args = TrainingArguments(
    output_dir="D:/jarvis_project/models/jarvis_emotion",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
)

# Train the model
trainer.train()

# Save the model
trainer.save_model("D:/jarvis_project/models/jarvis_emotion")
print("✅ Training complete. Model saved successfully!")
