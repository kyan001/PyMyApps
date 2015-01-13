alphabets = [
	'a','b','c','d','e','f','g',
	'h','i','j','k','l','m','n',
	'o','p','q','r','s','t',
	'u','v','w','x','y','z',
	'A','B','C','D','E','F','G',
	'H','I','J','K','L','M','N',
	'O','P','Q','R','S','T',
	'U','V','W','X','Y','Z',
	'0','1','2','3','4',
	'5','6','7','8','9',
	]
emojis = [
	'0TZ','OT2','0T2','OTZ','S20','SZ0','szo',	# abcdefg
	'SZO','S2O','@-@','@_@','@o@','>_<','>o<',	# hijklmn
	'>3<','O_O','O3O','OoO','o_o','0_0',		# opq rst
	'-_-','-o-','-3-','^-^','^_^','^o^',		# uvw xyz
	'^3^','=_=','=o=','=~=','<_<','>_>','*_*',	# ABCDEFG
	'*o*','*3*','U_U','U3U','u_u','ToT','T-T',	# HIJKLMN
	'T_T','T3T','#_#','&_&','Q_Q','QoQ',		# OPQ RST
	'Q3Q','a_a','e_e','X_X','$_$','$o$',		# UVW XYZ
	'$-$','n_n','~_~',':-D',':-(',				# 0-4
	':-P',':-*',';-)',':-x',':-O',				# 5-9
	]
decorates = [
	'_','!','|',')','(',
]
escaper = 'orz'
alpha_to_emoji = dict(zip(alphabets,emojis))
emoji_to_alpha = dict(zip(emojis,alphabets))