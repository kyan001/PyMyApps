import consoleiotools as cit


while True:
    # init
    cit.ask("Enter Your Birthday: (ex.19890101)")
    player1 = cit.get_input("Yours:")
    cit.ask("Yours Mr/Ms.Right was born in which year? (ex.1987)")
    player2_year = cit.get_input("He/She was born in ...:")
    result = player1 + player2_year
    # start calc
    good_list = []
    sad_list = []
    for month_iter in range(1, 13):
        for day_iter in range(1, 32):
            if month_iter >= 10:
                month_add = str(month_iter)
            else:
                month_add = '0' + str(month_iter)
            if day_iter >= 10:
                day_add = str(day_iter)
            else:
                day_add = '0' + str(day_iter)
            result_tmp = result + month_add + day_add
            while int(result_tmp) > 99 or len(result_tmp) >= 3:
                calc_store = ""
                for i in range(0, len(result_tmp) - 1):
                    num_this = int(result_tmp[i])
                    num_next = int(result_tmp[i + 1])
                    calc_result = num_this + num_next
                    calc_store += str(calc_result % 10)
                result_tmp = calc_store
            if int(result_tmp) > 90:
                good_list.append(player2_year + "." + month_add + "." + day_add + " --> " + result_tmp + "%")
            elif int(result_tmp) < 10:
                sad_list.append(player2_year + "." + month_add + "." + day_add + " --> " + result_tmp + "%")
    cit.echo("These guys are easy to get!")
    for x in good_list:
        print(x)
    cit.echo("Please avoid these guys!")
    for y in sad_list:
        print(y)
    cit.echo("This is just a game!")
    cit.pause()
