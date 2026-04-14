import json
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Trainer,
    TrainingArguments
)

# =========================
# 1. Load train and val data
# =========================
with open("train.json", "r", encoding="utf-8") as f:
    train_data = json.load(f)

with open("val.json", "r", encoding="utf-8") as f:
    val_data = json.load(f)

print(f"Training samples: {len(train_data)}")
print(f"Validation samples: {len(val_data)}")

# =========================
# 2. Convert to HF Datasets
# =========================
train_dataset = Dataset.from_list(train_data)
val_dataset = Dataset.from_list(val_data)

# =========================
# 3. Load model + tokenizer
# =========================
model_name = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# =========================
# 4. Tokenization settings
# =========================
max_input_length = 128
max_target_length = 256

def preprocess_function(examples):
    # Tokenize inputs
    model_inputs = tokenizer(
        examples["input_text"],
        max_length=max_input_length,
        truncation=True,
        padding="max_length"
    )

    # Tokenize targets
    labels = tokenizer(
        text_target=examples["target_text"],
        max_length=max_target_length,
        truncation=True,
        padding="max_length"
    )

    # VERY IMPORTANT: replace pad tokens with -100
    # so loss ignores padded positions
    labels_ids = labels["input_ids"]
    labels_ids = [
        [token if token != tokenizer.pad_token_id else -100 for token in label]
        for label in labels_ids
    ]

    model_inputs["labels"] = labels_ids
    return model_inputs

# =========================
# 5. Tokenize datasets
# =========================
train_dataset = train_dataset.map(preprocess_function, batched=True)
val_dataset = val_dataset.map(preprocess_function, batched=True)

print("\nSample tokenized training item keys:", train_dataset.column_names)
print("Sample labels (first 20):", train_dataset[0]["labels"][:20])

# =========================
# 6. Remove text columns
# =========================
remove_cols = [col for col in ["topic", "input_text", "target_text"] if col in train_dataset.column_names]
train_dataset = train_dataset.remove_columns(remove_cols)
val_dataset = val_dataset.remove_columns(remove_cols)

# =========================
# 7. Set dataset format for PyTorch
# =========================
train_dataset.set_format(type="torch")
val_dataset.set_format(type="torch")

# =========================
# 8. Data collator
# =========================
data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model,
    label_pad_token_id=-100
)

# =========================
# 9. Save path in Drive
# =========================
save_path = "/content/drive/MyDrive/asta/final"

# =========================
# 10. Training arguments
# =========================
training_args = TrainingArguments(
    output_dir="/content/astronomy_qna_model",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-4,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=4,
    weight_decay=0.01,
    save_total_limit=2,
    logging_dir="/content/logs",
    logging_steps=5,
    load_best_model_at_end=True,
    fp16=False,
    report_to="none",
    remove_unused_columns=False
)

# =========================
# 11. Trainer
# =========================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=data_collator
)

# =========================
# 12. Sanity check BEFORE training
# =========================
sample_batch = next(iter(trainer.get_train_dataloader()))
print("\nBatch keys:", sample_batch.keys())
print("Input shape:", sample_batch["input_ids"].shape)
print("Label shape:", sample_batch["labels"].shape)
print("First label row (first 20):", sample_batch["labels"][0][:20])

# =========================
# 13. Train
# =========================
trainer.train()

# =========================
# 14. Save final model
# =========================
trainer.save_model(save_path)
tokenizer.save_pretrained(save_path)

print(f"\nTraining complete. Model saved to: {save_path}")