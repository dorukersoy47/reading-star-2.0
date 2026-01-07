from transformers import AutoTokenizer
from optimum.intel import OVModelForCausalLM
from typing import cast

from config import MODEL_PATH, MAX_TOKENS_SONG, TEMPERATURE, TOP_P

model_path = MODEL_PATH

tokenizer = AutoTokenizer.from_pretrained(model_path)

model = cast(OVModelForCausalLM, OVModelForCausalLM.from_pretrained(
    model_path,
    export=True,
    load_in_8bit=True,
))

def generate_text(chat: list[dict], max_tokens: int = MAX_TOKENS_SONG) -> str:
    input_ids = tokenizer.apply_chat_template(
        chat,
        return_tensors="pt",
        thinking=False,
        return_dict=True,
        add_generation_prompt=True,
    )

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