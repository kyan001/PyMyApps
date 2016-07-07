#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import tkinter
# Parameters Definition
threshold = 0.5
seperater = "---------"


# functions:
def GetRange(a):
    if 1 <= a <= 12:
        return '-[01-12]-'
    elif 12 < a <= 24:
        return '-[12-24]-'
    elif 24 < a <= 48:
        return '-[24-48]-'
    elif 48 < a:
        return '--[48+]--'
    else:
        exit('[ERR] GetRange input error')


def GetInput():
    str_input = input("[input % / q = quit]: ")
    if str_input == 'q':
        exit()
    ClearScreen()
    int_input = int(str_input)
    if int_input > 50:
        int_input = 100 - int_input
    return int_input


def GetRatio(percent_in):
    if percent_in != 0:
        ratio_out = (100 - percent_in) / percent_in
        print('[INFO] Ratio=', ratio_out)
    else:
        print('Are you kidding me?')
        return None
    return ratio_out


def GetResult(ratio_in, thres, lowerBound=-1):
    print("\n\n")
    prefix = ''
    suffix = ''
    for x in range(1, 50):
        y_calc = ratio_in * x
        y = int(y_calc)
        if lowerBound < (y_calc - y) <= thres:
            believeRatio = 100 - int(100 * (y_calc - y) / threshold)
            if (prefix != GetRange(x)) and (suffix != GetRange(y)):
                prefix = GetRange(x)
                suffix = GetRange(y)
                print(DrawLine([prefix, seperater, seperater, suffix, None], "-", "-"))
            else:
                if prefix != GetRange(x):
                    prefix = GetRange(x)
                    print(DrawLine([prefix, seperater, None, None, None], "-", "|", "<"))
                if suffix != GetRange(y):
                    suffix = GetRange(y)
                    print(DrawLine([None, None, seperater, suffix, None], "|", "-", ">"))
            print(DrawLine([None, str(x), str(y), None, '\t' + str(believeRatio) + '%']))
    print("         +" + seperater + "=" + seperater + "+")


def printGui(gui_root, input_):
    tkinter.Label(gui_root, text=input_, font="Terminal").pack(anchor='w')


def GetResultGui(gui_root, ratio_in, thres, lowerBound=-1):
    print("\n\n")
    prefix = ''
    suffix = ''
    for x in range(1, 50):
        y_calc = ratio_in * x
        y = int(y_calc)
        if lowerBound < (y_calc - y) <= thres:
            believeRatio = 100 - int(100 * (y_calc - y) / threshold)
            if (prefix != GetRange(x)) and (suffix != GetRange(y)):
                prefix = GetRange(x)
                suffix = GetRange(y)
                printGui(gui_root, DrawLine([prefix, seperater, seperater, suffix, None], "-", "-"))
            else:
                if prefix != GetRange(x):
                    prefix = GetRange(x)
                    printGui(gui_root, DrawLine([prefix, seperater, None, None, None], "-", "|", "<"))
                if suffix != GetRange(y):
                    suffix = GetRange(y)
                    printGui(gui_root, DrawLine([None, None, seperater, suffix, None], "|", "-", ">"))
            printGui(gui_root, DrawLine([None, str(x), str(y), None, '\t' + str(believeRatio) + '%']))
    print("[-----GUI Load Finish-----]")


def ClearScreen():
    os.system('cls')


def DrawLine(strList, char1='|', char3='|', char2='|'):
    for i in range(0, len(strList)):
        if strList[i] is None:
            strList[i] = '         '
    finalStr = ''
    finalStr += GenStrInMiddle(strList[0], 9)
    finalStr += char1
    finalStr += GenStrInMiddle(strList[1], 9)
    finalStr += char2
    finalStr += GenStrInMiddle(strList[2], 9)
    finalStr += char3
    finalStr += GenStrInMiddle(strList[3], 9)
    finalStr += '\t'
    finalStr += strList[4]
    return finalStr


def GenStrInMiddle(str_in, len_in):
    str_out = ''
    spaceNum = int(len_in - len(str_in))
    if spaceNum % 2 == 1:
        str_out += ' '
        spaceNum -= 1
    midStr = str_in
    if spaceNum != 0:
        for i in range(1, int(spaceNum / 2) + 1):
            midStr = ' ' + midStr + ' '
    str_out += midStr
    return str_out


def main():
    while True:
        percent = GetInput()
        ratio = GetRatio(percent)
        if ratio:
            root = tkinter.Tk()
            GetResult(ratio, 0)
            GetResult(ratio, threshold, 0)
            GetResultGui(root, ratio, 0)
            GetResultGui(root, ratio, threshold, 0)
# Main:
main()
