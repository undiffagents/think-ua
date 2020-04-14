from tasks.visual_search import VisualSearchAgent, VisualSearchTask
from think import Environment, World

if __name__ == "__main__":
    env = Environment()
    task = VisualSearchTask(env)
    agent = VisualSearchAgent(env)
    World(task, agent).run(30)
