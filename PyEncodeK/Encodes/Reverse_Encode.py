class Reverse_Encode(object):
	def __init__(self):
		pass
	def __del__(self):
		pass
	def encode(self,input_):
		result = ''
		for i in input_.strip(' '):
			result = i + result;
		return result

	def decode(self,input_):
		return self.encode(input_)
