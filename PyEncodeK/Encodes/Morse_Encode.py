import Morse_Encode_Mapping

class Morse_Encode(object):
	def __init__(self):
		pass
	def __del__(self):
		pass
	def encode(self,input_):
		result = ''
		for i in input_.strip(' '):
			if (i.lower() in Morse_Encode_Mapping.alphabets):
				result += (Morse_Encode_Mapping.alpha_to_spchar[i.lower()]);
			else:
				result += (i);
			result += "/"
		return result

	def decode(self,input_):
		result = ''
		for s in input_.strip(' ').split('/'):
			if (s in Morse_Encode_Mapping.special_chars):
				result += Morse_Encode_Mapping.spchar_to_alpha[s]
			else:
				result += s
		return result
