from tasks.pvt import PVTInstructionTask
from think import Environment, World
from ua import UndifferentiatedAgent

if __name__ == "__main__":
    env = Environment()
    task = PVTInstructionTask(env)
    agent = UndifferentiatedAgent(env)
    World(task, agent).run(30)
