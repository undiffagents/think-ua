from tasks.paired_assoc import PairedAssociatesInstructionTask
from think import Environment, World
from ua import UndifferentiatedAgent

if __name__ == '__main__':
    env = Environment()
    task = PairedAssociatesInstructionTask(env)
    agent = UndifferentiatedAgent(env)
    World(task, agent).run(100)
