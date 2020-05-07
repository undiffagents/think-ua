from tasks.paired_assoc import (PairedAssociatesInteractiveTask,
                                PairedAssociatesSimulation)
from ua import UndifferentiatedAgent

if __name__ == '__main__':

    UndifferentiatedAgent.KNOWLEDGE_BASE = []

    n = 1
    print('Running {} simulations...'.format(n))
    PairedAssociatesSimulation(
        task_class=PairedAssociatesInteractiveTask,
        agent_class=UndifferentiatedAgent
    ).run(n=n, output=True)
