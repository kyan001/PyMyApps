alphabets = [
	'a','b','c','d','e','f','g',
	'h','i','j','k','l','m','n',
	'o','p','q','r','s','t',
	'u','v','w','x','y','z',
	'A','B','C','D','E','F','G',
	'H','I','J','K','L','M','N',
	'O','P','Q','R','S','T',
	'U','V','W','X','Y','Z',
	]
special_chars = [
	'︻','︼','︽','︾','〒','↑','↓',	# abcdefg
	'※','⊙','℡','≡','◎','¤','★',	# hijklmn
	'☆','■','▓','◆','∑','√',		# opq rst
	'』','▲','♀','▼','♂','╬',		# uvw xyz
	'☉','●','〇','『','◇','△','▽',	# ABCDEFG
	'◣','◥','◢','◤','→','←','Ψ',	# HIJKLMN
	'↘','↙','㊣','∩','∮','∏',		# OPQ RST
	'∞','①','∴','∵','≌','℃',		# UVW XYZ
	]
escaper = '№'
alpha_to_spchar = dict(zip(alphabets,special_chars))
spchar_to_alpha = dict(zip(special_chars,alphabets))