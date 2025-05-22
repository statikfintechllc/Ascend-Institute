#!/bin/zsh
# Clone required GremlinGPT repos into local project tree
cd ~/AscendNet/GremlinGPT || exit 1
echo '[+] Cloning https://github.com/karpathy/nanoGPT.git into AI_Models/nanoGPT'
git clone https://github.com/karpathy/nanoGPT.git AI_Models/nanoGPT
echo '[+] Cloning https://github.com/bigcode-project/starcoder2.git into AI_Models/StarCoder2'
git clone https://github.com/bigcode-project/starcoder2.git AI_Models/StarCoder2
echo '[+] Cloning https://github.com/CyberAgent/cyberagent-mistral.git into AI_Models/Mistral-7B-Instruct'
git clone https://github.com/CyberAgent/cyberagent-mistral.git AI_Models/Mistral-7B-Instruct
echo '[+] Cloning https://github.com/openai/whisper.git into AI_Models/whisper'
git clone https://github.com/openai/whisper.git AI_Models/whisper
echo '[+] Cloning https://github.com/hwchase17/langchain.git into AI_Modules/langchain'
git clone https://github.com/hwchase17/langchain.git AI_Modules/langchain
echo '[+] Cloning https://github.com/Chroma-Core/chroma.git into AI_Modules/chroma'
git clone https://github.com/Chroma-Core/chroma.git AI_Modules/chroma
echo '[+] Cloning https://github.com/CrewAI/CrewAI.git into AI_Modules/crewai'
git clone https://github.com/CrewAI/CrewAI.git AI_Modules/crewai
echo '[+] Cloning https://github.com/Significant-Gravitas/Auto-GPT.git into AI_Modules/autogpt'
git clone https://github.com/Significant-Gravitas/Auto-GPT.git AI_Modules/autogpt
echo '[+] Cloning https://github.com/yoheinakajima/babyagi.git into AI_Modules/babyagi'
git clone https://github.com/yoheinakajima/babyagi.git AI_Modules/babyagi
echo '[+] Cloning https://github.com/microsoft/DeepSpeed.git into AI_Modules/deepspeed'
git clone https://github.com/microsoft/DeepSpeed.git AI_Modules/deepspeed
echo '[+] Cloning https://github.com/facebookresearch/xformers.git into AI_Modules/xformers'
git clone https://github.com/facebookresearch/xformers.git AI_Modules/xformers
echo '[+] Cloning https://github.com/huggingface/transformers.git into AI_Modules/transformers'
git clone https://github.com/huggingface/transformers.git AI_Modules/transformers
