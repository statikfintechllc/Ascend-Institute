import subprocess
import os

# Explicitly verify conda environment creation
def verify_conda_env(env_name='ascendenv'):
    result = subprocess.run(['conda', 'env', 'list'], stdout=subprocess.PIPE, text=True)
    if env_name in result.stdout:
        print(f"✅ Conda environment '{env_name}' exists.")
    else:
        print(f"❌ Conda environment '{env_name}' is missing.")

# Explicitly verify model presence
def verify_llama_model(model_path='llama-13B.gguf'):
    if os.path.exists(model_path):
        print(f"✅ LLaMA model found at '{model_path}'.")
    else:
        print(f"❌ LLaMA model missing at '{model_path}'.")

# Explicitly verify essential files
def verify_files(files):
    for file in files:
        if os.path.exists(file):
            print(f"✅ '{file}' exists.")
        else:
            print(f"❌ '{file}' is missing.")

# Explicitly verify GPU and NVIDIA CUDA drivers
def verify_gpu():
    try:
        subprocess.run(['nvidia-smi'], check=True, stdout=subprocess.PIPE)
        print("✅ NVIDIA drivers and GPU detected.")
    except subprocess.CalledProcessError:
        print("❌ NVIDIA drivers or GPU not properly configured.")

# Run all verifications explicitly
def run_verification():
    verify_conda_env()
    verify_llama_model()
    verify_files(['Final_Goal.txt', 'automation_module.py', 'ascendenv.yml'])
    verify_gpu()

# Explicit main execution
if __name__ == '__main__':
    run_verification()
