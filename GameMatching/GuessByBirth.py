import KyanToolKit_Py
ktk = KyanToolKit_Py.KyanToolKit_Py()
ktk.update()

while True:
    ktk.clearScreen();
    print( ktk.banner("Enter Birthday: (ex.19890101)") )
    player1 = ktk.getInput("Player 1:")
    player2 = ktk.getInput("Player 2:")
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
        words = "Result is : " + result + "% ! " + "Congratulations! Go and get her/him!"
        print( ktk.banner(words) )
    else:
        words = "Result is : " + result + "% ! " + "Anyhow, Still have a chance! You can make it!"
        print( ktk.banner(words) )
    print( ktk.banner("This is just a game!") )
    ktk.pressToContinue()

