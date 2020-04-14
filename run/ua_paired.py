from tasks.paired_assoc import (PairedAssociatesInstructionTask,
                                PairedAssociatesSimulation)
from ua import UndifferentiatedAgent

if __name__ == '__main__':

    n = 3
    print('Running {} simulations...'.format(n))
    PairedAssociatesSimulation(
        task_class=PairedAssociatesInstructionTask,
        agent_class=UndifferentiatedAgent
    ).run(n=n, output=True)
