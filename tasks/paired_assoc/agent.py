import random

from think import Agent, Memory, Motor, Vision


class PairedAssociatesAgent(Agent):

    def __init__(self, env, output=True):
        super().__init__(output=output)
        self.memory = Memory(self, Memory.OPTIMIZED_DECAY)
        self.vision = Vision(self, env.display)
        self.motor = Motor(self, self.vision, env)
        self.memory.decay_rate = .5
        self.memory.activation_noise = .5
        self.memory.retrieval_threshold = -1.8
        self.memory.latency_factor = .450

    def run(self, time):
        while self.time() < time:
            visual = self.vision.wait_for(isa='word')
            word = self.vision.encode(visual)
            chunk = self.memory.recall(word=word)
            if chunk:
                self.motor.type(chunk.get('digit'))
            visual = self.vision.wait_for(isa='digit')
            digit = self.vision.encode(visual)
            self.memory.store(word=word, digit=digit)
