class Rail_Fence_Encode(object):
    def __init__(self):
        pass
    def __del__(self):
        pass
    def encode(self, input_):
        result_left = ''
        result_right = ''
        for i, s in enumerate(input_.strip(' ')):
            if 0 == i % 2:
                result_left += s
            else:
                result_right += s
        return result_left + result_right

    def decode(self, input_):
        result_left=''
        result_right=''
        result=''
        half = len(input_.strip(' '))/2
        result_left = input_.strip(' ')[0:-int(half)]
        result_right = input_.strip(' ')[-int(half):]
        for i in range(len(result_right)):
            result += result_left[i]
            result += result_right[i]
        if len(result_left) > len(result_right):
            result += result_left[-1]
        return result
