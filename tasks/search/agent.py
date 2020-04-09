from think import Agent, Motor, Vision


class SearchAgent(Agent):

    def __init__(self, env):
        super().__init__(output=True)
        self.vision = Vision(self, env.display)
        self.motor = Motor(self, self.vision, env)

    def run(self, time):
        while self.time() < time:
            visual = self.vision.wait_for(seen=False)
            obj = self.vision.encode(visual) if visual else None
            while visual and obj != 'C':
                visual = self.vision.find(seen=False)
                obj = self.vision.encode(visual) if visual else None
            if obj == 'C':
                self.log('target found')
                self.motor.type('j')
                self.vision.encode(visual)
            else:
                self.log('target not found')
                self.motor.type('k')
