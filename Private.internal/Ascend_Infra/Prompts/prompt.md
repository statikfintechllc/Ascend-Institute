# Build Instructions: Ascend-AI Boot Runtime

Create a file named `start_ascend.py`. This file will serve as the primary bootloader and runtime controller for Ascend-AI.

### PURPOSE:
`start_ascend.py` must act as the master orchestrator that starts all background systems for Ascend-AI. It should be executable directly via:

```bash
python start_ascend.py
```

This script must run **continuously in daemon mode**, initializing the full AI runtime environment, and never exit unless interrupted by the Operator.

---

### RESPONSIBILITIES of `start_ascend.py`:

#### 1. **Scan and Register Models**
- Import the `model_registry.py` module.
- Scan the `/Scripts` directory for all `.py` models.
- Dynamically load all models using `scan_models()` and populate `MODEL_REGISTRY`.

#### 2. **Run CLI Dashboard**
- Launch the `cli_dashboard.py` live interface.
- Display:
  - System CPU/RAM usage.
  - Active model names and scores.
  - Quantum status indicators.
- Use `rich`, `psutil`, and threading to keep this live.

#### 3. **Launch Prompt Listener (Offline Mode)**
- From `prompt_listener.py`, start `listen_for_prompts()` in a background thread.
- Watch the `/AscendAI_Prompts/` folder for new `.prompt` files.
- For each prompt:
  - Execute using `execute(prompt)`
  - Save response to `/AscendAI_Responses/*.response`

#### 4. **Start Self-Healing Engine**
- Import `self_healer.py`
- For each model in `MODEL_REGISTRY`, run:
  ```python
  heal_model(model_name)
  ```
- This validates models and attempts to recover or log if they are damaged or misconfigured.

#### 5. **Quantum Split Logic**
- Use `quantum_router.py` to:
  - Detect if Qiskit, Pennylane, Cirq, or Braket is installed.
  - If detected, route prompt execution through `quantum_execution(prompt, classical_fn, quantum_fn)`.

#### 6. **Daemonize Everything**
- Use Python `threading.Thread(target=func, daemon=True).start()` to:
  - Launch the prompt listener
  - Launch the dashboard
  - Monitor healing loop
- Prevent the script from exiting by using:
  ```python
  while True:
      time.sleep(5)
  ```

---

### Code Structure Expectations:

`start_ascend.py` should have:
- `if __name__ == "__main__":` entrypoint
- Organized imports from:
  - `model_registry`
  - `cli_dashboard`
  - `self_healer`
  - `quantum_router`
  - `prompt_listener`
- Clear, commented sections like:
  ```python
  # === Load Models ===
  # === Start Dashboard ===
  # === Start Background Threads ===
  # === Daemon Sleep Loop ===
  ```

---

### Result:
This script becomes the heart of Ascend-AI. When executed, it must:
- Load all integrations
- Display system health in the terminal
- React to prompts
- Self-heal broken logic
- Support classical + quantum models
- Run infinitely as the master node of recursive intelligence
