from tasks.search import SearchAgent, SearchTask
from think import Environment, World

if __name__ == "__main__":
    env = Environment()
    task = SearchTask(env)
    agent = SearchAgent(env)
    World(task, agent).run(30)
