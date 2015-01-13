import Emoji_CodeMapping
import random

class Emoji_Encode_Pure(object):
	def __init__(self):
		self.CHAR_NUMBER = 5
		pass
	def __del__(self):
		pass
	def encode(self,input_):
		result = ''
		for i in input_:
			if (i in Emoji_CodeMapping.alphabets):
				result += (Emoji_CodeMapping.alpha_to_emoji[i] + " ");
			elif " " == i:
				result += (Emoji_CodeMapping.escaper + " ");
			else:
				result += (i + " ");
		return result

	def decode(self,input_):
		result = ''
		for s in input_.split():
			if (s in Emoji_CodeMapping.escaper):
				result += " "
			elif (s in Emoji_CodeMapping.emojis):
				result += Emoji_CodeMapping.emoji_to_alpha[s]
			else:
				result += s
		return result