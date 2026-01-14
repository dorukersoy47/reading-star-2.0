from transformers import AutoTokenizer
from optimum.intel import OVModelForCausalLM
from typing import cast
from pathlib import Path
import os

from config import LYRIC_MAX_TOKENS, TEMPERATURE, TOP_P

# Force offline behavior at runtime
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

# Always use the locally prepared OpenVINO model directory
ov_model_dir = Path(__file__).parent / "ai_models" / "ov_model"
if not ov_model_dir.exists():
    raise FileNotFoundError(
        f"Offline model not found at '{ov_model_dir}'. "
        f"Run: python lyric-generation\\prepare_model.py"
    )

tokenizer = AutoTokenizer.from_pretrained(ov_model_dir.as_posix())

model = cast(OVModelForCausalLM, OVModelForCausalLM.from_pretrained(
    ov_model_dir.as_posix(),
    export=False,       # already exported
    load_in_8bit=False, # already compressed
))

def generate_text(chat: list[dict], max_tokens: int = MAX_TOKENS_SONG) -> str:
    input_ids = tokenizer.apply_chat_template(
        chat,
        return_tensors="pt",
        thinking=False,
        return_dict=True,
        add_generation_prompt=True,
    )

    output = model.generate(  # type: ignore[attr-defined]
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