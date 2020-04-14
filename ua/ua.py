from think import (Agent, Audition, Aural, Chunk, Environment, Instruction,
                   Item, Language, Memory, Motor, Query, Vision, Visual)

KNOWLEDGE_BASE = [
    Chunk(isa='synonym', word='number', synonym='digit'),
    Chunk(isa='synonym', word='digit', synonym='number'),
]


class UndifferentiatedAgent(Agent):

    def __init__(self, env, output=True):
        super().__init__(output=output)

        self.memory = Memory(self, Memory.OPTIMIZED_DECAY)
        self.memory.decay_rate = .5
        self.memory.activation_noise = .5
        self.memory.retrieval_threshold = -1.8
        self.memory.latency_factor = .450
        for chunk in KNOWLEDGE_BASE:
            self.memory.store(chunk, boost=100)

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

        if words[0] == 'read':
            sem = Item(isa='action', type='read', object=words[1])
            pointer = self.vision.find(isa='pointer')
            if pointer is not None:
                self.vision.encode(pointer)
                sem.set('x', pointer.x).set('y', pointer.y)
            return sem

        elif words[0] == 'if':
            return Item(isa='if', condition=words[1],
                        action=self.interpreter(words[2:]))

        elif words[0] == 'done':
            return Item(isa='done')

        elif len(words) >= 2:
            sem = Item(isa='action', type=words[0], object=words[1])
            if len(words) == 4 and words[2] == 'for':
                sem.set('for', words[3])
            return sem

        else:
            return Item(isa='action', type=words[0])

    def executor(self, action, context):

        def set_context(slot, value):
            self.log('updating context {}={}'.format(slot, value))
            context.set(slot, value)

        def deep_get(chunk, slot):
            value = chunk.get(slot)
            if not value:
                syn = self.memory.recall(isa='synonym', word=slot)
                if syn:
                    self.log('trying synonym {}'.format(syn.synonym))
                    value = chunk.get(syn.synonym)
            return value

        def get_context(slot):
            return deep_get(context, slot)

        if action.isa == 'action':

            if action.type == 'wait_for':
                visual = self.vision.wait_for()
                set_context(action.object, self.vision.encode(visual))

            elif action.type == 'recall':
                for_slot = action.get('for')
                query = Query().eq(for_slot, get_context(for_slot))
                recalled = self.memory.recall(query)
                set_context(action.object,
                            deep_get(recalled, action.object) if recalled else None)

            elif action.type == 'read':
                query = Query(x=action.x, y=action.y)
                set_context(action.object, self.vision.find_and_encode(query))

            elif action.type == 'type' or action.type == 'press':
                text = (action.object[1:-1]
                        if action.object.startswith('"')
                        else get_context(action.object))
                self.motor.type(text)

            elif action.type == 'remember' and action.object == 'state':
                self.log('remembering state')
                self.memory.store(context)

            elif action.type == 'repeat':
                if (not self.time_limit) or self.time() < self.time_limit:
                    self.instruction.execute(self.goal)

        elif action.isa == 'if':
            cond = get_context(action.condition)
            if cond:
                self.log('condition passed')
                self.executor(action.action, context)
            else:
                self.log('condition failed')

    def run(self, time):
        self.goal = self.instruction.listen_and_learn()
        self.time_limit = self.time() + time
        while self.time() < self.time_limit:
            self.instruction.execute(self.goal)


# class InstructionChunk:

#     def __init__(self, query, fn):
#         self.query = query
#         self.fn = fn

#     def execute(self):
#         pass


# class DRSUndifferentiatedAgent(Agent):

#     def __init__(self):
#         """Initializes the agent"""
#         super().__init__(output=True)
#         self.memory = Memory(self)
#         self.vision = Vision(self)
#         self.audition = Audition(self)
#         self.hands = Hands(self)
#         self.mouse = Mouse(self.hands, self.vision)
#         self.typing = Typing(self.hands)

#         self.language = Language(self)
#         self.language.add_interpreter(self.interpret)

#         # self.instruction = Instruction(
#         #     self, self.memory, self.audition, self.language)
#         # self.instruction.add_executor(self.execute)

#     def _interpret_predicate(self, text, isa='fact', last=None):
#         chunk = None
#         (pred, args) = text.replace(')', '').split('(')
#         args = args.split(',')
#         if len(args) == 1:
#             chunk = Chunk(isa=isa, predicate='isa',
#                           subject=args[0], object=pred)
#         elif len(args) == 2:
#             chunk = Chunk(isa=isa, predicate=pred,
#                           subject=args[0], object=args[1])
#         if chunk:
#             if last:
#                 chunk.set('last', last.id)
#             self.memory.store(chunk)
#         return chunk

#     def _interpret_rule(self, text):
#         lhs, rhs = text.split('=>')
#         pred_pat = re.compile(r'[A-Za-z_-]+\([A-Za-z_,-]*\)')

#         rule = Chunk(isa='rule')
#         self.memory.store(rule)

#         last = rule
#         for t in pred_pat.findall(lhs):
#             chunk = self._interpret_predicate(t, isa='condition', last=last)
#             last = chunk

#         last = rule
#         for t in pred_pat.findall(rhs):
#             chunk = self._interpret_predicate(t, isa='action', last=last)
#             last = chunk

#         return rule

#     def _interpret_drs(self, text):
#         text = text.replace(' ', '')
#         if text.find('=>') >= 0:
#             return self._interpret_rule(text)
#         else:
#             return self._interpret_predicate(text)

#     def interpret(self, words):
#         return self._interpret_drs(''.join(words))

#     def _deep_find(self, isa):
#         visual = self.vision.find(isa=isa, seen=False)
#         if visual:
#             return visual
#         else:
#             part_of = self.memory.recall(predicate='isPartOf', object=isa)
#             if part_of:
#                 return self._deep_find(part_of.subject)
#             else:
#                 return None

#     def _execute_condition(self, cond, context):
#         if cond.predicate == 'appearsIn':
#             visual = self._deep_find(cond.subject)
#             if visual:
#                 context.set('visual', visual)
#                 visobj = self.vision.encode(visual)
#                 context.set(cond.subject, visobj)
#                 return True
#         return False

#     def _execute_action(self, action, context):
#         if action.subject == 'Subject':
#             print('**************  ' + action.predicate)

#             if action.predicate == 'click':
#                 visual = context.get('visual')
#                 self.mouse.point_and_click(visual)

#             elif action.predicate == 'remember':
#                 pass

#     def execute(self, chunk, context):
#         if chunk.isa == 'rule':

#             cond = self.memory.recall(isa='condition', last=chunk.id)
#             while cond:
#                 if not self._execute_condition(cond, context):
#                     return False
#                 cond = self.memory.recall(isa='condition', last=cond.id)

#             act = self.memory.recall(isa='action', last=chunk.id)
#             while act:
#                 self._execute_action(act, context)
#                 act = self.memory.recall(isa='action', last=act.id)

#             return True

#     def run(self, time=300):
#         context = Item()

#         chunk = None
#         done = Query(predicate='isa', object='done')
#         while not (chunk and done.matches(chunk)):
#             text = self.audition.listen_for_and_encode()
#             chunk = self.language.interpret(text)

#         while self.time() < time:
#             chunk = self.memory.recall(isa='rule')
#             self.execute(chunk, context)
