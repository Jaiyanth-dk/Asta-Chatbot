import json

# Input and output file names
input_file = "galaxies_1qna.json"
output_file = "galaxies_qna.json"

# Load the JSON data
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Clean each answer
for item in data:
    if "answer" in item and isinstance(item["answer"], str):
        item["answer"] = item["answer"].replace("\n\n**", "").rstrip()

# Save cleaned JSON
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(f"Cleaned file saved as {output_file}")