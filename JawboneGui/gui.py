import tkinter
import csv

# GUI Panels init:
panel1 = tkinter.Tk()
tkinter.Label(panel1, text="===== Information =====").pack()
panel2 = tkinter.Tk()
tkinter.Label(panel2, text="===== No-valued Cols =====").pack()

# Read csv file
csvfile = open('2013.csv', 'r')
reader = csv.reader(csvfile)
List = list()
UnvaluedList = list()
for line in reader:
    List.append(line)

# 1st Panel
for i in range(0, len(List[0])):
    if List[1][i] != "":
        guilabel = tkinter.Label(panel1, text=List[0][i] + " = " + List[1][i])
        guilabel.pack()
    else:
        UnvaluedList.append(List[0][i])

# 2nd Panel:
for unvalname in UnvaluedList:
    tkinter.Label(panel2, text=unvalname).pack()

# Show GUI
panel1.mainloop()
panel2.mainloop()
