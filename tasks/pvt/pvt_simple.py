import random

from think import Agent, Hands, Task, Typing, Vision, Visual, World


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
        self.typing = self.agent.typing

    def run(self, time=10):
        """Builds and runs the test agent and task"""
        trace = Trace(self)
        stimulus = None

        def handle_key(key):
            self.vision.remove(stimulus)
            trace.add('response')
        self.typing.add_type_fn(handle_key)

        while self.time() < time:
            self.wait(random.randint(2.0, 10.0))
            stimulus = Visual(50, 50, 20, 20, 'stimulus')
            self.vision.add(stimulus, '*')
            trace.add('stimulus')

        return trace


class PVTAgent(Agent):

    def __init__(self):
        """Initializes the agent"""
        super().__init__(output=True)
        self.vision = Vision(self)
        self.typing = Typing(Hands(self))

    def run(self, time=300):
        while self.time() < time:
            visual = self.vision.wait_for(seen=False)
            self.vision.start_encode(visual)
            self.typing.type('j')
            self.vision.get_encoded()


if __name__ == "__main__":
    agent = PVTAgent()
    task = PVT(agent)
    World(task, agent).run(30)
