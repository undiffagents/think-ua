from think import (Agent, Audition, Aural, Environment, Instruction, Item,
                   Language, Memory, Motor, Query, Vision, Visual)


class UndifferentiatedAgent(Agent):

    def __init__(self, env):
        super().__init__(output=True)
        self.memory = Memory(self)
        self.vision = Vision(self, env.display)
        self.audition = Audition(self, env.speakers)
        self.motor = Motor(self, self.vision, env)

        self.language = Language(self)
        self.language.add_interpreter(lambda w: self.interpreter(w))

        self.instruction = Instruction(
            self, self.memory, self.audition, self.language)
        self.instruction.add_executor(lambda a, c: self.executor(a, c))

        self.time_limit = None

    def interpreter(self, words):
        print(words)
        if words[0] == 'read':
            sem = Item(isa='action', type='read', object=words[1])
            pointer = self.vision.find(isa='pointer')
            if pointer is not None:
                self.vision.encode(pointer)
                sem.set('x', pointer.x).set('y', pointer.y)
            return sem
        elif words[0] == 'done':
            return Item(isa='done')
        elif len(words) > 1:
            return Item(isa='action', type=words[0], object=words[1])
        else:
            print(words[0])
            return Item(isa='action', type=words[0])

    def executor(self, action, context):
        if action.type == 'wait-for':
            visual = self.vision.wait_for()
            context.set(action.object, self.vision.encode(visual))
        elif action.type == 'read':
            query = Query(x=action.x, y=action.y)
            context.set(action.object, self.vision.find_and_encode(query))
        elif action.type == 'type' or action.type == 'press':
            text = (action.object[1:-1]
                    if action.object.startswith('"')
                    else context.get(action.object))
            self.motor.type(text)
        elif action.type == 'repeat':
            if (not self.time_limit) or self.time() < self.time_limit:
                self.instruction.execute(self.goal)

    def run(self, time):
        self.goal = self.instruction.listen_and_learn()
        self.time_limit = self.time() + time
        self.instruction.execute(self.goal)
