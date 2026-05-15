from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
ADAPTER_PATH = "./trained_model"
OUTPUT_PATH = "./merged_qwen"

print("Loading base model...")
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16,
    device_map="cpu"
)

print("Loading adapter...")
model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_PATH
)

print("Merging...")
merged_model = model.merge_and_unload()

print("Saving merged model...")
merged_model.save_pretrained(OUTPUT_PATH)
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.save_pretrained(OUTPUT_PATH)

print("Done.")