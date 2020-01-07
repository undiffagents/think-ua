import random

from think import (Agent, Audition, Aural, Hands, Instruction, Item, Language,
                   Memory, Query, Task, Typing, Vision, Visual, World)


class PVTTrace:

    def __init__(self, process):
        self.process = process
        self.events = []

    def add(self, event):
        self.events.append((self.process.time(), event))
        print('{:>12.3f}\t{}'.format(self.process.time(), event))


class PVTTask(Task):
    """Psychomotor Vigilance Task"""

    def __init__(self, agent, instructions=[]):
        super().__init__(agent)
        self.vision = self.agent.vision
        self.audition = self.agent.audition
        self.typing = self.agent.typing
        self.instructions = instructions

    def run(self, time=10):
        """Builds and runs the test agent and task"""
        trace = PVTTrace(self)
        stimulus = None

        def handle_key(key):
            self.vision.remove(stimulus)
            trace.add('response')

        self.typing.add_type_fn(handle_key)

        for line in self.instructions:
            self.wait(5.0)
            if isinstance(line, str):
                self.audition.add(Aural(isa='speech'), line)
            else:
                self.audition.add(Aural(isa='speech'), line[0])
                loc = line[1]
                # pointer.move(loc[0], loc[1])

        while self.time() < time:
            self.wait(random.randint(2.0, 10.0))
            stimulus = Visual(50, 50, 20, 20, 'Letter')
            self.vision.add(stimulus, 'A')
            trace.add('Target')

        return trace
