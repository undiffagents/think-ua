from tasks.pvt import ACE_INSTRUCTIONS, PVTTask
from think import World
from ua import ACEUndifferentiatedAgent

if __name__ == "__main__":
    agent = ACEUndifferentiatedAgent()
    task = PVTTask(agent, instructions=ACE_INSTRUCTIONS)
    World(task, agent).run(100)
