import consoleiotools as cit

while True:
    # init
    cit.echo("Enter Your Birthday: (ex.19890101)")
    player1 = cit.get_input("Yours:")
    cit.echo("Yours Mr/Ms.Right was born in which year? (ex.1987)")
    player2_year = cit.get_input("He/She was born in ...:")
    result = player1 + player2_year
    # start calc
    possible_list = []
    final_list = []
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
            # start 2nd round check
            if 70 <= int(result_tmp) <= 80:
                result_tmp2 = player2_year + month_add + day_add + player1
                while int(result_tmp2) > 99 or len(result_tmp2) >= 3:
                    calc_store = ""
                    for i in range(0, len(result_tmp2) - 1):
                        num_this = int(result_tmp2[i])
                        num_next = int(result_tmp2[i + 1])
                        calc_result = num_this + num_next
                        calc_store += str(calc_result % 10)
                    result_tmp2 = calc_store
                if 60 <= int(result_tmp2) <= 70:
                    final_list.append(player2_year + "." + month_add + "." + day_add + " --> " + result_tmp2 + "%")
            if 60 <= int(result_tmp) <= 70:
                result_tmp3 = player2_year + month_add + day_add + player1
                while int(result_tmp3) > 99 or len(result_tmp3) >= 3:
                    calc_store = ""
                    for i in range(0, len(result_tmp3) - 1):
                        num_this = int(result_tmp3[i])
                        num_next = int(result_tmp3[i + 1])
                        calc_result = num_this + num_next
                        calc_store += str(calc_result % 10)
                    result_tmp3 = calc_store
                if 70 <= int(result_tmp3) <= 80:
                    final_list.append(player2_year + "." + month_add + "." + day_add + " --> " + result_tmp3 + "%")
    cit.echo("Possible Results:")
    for y in final_list:
        print(y)
    cit.echo("This is just a game!")
    cit.pause()
