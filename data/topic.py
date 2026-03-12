import json

with open("/home/Jaiyanth/Desktop/Asta/data/black.json", "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = []
c=0
for item in data:
    c+=1

'''with open("/home/Jaiyanth/Desktop/Asta/data/black_holes.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)'''

print(c)