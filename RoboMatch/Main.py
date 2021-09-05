import time
import csv

import KyanToolKit

import RoboYard

# -Main----------------------------------------------------------
start_time = time.time()
CSV_FORM = [("time", "Power", "Alive Robo", "Total Robo")]


def csvGenerate(enable):
    if CSV_FORM and enable:
        file_name = "Robo_Yard_" + str(round(time.time())) + ".csv"
        csv_file = open(file_name, 'w', newline="")
        writer = csv.writer(csv_file)
        writer.writerows(CSV_FORM)
        csv_file.close()


def byeBye():
    csvGenerate(True)
    KyanToolKit.KyanToolKit.byeBye()

yards = []
yard = RoboYard.RoboYard(robo_init=8, power_max=72, idel_max=0.50, name="test")
yards.append(yard)
while True:
    time.sleep(30)
