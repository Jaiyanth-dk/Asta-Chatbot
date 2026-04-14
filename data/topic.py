import json
from collections import Counter
from pathlib import Path

# =========================
# CHANGE ONLY THIS
# =========================
topic = "galaxies"

# =========================
# USE SCRIPT'S OWN FOLDER
# =========================
script_dir = Path(__file__).resolve().parent

batch1_file = script_dir / f"{topic}_batch1_250.json"
batch2_file = script_dir / f"{topic}_batch2_250.json"
output_file = script_dir / f"{topic}_500.json"

# =========================
# LOAD FILES
# =========================
try:
    with open(batch1_file, "r", encoding="utf-8") as f:
        batch1 = json.load(f)
except FileNotFoundError:
    print(f"ERROR: Could not find file: {batch1_file}")
    exit()

try:
    with open(batch2_file, "r", encoding="utf-8") as f:
        batch2 = json.load(f)
except FileNotFoundError:
    print(f"ERROR: Could not find file: {batch2_file}")
    exit()

# =========================
# MERGE
# =========================
merged = batch1 + batch2

# =========================
# VALIDATION
# =========================
questions = [item.get("question", "").strip() for item in merged]
question_counts = Counter(questions)

duplicates = [q for q, count in question_counts.items() if count > 1]
unique_questions = len(question_counts)

print("=" * 50)
print(f"TOPIC: {topic}")
print("=" * 50)
print(f"Batch 1 count: {len(batch1)}")
print(f"Batch 2 count: {len(batch2)}")
print(f"Total merged count: {len(merged)}")
print(f"Unique questions: {unique_questions}")
print(f"Exact duplicate questions: {len(duplicates)}")

if len(merged) != 500:
    print("\nWARNING: Total merged count is NOT 500.")

if unique_questions != len(merged):
    print("\nWARNING: Duplicate questions found!")
    print("\nDuplicate question list:")
    for d in duplicates:
        print("-", d)
else:
    print("\nNo exact duplicate questions found.")

# =========================
# SAVE OUTPUT
# =========================
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"\nMerged file saved as: {output_file}")
print("=" * 50)