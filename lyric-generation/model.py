import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import MODEL_PATH, MAX_TOKENS_SONG, TEMPERATURE, TOP_P

torch.set_num_threads(torch.get_num_threads())  # Use all CPU threads

device = "cpu"
model_path = MODEL_PATH

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map=device,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
)

def generate_text(chat: list[dict], max_tokens: int = MAX_TOKENS_SONG) -> str:
    input_ids = tokenizer.apply_chat_template(
        chat,
        return_tensors="pt",
        thinking=False,
        return_dict=True,
        add_generation_prompt=True,
    ).to(device)

    with torch.inference_mode():
        output = model.generate(
            **input_ids,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=TEMPERATURE,
            top_p=TOP_P,
        )
    
    prediction = tokenizer.decode(
        output[0, input_ids["input_ids"].shape[1]:],
        skip_special_tokens=True,
    )

    return prediction