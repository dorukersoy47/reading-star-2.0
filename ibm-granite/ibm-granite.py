from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "ibm-granite/granite-4.0-micro"
tokenizer = AutoTokenizer.from_pretrained(model_name)
device = "cuda" if torch.cuda.is_available() else "cpu"
# On CPU you might omit device_map or set device_map="cpu"
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto" if device=="cuda" else None)
model.eval()

prompt = "Test."
inputs = tokenizer(prompt, return_tensors="pt").to(device)
import time; start = time.time()
outputs = model.generate(**inputs, max_new_tokens=20)
print("Elapsed:", time.time()-start)
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)

