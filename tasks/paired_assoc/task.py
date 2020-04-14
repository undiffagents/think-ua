import random

from think import Data, Environment, Task, World

from ..instructions import InstructionTaskFactory


class PairedAssociatesTask(Task):
    N_BLOCKS = 8
    PAIRS = [('bank', 0), ('card', 1), ('dart', 2), ('face', 3), ('game', 4),
             ('hand', 5), ('jack', 6), ('king', 7), ('lamb', 8), ('mask', 9),
             ('neck', 0), ('pipe', 1), ('quip', 2), ('rope', 3), ('sock', 4),
             ('tent', 5), ('vent', 6), ('wall', 7), ('xray', 8), ('zinc', 9)]

    def __init__(self, env, corrects=None, rts=None):
        super().__init__()
        self.display = env.display
        self.keyboard = env.keyboard
        self.corrects = corrects or Data(self.N_BLOCKS)
        self.rts = rts or Data(self.N_BLOCKS)
        self.responded = False
        self.done = False

    def run(self, time):

        def handle_key(key):
            if str(key) == str(self.trial_number):
                self.log('correct response')
                self.corrects.add(self.block, 1)
                self.rts.add(self.block, self.time() - self.trial_start)
                self.responded = True

        self.keyboard.add_type_fn(handle_key)

        for block in range(self.N_BLOCKS):
            self.block = block
            pairs = self.PAIRS.copy()
            random.shuffle(pairs)
            for word, number in pairs:
                self.trial_start = self.time()
                self.trial_number = number
                self.responded = False
                self.display.clear()
                self.display.add_text(50, 50, word, isa='word')
                self.wait(5.0)
                if not self.responded:
                    self.log('incorrect response')
                    self.corrects.add(self.block, 0)
                self.display.add_text(50, 50, number, isa='number')
                self.wait(5.0)


PAIRED_ASSOCIATE_INSTRUCTIONS = [
    'to perform the task',
    'wait for the word',
    'recall the digit for the word',
    'if digit type the digit',
    'wait for the digit',
    'remember the word and digit',
    'repeat'
]

PAIRED_ASSOCIATE_INSTRUCTIONS_SYNONYM_1 = [
    'to perform the task',
    'wait for the word',
    'recall the digit for the word',
    'if digit type the digit',
    'wait for the number',
    'remember the word and digit',
    'repeat'
]

PAIRED_ASSOCIATE_INSTRUCTIONS_SYNONYM_2 = [
    'to perform the task',
    'wait for the word',
    'recall the number for the word',
    'if digit type the digit',
    'wait for the digit',
    'remember the word and digit',
    'repeat'
]

PAIRED_ASSOCIATE_INSTRUCTIONS_SYNONYM_3 = [
    'to perform the task',
    'wait for the word',
    'recall the digit for the word',
    'if digit type the number',
    'wait for the digit',
    'remember the word and digit',
    'repeat'
]

PAIRED_ASSOCIATE_INSTRUCTIONS_NO_REPEAT = [
    'to perform the task',
    'wait for the word',
    'recall the digit for the word',
    'if digit type the digit',
    'wait for the digit',
    'remember the word and digit'
]


PairedAssociatesInstructionTask = InstructionTaskFactory(
    PairedAssociatesTask,
    # PAIRED_ASSOCIATE_INSTRUCTIONS
    # PAIRED_ASSOCIATE_INSTRUCTIONS_SYNONYM_1
    # PAIRED_ASSOCIATE_INSTRUCTIONS_SYNONYM_2
    # PAIRED_ASSOCIATE_INSTRUCTIONS_SYNONYM_3
    PAIRED_ASSOCIATE_INSTRUCTIONS_NO_REPEAT
)
