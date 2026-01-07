from pathlib import Path
import os
from transformers import AutoTokenizer
from optimum.intel import OVModelForCausalLM
from config import MODEL_PATH

def main():
    target_dir = Path(__file__).parent / "models" / "ov_model"
    target_dir.mkdir(parents=True, exist_ok=True)

    # Optional: avoid any network retries/telemetry during export
    os.environ["HF_HUB_OFFLINE"] = "0"  # allow download now
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

    print(f"Preparing OpenVINO model from '{MODEL_PATH}' -> '{target_dir}'")

    # Download tokenizer from HF and persist locally
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    tokenizer.save_pretrained(target_dir.as_posix())

    # Export to OpenVINO IR with 8-bit compressed weights and persist
    ov_model = OVModelForCausalLM.from_pretrained(
        MODEL_PATH,
        export=True,
        load_in_8bit=True,
    )
    ov_model.save_pretrained(target_dir.as_posix())

    print("Done. Offline model saved.")

if __name__ == "__main__":
    main()