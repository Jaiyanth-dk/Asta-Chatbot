import re
import json

# ==== SETTINGS ====
input_file = "light_optics_1000_qna_numbered.txt"      # your txt file
output_file = "optics_1000.json"    # output json file
topic_name = "optics"                # topic field for all entries
# ==================

# Read the txt file
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Regex to capture:
# 1. Question text
# 2. Answer text
pattern = re.compile(
    r"\d+\.\s*Question:\s*(.*?)\s*Answer:\s*(.*?)(?=\n\d+\.\s*Question:|\Z)",
    re.DOTALL
)

matches = pattern.findall(content)

data = []

for question, answer in matches:
    data.append({
        "topic": topic_name,
        "question": question.strip(),
        "answer": answer.strip().replace("\n", " ")
    })

# Save as JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Converted {len(data)} Q&As into {output_file}")