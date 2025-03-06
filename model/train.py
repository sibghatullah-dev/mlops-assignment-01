# model/train.py
import json
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

# Load CUAD dataset (assumes JSON format with 'text' and 'label' keys)
def load_data(data_path):
    with open(data_path, 'r') as f:
        data = json.load(f)
    texts, labels = [], []
    # This is a simplified example. Adapt to actual CUAD structure.
    for contract in data["contracts"]:
        for clause in contract["clauses"]:
            texts.append(clause["text"])
            labels.append(clause["risk_label"])  # 0 for safe, 1 for risk (example)
    return texts, labels

def preprocess_data(texts, labels, tokenizer, max_length=256):
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_length)
    dataset = torch.utils.data.TensorDataset(
        torch.tensor(encodings["input_ids"]),
        torch.tensor(encodings["attention_mask"]),
        torch.tensor(labels)
    )
    return dataset

def main():
    data_file = os.path.join("..", "data", "cuad.json")  # adjust if necessary
    texts, labels = load_data(data_file)
    
    # Split data
    train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)
    
    # Load tokenizer and model
    model_name = "nlpaueb/legal-bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    
    # Tokenize data
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=256)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=256)
    
    class ContractDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels
        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item["labels"] = torch.tensor(self.labels[idx])
            return item
        def __len__(self):
            return len(self.labels)
    
    train_dataset = ContractDataset(train_encodings, train_labels)
    val_dataset = ContractDataset(val_encodings, val_labels)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        evaluation_strategy="epoch",
        save_steps=10_000,
        save_total_limit=2,
        logging_dir='./logs'
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )
    
    # Train and save model
    trainer.train()
    model.save_pretrained("../app/model")
    tokenizer.save_pretrained("../app/model")
    
if __name__ == "__main__":
    main()
