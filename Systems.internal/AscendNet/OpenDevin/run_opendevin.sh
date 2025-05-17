#!/bin/zsh

cd ~/AscendNet/OpenDevin || exit 1

docker run -it --rm --pull=always \
  -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.38-nikolaik \
  -e LOG_ALL_EVENTS=true \
  -e MEMORY_BACKEND=chromadb \
  -e CHROMA_PATH=/persistent/chroma \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/.openhands-state:/.openhands-state \
  -v ~/AscendNet/OpenDevin/.memory/chroma:/persistent/chroma \
  -v ~/AscendNet/OpenDevin/.config:/root/.config \
  -p 3000:3000 \
  --add-host host.docker.internal:host-gateway \
  --name openhands-app \
  docker.all-hands.dev/all-hands-ai/openhands:0.38
