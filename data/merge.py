import json

input_files = [
    "planets_qna.json",
    "blackholes_qna.json",
    "galaxies_qna.json",
    "cosmology_qna.json"
]

all_data = []

for file in input_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        all_data.extend(data)

with open("merged_qna.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)

print(f"Merged {len(all_data)} Q&A pairs into merged_qna.json")