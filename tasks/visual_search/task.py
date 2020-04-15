import random

from think import Task
from ..instructions import InstructionTaskFactory


class VisualSearchTask(Task):

    def __init__(self, env, n_targets=5):
        super().__init__()
        self.display = env.display
        self.mouse = env.mouse
        self.n_targets = n_targets

    def run(self, time):

        def handle_click(visual):
            self.display.clear()

        self.mouse.add_click_fn(handle_click)

        while self.time() < time:
            self.wait(5.0)
            self.log('stimulus')
            self.display.clear()
            target_index = random.randint(0, self.n_targets - 1)
            for i in range(self.n_targets):
                string = 'C' if i == target_index else 'O'
                self.display.add_text(random.randint(10, 90),
                                      random.randint(10, 90), string)


# class VisualSearchTaskKeyed(Task):

#     def __init__(self, env, n_targets=5):
#         super().__init__()
#         self.display = env.display
#         self.keyboard = env.keyboard
#         self.n_targets = n_targets

#     def run(self, time):

#         def handle_key(key):
#             self.display.clear()

#         self.keyboard.add_type_fn(handle_key)

#         while self.time() < time:
#             self.wait(3.0)
#             self.log('stimulus')
#             self.display.clear()
#             target_index = random.randint(0, self.n_targets)
#             for i in range(self.n_targets):
#                 string = 'C' if i == target_index else 'O'
#                 self.display.add_text(random.randint(10, 90),
#                                       random.randint(10, 90), string)


VISUAL_SEARCH_INSTRUCTIONS = [
    'To perform the task',
    'Find the "C"',
    'Move the mouse to it',
    'Click on it',
    'Repeat'
]

VISUAL_SEARCH_INSTRUCTIONS_2 = [
    'To perform the task',
    'Find the "C"',
    'Click on it',
    'Repeat'
]

VISUAL_SEARCH_INSTRUCTIONS_3 = [
    'To perform the task',
    'Click on the "C"',
]


VisualSearchInstructionTask = InstructionTaskFactory(
    VisualSearchTask,
    VISUAL_SEARCH_INSTRUCTIONS_3
)
