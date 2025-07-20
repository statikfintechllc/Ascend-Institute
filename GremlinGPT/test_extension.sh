#!/bin/bash

echo "🧪 Testing GremlinGPT VS Code Extension..."

# Test 1: Check if extension is installed
echo "1. Checking extension installation..."
if code --list-extensions | grep -q "statikfintechllc.gremlingpt"; then
    echo "✅ Extension is installed"
else
    echo "❌ Extension not found"
    exit 1
fi

# Test 2: Check conda environments
echo "2. Checking conda environments..."
missing_envs=()
for env in gremlin-orchestrator gremlin-dashboard gremlin-memory gremlin-nlp gremlin-scraper; do
    if ! conda env list | grep -q "$env"; then
        missing_envs+=("$env")
    fi
done

if [ ${#missing_envs[@]} -eq 0 ]; then
    echo "✅ All conda environments exist"
else
    echo "❌ Missing environments: ${missing_envs[*]}"
    echo "Run: ./conda_envs/create_envs.sh"
    exit 1
fi

# Test 3: Check if compiled extension exists
echo "3. Checking compiled extension..."
if [ -f ~/.vscode/extensions/statikfintechllc.gremlingpt-1.0.3/out/extension.js ]; then
    echo "✅ Compiled extension found"
else
    echo "❌ Compiled extension missing"
    exit 1
fi

# Test 4: Test conda activation
echo "4. Testing conda activation..."
if source $HOME/miniconda3/etc/profile.d/conda.sh && conda activate gremlin-orchestrator; then
    echo "✅ Conda activation works"
    conda deactivate
else
    echo "❌ Conda activation failed"
    exit 1
fi

echo ""
echo "🎉 Extension test passed! Ready to use:"
echo ""
echo "1. Open VS Code: code /home/statiksmoke8/Ascend-Institute/GremlinGPT"
echo "2. Press Ctrl+Shift+P"
echo "3. Type: GremlinGPT: Start System"
echo "4. Press Enter"
echo ""
echo "Available commands:"
echo "- GremlinGPT: Start System"
echo "- GremlinGPT: Stop System"  
echo "- GremlinGPT: Open Dashboard"
echo "- GremlinGPT: Memory Management"
echo "- GremlinGPT: Trading Panel"
echo "- GremlinGPT: GremlinGPT Terminal"
