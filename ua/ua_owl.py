import re
from urllib import parse, request
from xml.dom import minidom
from xml.etree import ElementTree

from think import (Agent, Audition, Aural, Chunk, Hands, Instruction, Item,
                   Language, Memory, Query, Typing, Vision, Visual)


def _chunk_multiset(chunk, prefix, vals):
    i = 1
    for val in vals:
        chunk.set(prefix + str(i), val)
        i += 1
    return chunk


def _chunk_multiget(chunk, prefix):
    vals = []
    i = 1
    while chunk.has(prefix + str(i)):
        print(chunk.get(prefix + str(i)))
        vals.append(chunk.get(prefix + str(i)))
        i += 1
    return vals


class UndifferentiatedAgent(Agent):

    def __init__(self):
        """Initializes the agent"""
        super().__init__(output=True)
        self.memory = Memory(self)
        self.vision = Vision(self)
        self.audition = Audition(self)
        self.typing = Typing(Hands(self))

        self.language = Language(self)
        self.language.add_interpreter(self.interpret)

        self.instruction = Instruction(
            self, self.memory, self.audition, self.language)
        self.instruction.add_executor(self.execute)

    def _interpret_fact(self, text):
        chunk = None
        text = text.replace(' ', '')
        m = re.search(r'([A-Za-z_-]+)\(([^)]*)\)', text)
        prop = m.group(1)
        objs = m.group(2).split(',')
        if len(objs) == 1:
            chunk = Chunk(isa='fact', property='isa', subject=objs[0], object=prop)
        elif len(objs) == 2:
            chunk = Chunk(isa='fact', property=prop, subject=objs[0], object=objs[1])
        if chunk:
            self.memory.add(chunk)
        return chunk

    def _interpret_conditional(self, text):
        cond = Chunk(isa='conditional')
        lhs, rhs = text.replace(' ', '').split('=>')
        _chunk_multiset(cond, 'if',
                        [self._interpret_fact(t) for t in re.findall(r'[A-Za-z_-]+\([A-Za-z_,-]*\)', lhs)])
        _chunk_multiset(cond, 'then',
                        [self._interpret_fact(t) for t in re.findall(r'[A-Za-z_-]+\([A-Za-z_,-]*\)', rhs)])
        self.memory.add(cond)
        return cond

    def _interpret_owl(self, text):
        if text.find('=>') >= 0:
            return self._interpret_conditional(text)
        else:
            return self._interpret_fact(text)

    def interpret(self, words):
        return self._interpret_owl(''.join(words))

        # if words[0] == 'read':
        #     sem=Item(isa='action', type='read', object=words[1])
        #     pointer=self.vision.find(isa='pointer')
        #     if pointer is not None:
        #         self.vision.encode(pointer)
        #         sem.set('x', pointer.x).set('y', pointer.y)
        #     return sem
        # elif words[0] == 'done':
        #     return Item(isa='done')
        # else:
        #     return Item(isa='action', type=words[0], object=words[1])

    def _execute_if(self, chunk, context):
        if chunk.property == 'appearsIn':
            visual = self.vision.find(isa=chunk.object, seen=False)
            if visual:
                visobj = self.vision.encode(visual)
                context.set(chunk.object, visobj)
        return True

    def _execute_then(self, chunk, context):
        if chunk.subject == 'Subject':
            print('**************  ' + chunk.property)

    def execute(self, chunk, context):
        if chunk.isa == 'conditional':
            for if_chunk in _chunk_multiget(chunk, 'if'):
                self.memory.recall(if_chunk)
                if not self._execute_if(if_chunk, context):
                    return False
            for then_chunk in _chunk_multiget(chunk, 'then'):
                self.memory.recall(then_chunk)
                self._execute_then(then_chunk, context)
            return True

        # if action.type == 'read':
        #     query=Query(x=action.x, y=action.y)
        #     context.set(action.object, self.vision.find_and_encode(query))
        # elif action.type == 'type':
        #     self.typing.type(context.get(action.object))

    def run(self, time=300):
        context = Item()

        chunk = None
        done = Query(property='isa', object='done')
        while not (chunk and done.matches(chunk)):
            text = self.audition.listen_for_and_encode()
            chunk = self.language.interpret(text)
            # self.execute(chunk, context)

        while self.time() < time:
            chunk = self.memory.recall(isa='conditional')
            print(chunk)
            self.execute(chunk, context)

        # goal = self.instruction.listen_and_learn()
        # self.instruction.execute(goal)
