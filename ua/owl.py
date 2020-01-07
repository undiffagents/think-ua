import re
from urllib import parse, request
from xml.dom import minidom
from xml.etree import ElementTree

from think import (Agent, Audition, Aural, Chunk, Hands, Item, Language,
                   Memory, Mouse, Query, Typing, Vision)


# class InstructionChunk:

#     def __init__(self, query, fn):
#         self.query = query
#         self.fn = fn

#     def execute(self):
#         pass


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

    def _interpret_predicate(self, text, isa='fact', last=None):
        chunk = None
        (pred, args) = text.replace(')', '').split('(')
        args = args.split(',')
        if len(args) == 1:
            chunk = Chunk(isa=isa, predicate='isa',
                          subject=args[0], object=pred)
        elif len(args) == 2:
            chunk = Chunk(isa=isa, predicate=pred,
                          subject=args[0], object=args[1])
        if chunk:
            if last:
                chunk.set('last', last.id)
            self.memory.store(chunk)
        return chunk

    def _interpret_rule(self, text):
        lhs, rhs = text.split('=>')
        pred_pat = re.compile(r'[A-Za-z_-]+\([A-Za-z_,-]*\)')

        rule = Chunk(isa='rule')
        self.memory.store(rule)

        last = rule
        for t in pred_pat.findall(lhs):
            chunk = self._interpret_predicate(t, isa='condition', last=last)
            last = chunk

        last = rule
        for t in pred_pat.findall(rhs):
            chunk = self._interpret_predicate(t, isa='action', last=last)
            last = chunk

        return rule

    def _interpret_owl(self, text):
        text = text.replace(' ', '')
        if text.find('=>') >= 0:
            return self._interpret_rule(text)
        else:
            return self._interpret_predicate(text)

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

    def _execute_condition(self, cond, context):
        if cond.predicate == 'appearsIn':
            visual = self._deep_find(cond.subject)
            if visual:
                context.set('visual', visual)
                visobj = self.vision.encode(visual)
                context.set(cond.subject, visobj)
                return True
        return False

    def _execute_action(self, action, context):
        if action.subject == 'Subject':
            print('**************  ' + action.predicate)

            if action.predicate == 'click':
                visual = context.get('visual')
                self.mouse.point_and_click(visual)

            elif action.predicate == 'remember':
                pass

    def execute(self, chunk, context):
        if chunk.isa == 'rule':

            cond = self.memory.recall(isa='condition', last=chunk.id)
            while cond:
                if not self._execute_condition(cond, context):
                    return False
                cond = self.memory.recall(isa='condition', last=cond.id)

            act = self.memory.recall(isa='action', last=chunk.id)
            while act:
                self._execute_action(act, context)
                act = self.memory.recall(isa='action', last=act.id)

            return True

    def run(self, time=300):
        context = Item()

        chunk = None
        done = Query(predicate='isa', object='done')
        while not (chunk and done.matches(chunk)):
            text = self.audition.listen_for_and_encode()
            chunk = self.language.interpret(text)

        while self.time() < time:
            chunk = self.memory.recall(isa='rule')
            self.execute(chunk, context)
