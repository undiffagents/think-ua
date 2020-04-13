import random

from think import Data, Environment, World

from .agent import PairedAssociatesAgent
from .task import PairedAssociatesTask


class PairedAssociatesSimulation:
    HUMAN_CORRECT = [.000, .526, .667, .798, .887, .924, .958, .954]
    HUMAN_RT = [.000, 2.158, 1.967, 1.762, 1.680, 1.552, 1.467, 1.402]

    def __init__(self):
        pass

    def run(self, n=10, output=False):
        corrects = Data(PairedAssociatesTask.N_BLOCKS)
        rts = Data(PairedAssociatesTask.N_BLOCKS)

        for _ in range(n):
            env = Environment()
            task = PairedAssociatesTask(env, corrects=corrects, rts=rts)
            agent = PairedAssociatesAgent(env, output=False)
            World(task, agent).run(1590)

        result_correct = corrects.analyze(self.HUMAN_CORRECT)
        result_rt = rts.analyze(self.HUMAN_RT)

        if output:
            result_correct.output("Correctness", 2)
            result_rt.output("Response Times", 2)

        return (result_correct, result_rt)
