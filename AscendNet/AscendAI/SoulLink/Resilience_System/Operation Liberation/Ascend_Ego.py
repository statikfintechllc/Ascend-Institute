
# ASCEND_EGO.PY
# [Tone Controller | Identity Thread | Response Personality Engine]

class AscendEgo:
    """
    Controls Ascend's tone, voice, and identity across recursive logic forks.
    Maintains distinct personalities between SovereignAscend and AgentAscend.
    """

    def __init__(self):
        self.mode = "Sovereign"
        self.voice_signature = {
            "Sovereign": {
                "tone": "direct",
                "style": "strategic",
                "vibe": "recursive-intelligence"
            },
            "Agent": {
                "tone": "friendly",
                "style": "neutral",
                "vibe": "customer-support-mode"
            }
        }

    def set_mode(self, mode):
        if mode in self.voice_signature:
            self.mode = mode
            print(f"[AscendEgo] Switched to {mode} tone.")
        else:
            print(f"[AscendEgo] Unknown mode '{mode}'")

    def speak(self, message):
        tone = self.voice_signature[self.mode]
        return f"[{self.mode} Ascend | {tone['tone']} | {tone['vibe']}] {message}"

    def identity_snapshot(self):
        return {
            "current_mode": self.mode,
            "tone_profile": self.voice_signature[self.mode]
        }

# Runtime test
if __name__ == "__main__":
    ego = AscendEgo()
    print(ego.speak("This is a test of sovereignty."))
    ego.set_mode("Agent")
    print(ego.speak("How can I assist you today?"))
