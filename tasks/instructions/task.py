from think import Task


def InstructionTask(task_class, instructions, machine):

    def init(self):
        task_class.__init__(self, machine)
    
    def run(self, time):
        display = machine.display
        speakers = machine.speakers

        pointer = None
        for line in instructions:
            self.wait(3.0)
            if isinstance(line, str):
                speakers.add('speech', line)
            else:
                speakers.add('speech', line[0])
                loc = line[1]
                if not pointer:
                    pointer = display.add(loc[0], loc[1], 20, 20,
                                                'pointer', 'pointer')
                else:
                    pointer.move(loc[0], loc[1])
        
        task_class.run(self, self.time() + time)

    instr_task = type('NewClass', (task_class,), {
        '__init__': init,
        'run': run,
    })

    return instr_task()
