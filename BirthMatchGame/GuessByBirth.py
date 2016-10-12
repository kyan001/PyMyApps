import consoleiotools as cit

while True:
    cit.start()
    cit.title('Game Start')
    cit.ask("Enter Birthday: (ex.19890101):")
    player1 = cit.get_input("Player 1:")
    player2 = cit.get_input("Player 2:")
    result = player1 + player2
    while int(result) > 99 or len(result) >= 3:
        calc_store = ""
        for i in range(0, len(result) - 1):
            num_this = int(result[i])
            num_next = int(result[i + 1])
            calc_result = num_this + num_next
            calc_store += str(calc_result % 10)
        result = calc_store
        print("-->" + result)
    if int(result) > 50:
        words = "Result is : " + result + "% ! " + "Congratulations! Go and get her/him!"
        cit.info(words)
    else:
        words = "Result is : " + result + "% ! " + "Anyhow, Still have a chance! You can make it!"
        cit.info(words)
    cit.warn("This is just a game!")
    cit.pause()
