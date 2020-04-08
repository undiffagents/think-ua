from tasks.pvt import DRS_INSTRUCTIONS, PVTTask
from think import World
from ua import DRSUndifferentiatedAgent

if __name__ == "__main__":
    agent = DRSUndifferentiatedAgent()
    task = PVTTask(agent, instructions=DRS_INSTRUCTIONS)
    World(task, agent).run(100)
