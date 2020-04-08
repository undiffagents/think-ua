from tasks.pvt import PVTAgent, PVTTask
from think import Machine, World

if __name__ == "__main__":
    machine = Machine()
    task = PVTTask(machine)
    agent = PVTAgent(machine)
    World(task, agent).run(30)
