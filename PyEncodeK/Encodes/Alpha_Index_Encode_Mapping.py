alphabets = [
	'a','b','c','d','e','f','g',
	'h','i','j','k','l','m','n',
	'o','p','q','r','s','t',
	'u','v','w','x','y','z',
	]
special_chars = [
	'01','02','03','04','05','06','07',	# abcdefg
	'08','09','10','11','12','13','14',	# hijklmn
	'15','16','17','18','19','20',		# opq rst
	'21','22','23','24','25','26',		# uvw xyz
	]
escaper = 'x'
alpha_to_spchar = dict(zip(alphabets,special_chars))
spchar_to_alpha = dict(zip(special_chars,alphabets))
