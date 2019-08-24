import re
from urllib import parse, request
from xml.dom import minidom
from xml.etree import ElementTree

from think import (Agent, Audition, Aural, Chunk, Hands, Instruction, Item,
                   Language, Memory, Mouse, Query, Typing, Vision, Visual)


class UndifferentiatedAgent(Agent):

    def __init__(self):
        """Initializes the agent"""
        super().__init__(output=True)
        self.memory = Memory(self)
        self.vision = Vision(self)
        self.audition = Audition(self)
        self.hands = Hands(self)
        self.mouse = Mouse(self.hands, self.vision)
        self.typing = Typing(self.hands)

        self.language = Language(self)
        self.language.add_interpreter(self.interpret)

        # self.instruction = Instruction(
        #     self, self.memory, self.audition, self.language)
        # self.instruction.add_executor(self.execute)

    def _interpret_fact(self, text):
        chunk = None
        m = re.search(r'([A-Za-z_-]+)\(([^)]*)\)', text)
        pred = m.group(1)
        args = m.group(2).split(',')
        if len(args) == 1:
            chunk = Chunk(isa='fact', predicate='isa',
                          subject=args[0], object=pred)
        elif len(args) == 2:
            chunk = Chunk(isa='fact', predicate=pred,
                          subject=args[0], object=args[1])
        if chunk:
            self.memory.add(chunk)
        return chunk

    def _interpret_conditional(self, text):
        lhs, rhs = text.split('=>')
        ifs = [self._interpret_fact(t) for t in re.findall(
            r'[A-Za-z_-]+\([A-Za-z_,-]*\)', lhs)]
        thens = [self._interpret_fact(t) for t in re.findall(
            r'[A-Za-z_-]+\([A-Za-z_,-]*\)', rhs)]
        cond = Chunk(isa='conditional', ifs=ifs, thens=thens)
        self.memory.add(cond)
        return cond

    def _interpret_owl(self, text):
        text = text.replace(' ', '')
        if text.find('=>') >= 0:
            return self._interpret_conditional(text)
        else:
            return self._interpret_fact(text)

    def interpret(self, words):
        return self._interpret_owl(''.join(words))

    def _deep_find(self, isa):
        visual = self.vision.find(isa=isa, seen=False)
        if visual:
            return visual
        else:
            part_of = self.memory.recall(predicate='isPartOf', object=isa)
            if part_of:
                return self._deep_find(part_of.subject)
            else:
                return None

    def _execute_if(self, chunk, context):
        if chunk.predicate == 'appearsIn':
            visual = self._deep_find(chunk.subject)
            if visual:
                context.set('visual', visual)
                visobj = self.vision.encode(visual)
                context.set(chunk.subject, visobj)
                return True
        return False

    def _execute_then(self, chunk, context):
        if chunk.subject == 'Subject':
            action = chunk.predicate
            print('**************  ' + action)

            if action == 'click':
                visual = context.get('visual')
                self.mouse.point_and_click(visual)

            elif action == 'remember':
                pass

    def execute(self, chunk, context):
        if chunk.isa == 'conditional':
            for if_chunk in chunk.ifs:
                self.memory.recall_by_id(if_chunk.id)
                if not self._execute_if(if_chunk, context):
                    return False
            for then_chunk in chunk.thens:
                self.memory.recall_by_id(then_chunk.id)
                self._execute_then(then_chunk, context)
            return True

    def run(self, time=300):
        context = Item()

        chunk = None
        done = Query(predicate='isa', object='done')
        while not (chunk and done.matches(chunk)):
            text = self.audition.listen_for_and_encode()
            chunk = self.language.interpret(text)

        while self.time() < time:
            chunk = self.memory.recall(isa='conditional')
            print(chunk)
            self.execute(chunk, context)
