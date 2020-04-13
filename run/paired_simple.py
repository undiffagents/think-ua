from tasks.paired_assoc import PairedAssociatesAgent, PairedAssociatesTask
from think import Environment, World

if __name__ == "__main__":
    env = Environment()
    task = PairedAssociatesTask(env)
    agent = PairedAssociatesAgent(env)
    World(task, agent).run(1590)
