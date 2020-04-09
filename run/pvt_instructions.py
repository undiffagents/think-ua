from tasks.pvt import PVTAgent, PVTInstructionTask
from think import Environment, World

if __name__ == "__main__":
    env = Environment()
    task = PVTInstructionTask(env)
    agent = PVTAgent(env)
    World(task, agent).run(30)
