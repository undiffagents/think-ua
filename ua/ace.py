from urllib import parse, request
from xml.dom import minidom
from xml.etree import ElementTree

from think import (Agent, Audition, Aural, Hands, Instruction, Item, Language,
                   Memory, Query, Typing, Vision, Visual)


class ACEUndifferentiatedAgent(Agent):

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

    def _ace_to_owl(self, text):
        """Converts ACE instruction text to OWL XML using the web API"""
        url = 'http://attempto.ifi.uzh.ch/ws/ape/apews.perl'
        params = {
            'text': text,
            'guess': 'on',
            # 'solo': 'owlxml',
            'cdrs': 'on',
            'cowlxml': 'on',
        }
        data = parse.urlencode(params).encode()
        req = request.Request(url, parse.urlencode(params).encode())
        res = request.urlopen(req)
        xml_string = res.read().decode('utf-8')
        print(xml_string)
        xml = ElementTree.fromstring(xml_string)
        print(xml)
        # print(ElementTree.tostring(xml, encoding='utf8', method='xml'))

    def interpret(self, words):
        self._ace_to_owl(' '.join(words))
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

    def execute(self, action, context):
        if action.type == 'read':
            query = Query(x=action.x, y=action.y)
            context.set(action.object, self.vision.find_and_encode(query))
        elif action.type == 'type':
            self.typing.type(context.get(action.object))

    def run(self, time=300):
        goal = self.instruction.listen_and_learn()
        self.instruction.execute(goal)
