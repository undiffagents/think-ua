from urllib import parse, request
from xml.dom import minidom
from xml.etree import ElementTree

from think import (Agent, Audition, Aural, Instruction, Item, Language,
                   Environment, Memory, Motor, Query, Vision, Visual)


class UndifferentiatedAgent(Agent):

    def __init__(self, env):
        """Initializes the agent"""
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

    def _ace_to_owl(self, text):
        """Converts ACE instruction text to OWL XML using the web API"""
        url = 'http://attempto.ifi.uzh.ch/ws/ape/apews.perl'
        params = {'text': text, 'solo': 'owlxml'}
        data = parse.urlencode(params).encode()
        req = request.Request(url, parse.urlencode(params).encode())
        res = request.urlopen(req)
        xml_string = res.read().decode('utf-8')
        print(xml_string)
        xml = ElementTree.fromstring(xml_string)
        print(xml)
        # print(ElementTree.tostring(xml, encoding='utf8', method='xml'))

    def interpreter(self, words):
        """Provides interpreters that convert words to semantic units"""
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

    def executor(self, action, context):
        """Provides executors that take semantic actions + context and executes them"""
        if action.type == 'read':
            query = Query(x=action.x, y=action.y)
            context.set(action.object, self.vision.find_and_encode(query))
        elif action.type == 'type':
            self.typing.type(context.get(action.object))


class ExampleTask:

    def run(self, agent):
        """Builds and runs the test agent and task"""

        vision = agent.vision
        audition = agent.audition
        typing = agent.typing
        instruction = agent.instruction

        typed = []

        def type_handler(key):
            typed.append(key)
        typing.add_type_fn(type_handler)

        # add a visual stimulus "a" and a pointer pointing to it
        vision.add(Visual(50, 50, 20, 20, 'text'), 'a')
        pointer = Visual(50, 50, 1, 1, 'pointer')
        vision.add(pointer, 'pointer')

        # create the ACE instruction text
        ace_instructions = [
            'to perform_task',
            'Psychomotor-Vigilance has a box and a target that is a letter.',
            'Acknowledge is a button.',
            'If Psychomotor-Vigilance is active then a letter appears in the box of Psychomotor-Vigilance.',
            'If the target of Psychomotor-Vigilance appears in the box of Psychomotor-Vigilance then the subject remembers the letter and clicks Acknowledge.',
            # ['read letter', (50, 50)],
            'done'
        ]

        # start a thread that presents the instructions via speech every 3
        # seconds
        def stimulus_thread():
            for line in ace_instructions:
                agent.wait(3.0)
                if isinstance(line, str):
                    # if it's just a string, create a speech stimulus
                    audition.add(Aural(isa='speech'), line)
                else:
                    # if it's a string + pointer location,
                    # move the pointer there and create a speech stimulus
                    audition.add(Aural(isa='speech'), line[0])
                    loc = line[1]
                    pointer.move(loc[0], loc[1])
        agent.run(stimulus_thread)

        # on the main thread, start the instruction-following process
        goal = instruction.listen_and_learn()
        instruction.execute(goal)

        # wait for all processes to finish (both the stimuli and the agent)
        agent.wait_for_all()
        print(typed)


if __name__ == "__main__":
    ExampleTask().run(UndifferentiatedAgent())
