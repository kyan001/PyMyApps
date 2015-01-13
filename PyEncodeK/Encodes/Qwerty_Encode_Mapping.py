alphabets = [
	'a','b','c','d','e','f','g',
	'h','i','j','k','l','m','n',
	'o','p','q','r','s','t',
	'u','v','w','x','y','z',
	]
special_chars = [
	'q','w','e','r','t','y','u',	# abcdefg
	'i','o','p','a','s','d','f',	# hijklmn
	'g','h','j','k','l','z',		# opq rst
	'x','c','v','b','n','m',		# uvw xyz
	]
escaper = '№'
alpha_to_spchar = dict(zip(alphabets,special_chars))
spchar_to_alpha = dict(zip(special_chars,alphabets))
