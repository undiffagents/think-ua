from think import (Agent, Audition, Aural, Chunk, Environment, Instruction,
                   Item, Language, Memory, Motor, Query, Vision, Visual)

KNOWLEDGE_BASE = [
    Chunk(isa='synonym', word='number', synonym='digit'),
    Chunk(isa='synonym', word='digit', synonym='number'),
]


class UndifferentiatedAgent(Agent):

    def __init__(self, env, output=True, knowledge_base=KNOWLEDGE_BASE):
        super().__init__(output=output)

        self.memory = Memory(self, Memory.OPTIMIZED_DECAY)
        self.memory.decay_rate = .5
        self.memory.activation_noise = .5
        self.memory.retrieval_threshold = -1.8
        self.memory.latency_factor = .450
        for chunk in knowledge_base:
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
        self.last_obj = None

    def interpreter(self, words):
        words[0] = words[0].lower()
        words = [w for w in words if w not in ['a', 'the', 'you', 'can']]

        if words[0] == 'if':
            lhs, rhs = ' '.join(words[1:]).split(', ')
            cond = self.interpreter(lhs.split(' '))
            act = self.interpreter(rhs.split(' '))
            return Item(isa='if', condition=cond, action=act)

        if self.last_obj:
            words = [self.last_obj if w == 'it' else w for w in words]

        def create_action(type_, obj):
            self.last_obj = obj
            return Item(isa='action', type=type_, object=obj)

        if words[0] == 'to':
            return Item(isa='goal', name='_'.join(words[1:]))

        elif words[0] == 'read':
            sem = create_action('read', words[1])
            pointer = self.vision.find(isa='pointer')
            if pointer is not None:
                self.vision.encode(pointer)
                sem.set('x', pointer.x).set('y', pointer.y)
            return sem

        elif words[0] == 'remember':
            objs = [w for w in words[1:] if w != 'and']
            return create_action(words[0], objs)

        elif words[0] == 'done':
            return Item(isa='done')

        elif len(words) >= 2:
            if len(words) == 4 and words[2] == 'for':
                return create_action(words[0], words[1]).set('for', words[3])
            else:
                return create_action('_'.join(words[:-1]), words[-1])
            return sem

        else:
            return Item(isa='action', type=words[0])

    def executor(self, action, context):

        def set_context(slot, value):
            self.log('updating context {}={}'.format(slot, value))
            context.set(slot, value)

        def deep_get(chunk, slot):
            if slot.startswith('"'):
                return slot[1:-1]
            else:
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

            elif action.type == 'find':
                target = get_context(action.object)
                visual = self.vision.wait_for(seen=False)
                obj = self.vision.encode(visual) if visual else None
                while visual and obj != target:
                    visual = self.vision.find(seen=False)
                    obj = self.vision.encode(visual) if visual else None
                set_context('found', action.object)
                set_context('found_visual', visual)

            elif action.type == 'move_mouse_to':
                if context.get('found') != action.object:
                    self.executor(Item(isa='action', type='find',
                                       object=action.object),
                                  context)
                visual = get_context('found_visual')
                self.motor.move_to(visual)
                set_context('moved_to', action.object)

            elif action.type == 'click_on':
                if context.get('moved_to') != action.object:
                    self.executor(Item(isa='action', type='move_mouse_to',
                                       object=action.object),
                                  context)
                self.motor.click()

            elif action.type == 'recall':
                for_slot = action.get('for')
                query = Query().eq(for_slot, get_context(for_slot))
                recalled = self.memory.recall(query)
                value = deep_get(recalled, action.object) if recalled else None
                set_context(action.object, value)
                if not value:
                    return False

            elif action.type == 'read':
                query = Query(x=action.x, y=action.y)
                set_context(action.object, self.vision.find_and_encode(query))

            elif action.type == 'type' or action.type == 'press':
                text = (action.object[1:-1]
                        if action.object.startswith('"')
                        else get_context(action.object))
                self.motor.type(text)

            elif action.type == 'remember':
                chunk = Chunk()
                for slot in action.object:
                    chunk.set(slot, get_context(slot))
                self.log('remembering {}'.format(chunk))
                self.memory.store(chunk)

            elif action.type == 'repeat':
                if (not self.time_limit) or self.time() < self.time_limit:
                    self.instruction.execute(self.goal)

        elif action.isa == 'if':
            if self.executor(action.condition, context):
                self.log('condition passed')
                self.executor(action.action, context)
            else:
                self.log('condition failed')

        return True

    def run(self, time):
        self.goal = self.instruction.listen_and_learn()
        self.time_limit = self.time() + time
        while self.time() < self.time_limit:
            self.instruction.execute(self.goal)
