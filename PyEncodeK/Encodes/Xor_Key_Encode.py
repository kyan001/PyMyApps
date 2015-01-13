class Xor_Key_Encode(object):
	def __init__(self):
		self.SEPARATOR = "-"
		self.ESCAPOR = "~"
		pass
	def encode(self,input_):
		result = ''
		key = input_.strip(' ').split(':')[0]
		original = ''.join(input_.strip(' ').split(':')[1:])
		if "" == original:
			return "[Format:] CipherKey:Your words"
		for i in range(len(original)):
			if self.SEPARATOR == original[i]:
				result += self.ESCAPOR + self.SEPARATOR
			else:
				result += str((ord(original[i]) ^ ord(key[i%len(key)]))) + self.SEPARATOR
		return result

	def decode(self,input_):
		result = ''
		key = input_.strip(' ').split(':')[0]
		ciphered = ''.join(input_.strip(' ').split(':')[1:]).split(self.SEPARATOR)[:-1]
		if "" == ciphered:
			return "[Format:] CipherKey:Your words"
		for i in range(len(ciphered)):
			result += chr(int(ciphered[i]) ^ ord(key[i%len(key)]))
		return result
