from Encodes import Alpha_Index_Encode_Mapping


class Alpha_Index_Encode(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def encode(self, input_):
        result = ''
        for i in input_.strip():
            if (i.lower() in Alpha_Index_Encode_Mapping.alphabets):
                result += Alpha_Index_Encode_Mapping.alpha_to_spchar[i.lower()]
            else:
                result += (Alpha_Index_Encode_Mapping.escaper + i)
        return result

    def decode(self, input_):
        result = ''
        s = input_.strip()
        for i in range(int(len(s) / 2)):
            s1 = s[i * 2]
            s2 = s[i * 2 + 1]
            if (s1 + s2 in Alpha_Index_Encode_Mapping.special_chars):
                result += Alpha_Index_Encode_Mapping.spchar_to_alpha[s1 + s2]
            elif Alpha_Index_Encode_Mapping.escaper == s1:
                result += s2
            else:
                result += "[Undefine]"
        return result
