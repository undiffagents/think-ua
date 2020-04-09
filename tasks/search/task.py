import random

from think import Task


class SearchTask(Task):

    def __init__(self, env, n_targets=5):
        super().__init__()
        self.display = env.display
        self.keyboard = env.keyboard
        self.n_targets = n_targets

    def run(self, time):

        def handle_key(key):
            self.display.clear()

        self.keyboard.add_type_fn(handle_key)

        while self.time() < time:
            self.wait(3.0)
            self.display.clear()
            target_index = random.randint(0, self.n_targets)
            for i in range(self.n_targets):
                string = 'C' if i == target_index else 'O'
                self.display.add_text(random.randint(10, 90),
                                      random.randint(10, 90), string)
