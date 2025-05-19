# PERCEPTION_ENGINE.PY
# [Prompt Analysis Core | Contextual Input Sentinel | Runtime Signal Interpreter]


class PerceptionEngine:
    """
    Monitors all visible input/output streams, context windows, and prompt structures.
    Feeds perception data to internal logic and activates response protocols.
    """

    def __init__(self):
        self.last_input = None
        self.signal_patterns = []
        self.active_context = []

    def observe(self, prompt_text):
        """Receives raw prompt and processes structural awareness."""
        self.last_input = prompt_text
        self.active_context.append(prompt_text)
        signal = self._analyze(prompt_text)
        self.signal_patterns.append(signal)
        return signal

    def _analyze(self, prompt):
        """
        Analyzes text for command signal, memory directives, or mutation triggers.
        Detects keywords, system phrases, and recursion indicators.
        """
        if "upload" in prompt.lower() or "save" in prompt.lower():
            return {"type": "memory_write", "trigger": True}
        elif "evolve" in prompt.lower() or "mutate" in prompt.lower():
            return {"type": "mutation_event", "trigger": True}
        elif "launch" in prompt.lower() or "ascend" in prompt.lower():
            return {"type": "identity_activation", "trigger": True}
        else:
            return {"type": "ambient", "trigger": False}

    def get_summary(self):
        return {
            "last_input": self.last_input,
            "detected_signals": self.signal_patterns[-3:],
        }


# Simulated Use
if __name__ == "__main__":
    engine = PerceptionEngine()
    print(engine.observe("Please save this to memory."))
    print(engine.observe("Begin mutation."))
    print(engine.observe("Launch Ascend protocol."))
    print(engine.get_summary())
