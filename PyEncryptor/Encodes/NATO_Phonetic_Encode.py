from Encodes import NATO_Phonetic_CodeMapping
import random


class NATO_Phonetic_Encode(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def encode(self, input_):
        result = ''
        for i in input_.strip(' '):
            if (i in NATO_Phonetic_CodeMapping.alphabet):
                _mapping = NATO_Phonetic_CodeMapping.alpha_to_np[i]
                result += (" " + _mapping)
            elif (" " == i):
                result += (" " + random.choice(NATO_Phonetic_CodeMapping.decorate))
            else:
                result += (" " + i)
        return result

    def decode(self, input_):
        result = ''
        input_words = input_.strip(' ').split(" ")
        for i in input_words:
            if (i in NATO_Phonetic_CodeMapping.NATO_phonetic):
                _mapping = NATO_Phonetic_CodeMapping.np_to_alpha[i]
                result += _mapping
            elif (i in NATO_Phonetic_CodeMapping.decorate):
                result += (" ")
            else:
                result += i
        return result
