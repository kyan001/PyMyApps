import KyanToolKit3

while True:
	KyanToolKit3.clearScreen();
	KyanToolKit3.banner("Enter Birthday: (ex.19890101)")
	player1 = KyanToolKit3.getInput("Player 1:")
	player2 = KyanToolKit3.getInput("Player 2:")
	result = player1 + player2
	while int(result) > 99 or len(result) >= 3:
		calc_store = ""
		for i in range(0,len(result)-1):
			num_this = int(result[i])
			num_next = int(result[i+1])
			calc_result = num_this + num_next
			calc_store += str(calc_result % 10)
		result = calc_store
		print("-->" + result)
	if int(result) > 50:
		KyanToolKit3.banner("Result is : " + result + "% ! " + "Congratulations! Go and get her/him!")
	else:
		KyanToolKit3.banner("Result is : " + result + "% ! " + "Anyhow, Still have a chance! You can make it!")
	KyanToolKit3.banner("This is just a game!")
	KyanToolKit3.pressToContinue()

