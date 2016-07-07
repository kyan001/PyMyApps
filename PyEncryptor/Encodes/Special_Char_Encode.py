from Encodes import Special_Char_Mapping


class Special_Char_Encode(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def encode(self, input_):
        result = ''
        for i in input_:
            if (i in Special_Char_Mapping.alphabets):
                result += (Special_Char_Mapping.alpha_to_spchar[i])
            elif " " == i:
                result += (Special_Char_Mapping.escaper)
            else:
                result += (i)
        return result

    def decode(self, input_):
        result = ''
        for s in input_:
            if (s in Special_Char_Mapping.escaper):
                result += " "
            elif (s in Special_Char_Mapping.special_chars):
                result += Special_Char_Mapping.spchar_to_alpha[s]
            else:
                result += s
        return result
