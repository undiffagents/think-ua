import random

from think import (Agent, Audition, Aural, Hands, Instruction, Item, Language,
                   Memory, Query, Task, Typing, Vision, Visual, World)

from ua import UndifferentiatedAgent


class Trace:

    def __init__(self, process):
        self.process = process
        self.events = []

    def add(self, event):
        self.events.append((self.process.time(), event))
        print('{:>12.3f}\t{}'.format(self.process.time(), event))


class PVT(Task):
    """Psychomotor Vigilance Task"""

    def __init__(self, agent):
        super().__init__(agent)
        self.vision = self.agent.vision
        self.audition = self.agent.audition
        self.typing = self.agent.typing

    def run(self, time=300):
        """Builds and runs the test agent and task"""
        trace = Trace(self)
        stimulus = None

        def handle_key(key):
            self.vision.remove(stimulus)
            trace.add('response')
        self.typing.add_type_fn(handle_key)

        instructions = [
            'to pvt',
            'Psychomotor-Vigilance is a task X1.',
            'Acknowledge is a button X2.',
            # 'X1 has a box X3 and a target X4.',
            'X1 has a box X3.',
            'X1 has a target X4.',
            'X4 is a letter X5.',
            'If X4 appears in X3 then a subject X6 clicks X2 and X6 remembers X5.',
            'If X1 is active then X4 appears in X3.',
        ]
        for line in instructions:
            self.wait(5.0)
            if isinstance(line, str):
                self.audition.add(Aural(isa='speech'), line)
            else:
                self.audition.add(Aural(isa='speech'), line[0])
                loc = line[1]
                # pointer.move(loc[0], loc[1])

        while self.time() < time:
            self.wait(random.randint(2.0, 10.0))
            stimulus = Visual(50, 50, 20, 20, 'stimulus')
            self.vision.add(stimulus, '*')
            trace.add('stimulus')

        print(trace)


if __name__ == "__main__":
    agent = UndifferentiatedAgent()
    task = PVT(agent)
    World(agent, task).run(300)
