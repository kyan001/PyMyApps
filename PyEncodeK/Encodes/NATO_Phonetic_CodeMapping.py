alphabet = [
	'a','b','c','d','e','f','g',
	'h','i','j','k','l','m','n',
	'o','p','q','r','s','t',
	'u','v','w','x','y','z',
	'A','B','C','D','E','F','G',
	'H','I','J','K','L','M','N',
	'O','P','Q','R','S','T',
	'U','V','W','X','Y','Z',
	'.',',','!','?','"',
	]
NATO_phonetic = [
	'alpha','bravo','charlie','delta','echo','foxtrot','golf',	# abcdefg
	'hotel','india','juliet','kilo','lima','mike','november',	# hijklmn
	'oscar','papa','quebec','romeo','sierra','tango',		# opq rst
	'uniform','victor','whiskey','x-ray','yankee','zulu',		# uvw xyz
	'Alpha','Bravo','Charlie','Delta','Echo','Foxtrot','Golf',	# ABCDEFG
	'Hotel','India','Juliet','Kilo','Lima','Mike','November',	# HIJKLMN
	'Oscar','Papa','Quebec','Romeo','Sierra','Tango',		# OPQ RST
	'Uniform','Victor','Whiskey','X-ray','Yankee','Zulu',		# UVW XYZ
	'copy.','ummm,','!!!','right?','->',
	]
decorate = [',','.','!','?','"']
alpha_to_np = dict(zip(alphabet,NATO_phonetic))
np_to_alpha = dict(zip(NATO_phonetic,alphabet))