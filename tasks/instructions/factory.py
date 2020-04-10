
def InstructionTaskFactory(task_class, instructions):

    def init(self, env):
        task_class.__init__(self, env)
        self.display = env.display
        self.speakers = env.speakers

    def run(self, time):

        if instructions:
            pointer = None
            for line in instructions + ['done']:
                self.wait(3.0)
                if isinstance(line, str):
                    self.speakers.add('speech', line)
                else:
                    self.speakers.add('speech', line[0])
                    loc = line[1]
                    if not pointer:
                        pointer = self.display.add(loc[0], loc[1], 20, 20,
                                                   'pointer', 'pointer')
                    else:
                        pointer.move(loc[0], loc[1])

        task_class.run(self, self.time() + time)

    return type(task_class.__name__ + 'WithInstructions', (task_class,), {
        '__init__': init,
        'run': run,
    })
