# run_llama_final_goal.py

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Path to your local LLaMA model
MODEL_PATH = "./models/Llama-2-7b-hf"
PROMPT_FILE = "./final_goal.txt"

def main():
    print("[Ascend Init] Loading Sovereign Core LLaMA...")
    
    # Load tokenizer and model from local path
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Load prompt
    with open(PROMPT_FILE, "r") as f:
        prompt = f.read()

    print("[Ascend Init] Executing final_goal.txt...
")
    
    # Run the model pipeline
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    output = pipe(prompt, max_new_tokens=512, do_sample=True, temperature=0.7)

    print("[Ascend Response]")
    print(output[0]["generated_text"])

if __name__ == "__main__":
    main()
