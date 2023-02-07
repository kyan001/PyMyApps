import time
import csv

from classes import RoboYard


def csvGenerate():
    csv_form = [("time", "Power", "Alive Robo", "Total Robo")]
    file_name = "Robo_Yard_" + str(round(time.time())) + ".csv"
    csv_file = open(file_name, 'w', newline="")
    writer = csv.writer(csv_file)
    writer.writerows(csv_form)
    csv_file.close()


def main():
    yards = []
    yard = RoboYard.RoboYard(robo_init=8, power_max=72, idel_max=0.50, name="test")
    yards.append(yard)


if __name__ == '__main__':
    main()
