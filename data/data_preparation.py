import json
import random

# Load original merged Q&A file
with open("merged_qna.json", "r", encoding="utf-8") as f:
    data = json.load(f)

processed_data = []

for item in data:
    topic = item.get("topic", "").strip()
    question = item.get("question", "").strip()
    answer = item.get("answer", "").strip()

    # Skip empty/bad entries
    if not question or not answer:
        continue

    input_text = f"answer astronomy question about {topic}: {question}"
    target_text = answer

    processed_data.append({
        "topic": topic,
        "input_text": input_text,
        "target_text": target_text
    })

# Shuffle the data so split is random
random.seed(42)  # keeps split same every run
random.shuffle(processed_data)

# 80/20 split
split_index = int(len(processed_data) * 0.8)

train_data = processed_data[:split_index]
val_data = processed_data[split_index:]

# Save training file
with open("train.json", "w", encoding="utf-8") as f:
    json.dump(train_data, f, indent=4, ensure_ascii=False)

# Save validation file
with open("val.json", "w", encoding="utf-8") as f:
    json.dump(val_data, f, indent=4, ensure_ascii=False)

# Print summary
print(f"Total valid samples: {len(processed_data)}")
print(f"Training samples: {len(train_data)}")
print(f"Validation samples: {len(val_data)}")
print("Saved train.json and val.json successfully.")