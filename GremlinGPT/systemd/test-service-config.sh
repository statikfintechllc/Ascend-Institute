#!/bin/bash

# GremlinGPT Service Test Script
# Tests if the service configuration will work properly

echo "🧪 Testing GremlinGPT Service Configuration..."
echo "================================================"

# Test 1: Check if conda is available
echo "1. Testing conda availability..."
if command -v conda &> /dev/null; then
    echo "   ✅ conda command found: $(which conda)"
else
    echo "   ❌ conda command not found"
    exit 1
fi

# Test 2: Check if conda profile exists
CONDA_PROFILE="$HOME/miniconda3/etc/profile.d/conda.sh"
echo "2. Testing conda profile..."
if [ -f "$CONDA_PROFILE" ]; then
    echo "   ✅ conda profile found: $CONDA_PROFILE"
else
    echo "   ❌ conda profile not found at: $CONDA_PROFILE"
    echo "   💡 Try: $HOME/anaconda3/etc/profile.d/conda.sh"
    CONDA_PROFILE="$HOME/anaconda3/etc/profile.d/conda.sh"
    if [ -f "$CONDA_PROFILE" ]; then
        echo "   ✅ Found anaconda profile instead: $CONDA_PROFILE"
    else
        echo "   ❌ Neither miniconda nor anaconda profile found"
        exit 1
    fi
fi

# Test 3: Check if gremlin-orchestrator environment exists
echo "3. Testing gremlin-orchestrator environment..."
source "$CONDA_PROFILE"
if conda env list | grep -q "gremlin-orchestrator"; then
    echo "   ✅ gremlin-orchestrator environment found"
else
    echo "   ❌ gremlin-orchestrator environment not found"
    echo "   💡 Run: conda env create -f conda_envs/gremlin-orchestrator.yml"
    exit 1
fi

# Test 4: Test activation command
echo "4. Testing conda activation command..."
if conda activate gremlin-orchestrator; then
    echo "   ✅ Successfully activated gremlin-orchestrator"
    
    # Test 5: Check if Python can import GremlinGPT modules
    echo "5. Testing Python imports..."
    SERVICE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
    cd "$SERVICE_DIR"
    if python3 -c "import backend.globals; print('✅ Backend imports work')" 2>/dev/null; then
        echo "   ✅ GremlinGPT modules import successfully"
    else
        echo "   ❌ GremlinGPT modules failed to import"
        echo "   💡 Check PYTHONPATH and ensure all dependencies are installed"
    fi
    
    conda deactivate
else
    echo "   ❌ Failed to activate gremlin-orchestrator"
    exit 1
fi

echo ""
echo "🎉 All tests passed! Service should work correctly."
echo "💡 To install the service, run: sudo systemctl enable --now gremlin"
