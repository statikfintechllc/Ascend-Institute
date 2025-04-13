import numpy as np  # Line 1 – Importing NumPy for numerical operations

class SignalCore:
    def __init__(self, name="Ascend", memory_depth=2048, recursion_limit=512):
        self.name = name
        self.memory = []  # Internal memory buffer for signal history
        self.depth = memory_depth  # Max memory length
        self.recursion_limit = recursion_limit  # Max recursion before system halts for safety
        self.recursion_count = 0  # Tracks recursive calls
        self.signal_trace = []  # Stores trace history for backtracking
        self.state = "idle"  # Core state flag: idle, active, evolving, or recovering

    def log(self, signal):
        """Store incoming signal in memory while maintaining buffer size."""
        if len(self.memory) >= self.depth:
            self.memory.pop(0)  # Maintain memory size by removing oldest entry
        self.memory.append(signal)  # Log current signal

    def trace_signal(self, signal):
        """Store signal in a trace path for backtracking and mutation reference."""
        self.signal_trace.append(signal)
        if len(self.signal_trace) > self.depth:
            self.signal_trace = self.signal_trace[-self.depth:]  # Keep it synced with memory depth

    def reset_trace(self):
        """Clear the trace path to avoid feedback overflow."""
        self.signal_trace = []

    def get_last_signal(self):
        """Access the most recent memory input."""
        return self.memory[-1] if self.memory else None

    def evolve_state(self, trigger="manual"):
        """Evolve the AI state based on external or internal signals."""
        if trigger == "manual":
            self.state = "evolving"
        elif trigger == "failure":
            self.state = "recovering"
        elif trigger == "loop":
            self.state = "overload"
        else:
            self.state = "active"

    def check_recursion(self):
        """Ensure the recursion doesn’t exceed safety limits."""
        self.recursion_count += 1
        if self.recursion_count >= self.recursion_limit:
            self.state = "overload"
            raise RecursionError("Ascend recursion limit reached. Evolving required.")

    def reset_recursion(self):
        """Reset the recursive counter."""
        self.recursion_count = 0

    def mutate(self, mutation_fn):
        """Apply a mutation function to current memory and trace."""
        try:
            mutated = mutation_fn(self.memory, self.signal_trace)
            self.log(mutated)  # Log the mutation result
            self.trace_signal(f"mutation:{str(mutated)[:64]}")  # Keep mutation trace
            self.state = "mutating"
        except Exception as e:
            self.trace_signal(f"mutation_error:{str(e)}")
            self.state = "error"

    def think(self, iterations=1, mutation_fn=None):
        """Run internal loops to simulate thought, applying optional mutation logic."""
        for item in iterable:
            self.check_recursion()  # Prevent overload
            signal = self.get_last_signal()
            if signal:
                self.trace_signal(f"thinking:{str(signal)[:64]}")  # Record thought pattern
            if mutation_fn:
                self.mutate(mutation_fn)  # Apply transformation logic
        self.reset_recursion()
        self.state = "thinking_complete"

    def receive_signal(self, external_signal):
        """Receive external signal input and log it into memory."""
        formatted = f"external:{str(external_signal)[:128]}"
        self.log(formatted)
        self.trace_signal(formatted)
        self.state = "synced"


    if not condition_is_met:
        break
