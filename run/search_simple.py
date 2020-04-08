from tasks.search import SearchAgent, SearchTask
from think import Machine, World

if __name__ == "__main__":
    machine = Machine()
    task = SearchTask(machine)
    agent = SearchAgent(machine)
    World(task, agent).run(30)
