import unittest
from tasks.paired_assoc import (PairedAssociatesInstructionTask,
                                PairedAssociatesSimulation)
from ua import UndifferentiatedAgent


class TestUAPaired(unittest.TestCase):

    def test_ua_paired(self, output=False):
        n = 3
        print('Running {} simulations...'.format(n))
        sim = PairedAssociatesSimulation(
            task_class=PairedAssociatesInstructionTask,
            agent_class=UndifferentiatedAgent
        )
        res_corr, res_rt = sim.run(n=n, output=False)
        print(res_rt)
