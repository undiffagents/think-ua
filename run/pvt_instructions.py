from tasks.instructions import InstructionTask
from tasks.pvt import PVTAgent, PVTTask
from think import Environment, World

INSTRUCTIONS = [
    'to perform-task',
    'wait-for stimulus',
    # ['read stimulus', (50, 50)],
    'press "j"',
    'done'
]

if __name__ == "__main__":
    env = Environment()
    task = InstructionTask(PVTTask, INSTRUCTIONS, env)
    agent = PVTAgent(env)
    World(task, agent).run(30)
