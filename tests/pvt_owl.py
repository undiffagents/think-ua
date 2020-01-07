from tasks.pvt import OWL_INSTRUCTIONS, PVTTask
from think import World
from ua import OWLUndifferentiatedAgent

if __name__ == "__main__":
    agent = OWLUndifferentiatedAgent()
    task = PVTTask(agent, instructions=OWL_INSTRUCTIONS)
    World(task, agent).run(100)
