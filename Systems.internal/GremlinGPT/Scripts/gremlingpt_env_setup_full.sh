#!/bin/zsh
# Full GremlinGPT Conda environment setup with extended dependencies
if ! command -v conda &> /dev/null; then
  echo '[-] Conda not found. Please install Miniconda or Anaconda.'
  exit 1
fi
echo '[+] Creating environment: ai-core'
conda create -n ai-core python=3.10 -y
echo '[+] Installing packages in: ai-core'
conda run -n ai-core pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers bitsandbytes accelerate deepspeed flash-attn xformers llama-cpp-python sentence-transformers pytorch-lightning optimum scipy numpy
echo '[+] Creating environment: starcoder-wrapper'
conda create -n starcoder-wrapper python=3.10 -y
echo '[+] Installing packages in: starcoder-wrapper'
conda run -n starcoder-wrapper pip install huggingface_hub transformers auto-gptq einops
echo '[+] Creating environment: nanogpt-wrapper'
conda create -n nanogpt-wrapper python=3.10 -y
echo '[+] Installing packages in: nanogpt-wrapper'
conda run -n nanogpt-wrapper pip install numpy datasets tiktoken
echo '[+] Creating environment: ai-agents'
conda create -n ai-agents python=3.10 -y
echo '[+] Installing packages in: ai-agents'
conda run -n ai-agents pip install crewai langchain==0.0.293 langgraph openai autogpt babyagi tiktoken pydantic tenacity
echo '[+] Creating environment: vector-db'
conda create -n vector-db python=3.10 -y
echo '[+] Installing packages in: vector-db'
conda run -n vector-db pip install chromadb faiss-cpu weaviate-client
echo '[+] Creating environment: dashboard-ui'
conda create -n dashboard-ui python=3.10 -y
echo '[+] Installing packages in: dashboard-ui'
conda run -n dashboard-ui pip install streamlit gradio dash panel flask fastapi uvicorn voila gunicorn
echo '[+] Creating environment: quantum-research'
conda create -n quantum-research python=3.10 -y
echo '[+] Installing packages in: quantum-research'
conda run -n quantum-research pip install qiskit qiskit-aer qiskit-ibmq-provider cirq pennylane azure-quantum braket
echo '[+] Creating environment: finops'
conda create -n finops python=3.10 -y
echo '[+] Installing packages in: finops'
conda run -n finops pip install ib_insync alpaca-trade-api ccxt ta-lib finta quantstats backtrader bt pandas matplotlib yfinance zipline-reloaded
echo '[+] Creating environment: stealth-core'
conda create -n stealth-core python=3.10 -y
echo '[+] Installing packages in: stealth-core'
conda run -n stealth-core pip install watchdog pyinotify pyxhook getmac psutil loguru shodan
echo '[+] Creating environment: surveillance-stack'
conda create -n surveillance-stack python=3.10 -y
echo '[+] Installing packages in: surveillance-stack'
conda run -n surveillance-stack pip install opencv-python mediapipe face_recognition cvzone pyaudio pyttsx3 gTTS SpeechRecognition PyAV
echo '[+] Creating environment: ml-ops-deploy'
conda create -n ml-ops-deploy python=3.10 -y
echo '[+] Installing packages in: ml-ops-deploy'
conda run -n ml-ops-deploy pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
conda run -n ml-ops-deploy pip install docker kubernetes sagemaker mlflow bentoml onnx tritonclient torchserve
echo '[+] Creating environment: netsec-tools'
conda create -n netsec-tools python=3.10 -y
echo '[+] Installing packages in: netsec-tools'
conda run -n netsec-tools pip install aircrack-ng bettercap nmap wireshark tcpdump mitmproxy macchanger reaver hydra john
echo '[+] Creating environment: telemetry-ops'
conda create -n telemetry-ops python=3.10 -y
echo '[+] Installing packages in: telemetry-ops'
conda run -n telemetry-ops pip install loguru fluentd filebeat elastic-apm opentelemetry graypy
echo '[+] Creating environment: intel-recon'
conda create -n intel-recon python=3.10 -y
echo '[+] Installing packages in: intel-recon'
conda run -n intel-recon pip install shodan whois python-whois theHarvester sublist3r spyse censys
echo '[+] Creating environment: darknet-interface'
conda create -n darknet-interface python=3.10 -y
echo '[+] Installing packages in: darknet-interface'
conda run -n darknet-interface pip install stem onionshare flask-sock
echo '[+] Creating environment: ai-eval'
conda create -n ai-eval python=3.10 -y
echo '[+] Installing packages in: ai-eval'
conda run -n ai-eval pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
conda run -n ai-eval pip install torchmetrics evaluate datasets seqeval scikit-learn wandb
echo '[+] Creating environment: code-fuzz'
conda create -n code-fuzz python=3.10 -y
echo '[+] Installing packages in: code-fuzz'
conda run -n code-fuzz pip install hypothesis afl fuzzingbook mutmut pytest
echo '[+] Creating environment: base-dev'
conda create -n base-dev python=3.10 -y
echo '[+] Installing packages in: base-dev'
conda run -n base-dev pip install pip setuptools wheel build httpx poetry pipdeptree pre-commit virtualenv
