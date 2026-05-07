import json
import glob
import random

# Find all files ending with _500.json
files = glob.glob("*_500.json")

merged_data = []

for file in files:
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

            # Basic integrity checks
            if not isinstance(data, list):
                print(f"Skipped {file}: not a list")
                continue

            for item in data:
                if not all(key in item for key in ["topic", "question", "answer"]):
                    print(f"Skipped invalid entry in {file}")
                    continue

                merged_data.append(item)

            print(f"Loaded {len(data)} entries from {file}")

    except Exception as e:
        print(f"Error reading {file}: {e}")

# Shuffle dataset
random.shuffle(merged_data)

# Save merged file
output_file = "merged_dataset_4000.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)

print(f"\nMerged dataset saved as {output_file}")
print(f"Total Q&A pairs: {len(merged_data)}")