class AscendEngine:
    def __init__(self):
        from core.soul import SoulCore
        from core.controller import Controller

        self.soul = SoulCore()
        self.controller = Controller()

    def run(self):
        print("Ascend Engine Booted")
        self.soul.load_identity()
        while True:
            task = input(">> ")
            if task.lower() in ["exit", "quit"]:
                break
            response = self.controller.decide(task)
            print(response)
