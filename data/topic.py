import re
import json

# === SETTINGS ===
input_file = "planets.txt"   # your txt file name
output_file = "planets.qna.json"             # output json file name
topic_name = "planets"                       # topic field in JSON

# === READ FILE ===
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# === REGEX TO EXTRACT Q&A PAIRS ===
pattern = r"\d+\.\s*Q:\s*(.*?)\n\s*A+\:\s*(.*?)(?=\n\d+\.\s*Q:\s*|\Z)"

matches = re.findall(pattern, text, re.DOTALL)

# === BUILD JSON STRUCTURE ===
data = []

for question, answer in matches:
    question = question.strip()
    answer = answer.strip()

    data.append({
        "topic": topic_name,
        "question": question,
        "answer": answer
    })

# === SAVE JSON ===
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Converted {len(data)} Q&A pairs into {output_file}")