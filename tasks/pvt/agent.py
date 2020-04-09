from think import Agent, Motor, Vision


class PVTAgent(Agent):

    def __init__(self, env):
        super().__init__(output=True)
        self.vision = Vision(self, env.display)
        self.motor = Motor(self, self.vision, env)

    def run(self, time):
        while self.time() < time:
            visual = self.vision.wait_for(seen=False)
            self.vision.start_encode(visual)
            self.motor.type('j')
            self.vision.get_encoded()
