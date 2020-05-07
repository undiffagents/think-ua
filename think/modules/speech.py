import re

from think import Module, Worker

from .utilities import count_syllables, text_to_words


class Speech(Module):

    def __init__(self, agent, microphone):
        super().__init__('speech', agent)
        self.microphone = microphone
        self.worker = Worker('speech', self)
        self.base_time = .200
        self.syllable_rate = .150

    def calculate_duration(self, word):
        return self.base_time + self.syllable_rate * count_syllables(word)

    def _say_word(self, word, s1, s2, s3):
        self.worker.acquire()
        self.think(s1 + ' "' + word + '"')
        self.log(s2 + ' "' + word + '"')
        duration = self.calculate_duration(word)

        def fn():
            self.microphone.receive(word)

        self.worker.run(duration, s3 + ' "' + word + '"', fn)

    def say(self, text):
        for word in text_to_words(text):
            self._say_word(word, 'say', 'saying', 'said')
        return self

    def subvocalize(self, text):
        for word in text_to_words(text):
            self._say_word(word, 'subvocalize',
                           'subvocalizing', 'subvocalized')
        return self
