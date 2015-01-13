import Qwerty_Encode_Mapping

class Qwerty_Encode(object):
	def __init__(self):
		pass
	def __del__(self):
		pass
	def encode(self,input_):
		result = ''
		for i in input_.strip():
			if (i.lower() in Qwerty_Encode_Mapping.alphabets):
				if i.islower():
					result += Qwerty_Encode_Mapping.alpha_to_spchar[i.lower()]
				else:
					result += Qwerty_Encode_Mapping.alpha_to_spchar[i.lower()].upper()
			else:
				result += i
		return result

	def decode(self,input_):
		result = ''
		for s in input_.strip():
			if (s.lower() in Qwerty_Encode_Mapping.special_chars):
				if s.islower():
					result += Qwerty_Encode_Mapping.spchar_to_alpha[s.lower()]
				else:
					result += Qwerty_Encode_Mapping.spchar_to_alpha[s.lower()].upper()
			else:
				result += s
		return result
