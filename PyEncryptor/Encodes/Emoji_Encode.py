import Emoji_CodeMapping
import random

class Emoji_Encode(object):
	def __init__(self):
		self.CHAR_NUMBER = 5
		pass
	def __del__(self):
		pass
	def encode(self,input_):
		result = ''
		for i in input_:
			_decorate_left = random.choice(Emoji_CodeMapping.decorates)
			_decorate_right = random.choice(Emoji_CodeMapping.decorates)
			if (i in Emoji_CodeMapping.alphabets):
				_mapping = Emoji_CodeMapping.alpha_to_emoji[i];
				result+= (_decorate_left + _mapping + _decorate_right)
			else:
				result+=(i+Emoji_CodeMapping.escaper+i)
		return result

	def decode(self,input_):
		result = ''
		_rest = input_;
		while _rest != '':
			_slot = _rest[0:self.CHAR_NUMBER]
			_rest = _rest[self.CHAR_NUMBER:]
			# get orz off
			if _slot.count(Emoji_CodeMapping.escaper) == 1:
				result += (_slot.replace(Emoji_CodeMapping.escaper,''))[0]
			else:
				# get decorates off
				for _decorate in Emoji_CodeMapping.decorates:
					_slot = _slot.strip(_decorate);
				result += Emoji_CodeMapping.emoji_to_alpha[_slot]
		return result