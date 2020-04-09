from tasks.instructions import InstructionTask
from tasks.pvt import PVTAgent, PVTTask
from think import Machine, World

INSTRUCTIONS = [
    'to perform-task',
    'wait-for stimulus',
    # ['read stimulus', (50, 50)],
    'press "j"',
    'done'
]

if __name__ == "__main__":
    machine = Machine()
    task = InstructionTask(PVTTask, INSTRUCTIONS, machine)
    agent = PVTAgent(machine)
    World(task, agent).run(30)
