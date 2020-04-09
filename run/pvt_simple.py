from tasks.pvt import PVTAgent, PVTTask
from think import Environment, World

if __name__ == "__main__":
    env = Environment()
    task = PVTTask(env)
    agent = PVTAgent(env)
    World(task, agent).run(30)
