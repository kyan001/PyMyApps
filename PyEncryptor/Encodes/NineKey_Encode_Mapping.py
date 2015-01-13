alphabets = [
	'a','b','c','d','e','f','g',
	'h','i','j','k','l','m','n',
	'o','p','q','r','s','t',
	'u','v','w','x','y','z',
	]
special_chars = [
	'21','22','23','31','32','33','41',	# abcdefg
	'42','43','51','52','53','61','62',	# hijklmn
	'63','71','72','73','74','81',		# opq rst
	'82','83','91','92','93','94',		# uvw xyz
	]
escaper = '0'
alpha_to_spchar = dict(zip(alphabets,special_chars))
spchar_to_alpha = dict(zip(special_chars,alphabets))
