from tasks.visual_search import VisualSearchInstructionTask
from think import Environment, World
from ua import UndifferentiatedAgent

if __name__ == "__main__":
    env = Environment()
    # env = Environment(window=(500, 500))
    task = VisualSearchInstructionTask(env)
    agent = UndifferentiatedAgent(env)
    World(task, agent).run(30)
    # World(task, agent).run(30, real_time=True)
