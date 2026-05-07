import json

import os

def count_qa_pairs(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0

    # Case 1: JSON is a list of Q&A objects
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "question" in item and "answer" in item:
                count += 1

    # Case 2: JSON is wrapped inside another dict (e.g., {"data": [...]})
    elif isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and "question" in item and "answer" in item:
                        count += 1

    return count


if __name__ == "__main__":
    file_path = "time_batch2.json"  # replace with your file name
    total = count_qa_pairs(file_path)
    print(f"Total Q&A pairs: {total}")
