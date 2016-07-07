import sys
import tkinter

import KyanToolKit

from Encodes import Emoji_Encode
from Encodes import NATO_Phonetic_Encode
from Encodes import Emoji_Encode_Pure
from Encodes import Special_Char_Encode
from Encodes import Xor_Key_Encode
from Encodes import Reverse_Encode
from Encodes import Rail_Fence_Encode
from Encodes import Qwerty_Encode
from Encodes import Morse_Encode
from Encodes import NineKey_Encode
from Encodes import Alpha_Index_Encode
from Encodes import ASCII_Encode

ktk = KyanToolKit.KyanToolKit()

algo_list = [
    "Emoji_Encode",
    "Emoji_Encode_Pure",
    "NATO_Phonetic_Encode",
    "Special_Char_Encode",
    "Xor_Key_Encode",
    "Reverse_Encode",
    "Rail_Fence_Encode",
    "Qwerty_Encode",
    "Morse_Encode",
    "NineKey_Encode",
    "Alpha_Index_Encode",
    "ASCII_Encode",
]


# -Common Defs----------------------------------------------------
def getAlgo(algo_input_):
    # if "Emoji_Encode" == algo_input_:
    # encode_mode = Emoji_Encode.Emoji_Encode()
    if algo_input_ in algo_list:
        encode_mode = getattr(globals()[algo_input_], algo_input_)()
    else:
        ktk.TRACE("Wrong Algorithm: " + algo_input_, "ERR")
        ktk.Err("Wrong Algorithm: " + algo_input_)
        ktk.byeBye()
    return encode_mode


def selectAlgo():
    print(ktk.banner("Please Choose Algorithm:"))
    return ktk.getChoice(algo_list)


# -GUI init-------------------------------------------------------
def getEncodeGui():
    global ALGO
    dec_gui_input.set(getAlgo(ALGO).encode(enc_gui_input.get()))
    # dec_entry['state'] = 'readonly'


def getDecodeGui():
    global ALGO
    enc_gui_input.set(getAlgo(ALGO).decode(dec_gui_input.get()))
    # dec_entry['state'] = 'readonly'


def clearEncodeEntry():
    enc_gui_input.set("")


def clearDecodeEntry():
    dec_gui_input.set("")


def setAlgoGui():
    global algo_var
    global ALGO
    ALGO = algo_list[algo_var.get()]
    algo_indicator.set(ALGO)


def selectEncodeText():
    enc_entry.selection_range(0, len(enc_gui_input.get()))


def selectDecodeText():
    dec_entry.selection_range(0, len(dec_gui_input.get()))


# -init-----------------------------------------------------------
# get encode Algorithm
ALGO = "Xor_Key_Encode"
ktk.TRACE("Selected Algorithm: " + ALGO)
if not (("-console" in sys.argv) or ("-gui" in sys.argv)):
    print(ktk.banner("Please choose the interface"))
    sys.argv.append(ktk.getChoice(["-gui", "-console"]))

# -GUI Launch-----------------------------------------------------
if "-gui" in sys.argv:
    root = tkinter.Tk(className="加密解密Encoder By Kyan")
    # set Algo Indicator
    algo_indicator = tkinter.StringVar()
    algo_indecator_entry = tkinter.Entry(root, textvariable=algo_indicator)
    algo_indicator.set("编码解码算法将显示在这里。")
    algo_indecator_entry['state'] = 'readonly'
    algo_indecator_entry.pack(side=tkinter.TOP, fill='both')
    # set Algo Option
    algo_var = tkinter.IntVar()
    algo_var.set(0)
    for i in range(len(algo_list)):
        algo_radio = tkinter.Radiobutton(root, text=algo_list[i] + ": " + getAlgo(algo_list[i]).encode("Hello"), variable=algo_var, value=i, command=setAlgoGui).pack(side=tkinter.TOP, anchor="w")
    # set Encode Entry
    encode_label = tkinter.Label(root, text="==========================Encode编码==========================").pack(side=tkinter.TOP, fill='both')
    enc_gui_input = tkinter.StringVar()
    enc_gui_input.set("input words here (编码输入这里)")
    enc_entry = tkinter.Entry(root, textvariable=enc_gui_input)
    enc_entry.pack(side=tkinter.TOP, fill='both')
    # set Decode Entry
    encode_label = tkinter.Label(root, text="==========================Decode解码==========================").pack(side=tkinter.TOP, fill='both')
    dec_gui_input = tkinter.StringVar()
    dec_entry = tkinter.Entry(root, textvariable=dec_gui_input)
    dec_gui_input.set("input passwords here (解码输入这里)")
    dec_entry.pack(side=tkinter.TOP, fill='both')
    # set Encode Button
    enc_button = tkinter.Button(root, text="Encode!", command=getEncodeGui).pack(side=tkinter.LEFT, fill='both')
    enc_clean_button = tkinter.Button(root, text="<--Clear", command=clearEncodeEntry).pack(side=tkinter.LEFT, fill='both')
    enc_select_button = tkinter.Button(root, text="<--Select", command=selectEncodeText).pack(side=tkinter.LEFT, fill='both')
    # set Decode Button
    dec_button = tkinter.Button(root, text="Decode!", command=getDecodeGui).pack(side=tkinter.RIGHT, fill='both')
    dec_clean_button = tkinter.Button(root, text="Clear-->", command=clearDecodeEntry).pack(side=tkinter.RIGHT, fill='both')
    dec_select_button = tkinter.Button(root, text="Select-->", command=selectDecodeText).pack(side=tkinter.RIGHT, fill='both')
    root.mainloop()

# -MAIN-----------------------------------------------------------
# start looping
if "-console" in sys.argv:
    while True:
        # Encode or Decode choice
        ktk.clearScreen()
        print(ktk.banner("Encode or Decode? That's a question"))
        print(ALGO + ":")
        usr_choice = ktk.getChoice(["Encode", "Decode", "Re-select Algorithm"])
        if "Re-select Algorithm" == usr_choice:
            ktk.clearScreen()
            ALGO = selectAlgo()
        else:
            # Enter words
            print(ktk.banner("What do you wanna " + usr_choice.upper() + "?"))
            print(ALGO + ":")
            user_input = ktk.getInput("Please Enter your words:").replace("\n", "")
            # Show result
            ktk.banner(usr_choice + " Result")
            if "Encode" == usr_choice:
                print("\n--Raw Input--")
                print(user_input)
                print("\n--Encoded Output--")
                print(getAlgo(ALGO).encode(user_input))
            elif "Decode" == usr_choice:
                print("\n--Encoded Input--")
                print(user_input)
                print("\n--Decoded Raw Output--")
                print(getAlgo(ALGO).decode(user_input))
            else:
                ktk.byeBye()
            ktk.pressToContinue()
