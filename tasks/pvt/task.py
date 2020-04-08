import random

from think import Task


class PVTTask(Task):

    def __init__(self, machine):
        super().__init__()
        self.display = machine.display
        self.keyboard = machine.keyboard

    def run(self, time):

        def handle_key(key):
            self.display.clear()

        self.keyboard.add_type_fn(handle_key)

        while self.time() < time:
            self.wait(random.randint(2.0, 10.0))
            self.display.add_text(50, 50, 'X')
