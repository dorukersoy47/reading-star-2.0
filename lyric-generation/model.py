import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import MODEL_PATH, MAX_TOKENS_SONG, TEMPERATURE, TOP_P

device = "cuda" if torch.cuda.is_available() else "cpu"

_tokenizer = None
_model = None


def get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    return _tokenizer


def get_model():
    global _model
    if _model is None:
        _model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
        _model.to(device)
        _model.eval()
    return _model


def load_model():
    get_tokenizer()
    get_model()
    print(f"Model loaded on device: {device}")


def generate_text(chat: list[dict], max_tokens: int = MAX_TOKENS_SONG) -> str:
    tokenizer = get_tokenizer()
    model = get_model()
    
    formatted = tokenizer.apply_chat_template(
        chat, tokenize=False, add_generation_prompt=True
    )
    
    input_tokens = tokenizer(formatted, return_tensors="pt").to(device)

    with torch.no_grad():
        output = model.generate(
            **input_tokens,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=TEMPERATURE,
            top_p=TOP_P,
        )

    generated_tokens = output[0][input_tokens["input_ids"].shape[1]:]
    answer = tokenizer.decode(generated_tokens, skip_special_tokens=True)
    return answer.strip()