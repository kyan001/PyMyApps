import string
import consoleiotools as cit
import KyanToolKit
ktk = KyanToolKit.KyanToolKit()


def Encode(in_, shift):
    result = ""
    for c in in_.strip(' '):
        if c.lower() in string.ascii_letters:
            result += chr((ord(c.lower()) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += c
    return result


def Decode(in_):
    result = ""
    result += "====== Possible Results ======\n"
    for i in range(26):
        result += "Shift=" + str(i) + " : "
        for c in in_.strip(' '):
            if c.lower() in string.ascii_letters:
                result += chr((ord(c.lower()) - ord('a') - i) % 26 + ord('a'))
            else:
                result += c
        result += "\n"
    return result


def main():
    ktk.clearScreen()

    cit.ask("Encode or Decode? That's a question")
    usr_choice = cit.get_choice(["Encode", "Decode"])

    cit.ask("What do you wanna " + usr_choice.upper() + "?")
    user_input = cit.get_input("Please Enter your words:").replace("\n", "")

    cit.info(usr_choice + " Result")
    if "Encode" == usr_choice:
        cit.ask("Shift is ... ?")
        user_shift = cit.get_input("Please Enter a number between 0-26 :").replace("\n", "")
        print("\n--Raw Input--")
        print(user_input + " @ " + user_shift)
        print("\n--Encoded Output--")
        print(Encode(user_input, int(user_shift)))
    elif "Decode" == usr_choice:
        print("\n--Encoded Input--")
        print(user_input)
        print("\n--Decoded Raw Output--")
        print(Decode(user_input))
    else:
        cit.bye()
    cit.pause()

while(True):
    main()
