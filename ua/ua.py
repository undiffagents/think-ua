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

    def interpreter(self, words):
        if words[0] == 'read':
            sem = Item(isa='action', type='read', object=words[1])
            pointer = self.vision.find(isa='pointer')
            if pointer is not None:
                self.vision.encode(pointer)
                sem.set('x', pointer.x).set('y', pointer.y)
            return sem
        elif words[0] == 'done':
            return Item(isa='done')
        else:
            return Item(isa='action', type=words[0], object=words[1])

    def executor(self, action, context):
        if action.type == 'read':
            query = Query(x=action.x, y=action.y)
            context.set(action.object, self.vision.find_and_encode(query))
        elif action.type == 'type':
            self.typing.type(context.get(action.object))

    def run(self, time=60):
        goal = self.instruction.listen_and_learn()
        self.instruction.execute(goal)
