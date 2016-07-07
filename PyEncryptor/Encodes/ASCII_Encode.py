class ASCII_Encode(object):
    def __init__(self):
        pass
    def __del__(self):
        pass
    def encode(self, input_):
        result = ''
        for c in input_.strip():
            result += str(hex(ord(c)))[-2:]
        return result

    def decode(self, input_):
        result = ''
        words = input_.strip()
        strategy = ""
        if set(words) <= set("01 "):
            strategy = 2
        elif set(words) <= set("0123456789 "):
            strategy = 10
        elif set(words) <= set("0123456789ABCDEFabcdef "):
            strategy = 16
        else:
            strategy = None

        if strategy != None:
            if " " in words:
                for s in words.split(" "):
                    result += chr(int(s,int(strategy)))
            else:
                for i in range(int(len(words)/2)):
                    s1 = words[i*2]
                    s2 = words[i*2+1]
                    result += chr(int(s1+s2,int(strategy)))
        result = str(strategy) + ": " + result
        return result
