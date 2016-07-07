import threading
import Robo
import queue
import random
import time

import KyanToolKit


class RoboYard(threading.Thread):
    'A Robo Yard can hold a group of Robos'

    def __init__(self, robo_init=10, power_max=100, idel_max=1, name="", trace_file="trace.xml"):
        threading.Thread.__init__(self)
        self.name = name
        self.robo_init = robo_init
        self.power_max = power_max
        self.idel_max = idel_max
        # unparametered variables
        self.peak_power = 0
        self.current_power = [0, 0]
        self.robo_list = []
        self.yard_queue = queue.Queue()
        self.start_time = time.time()
        self.end_time = None
        self.ktk = KyanToolKit.KyanToolKit(trace_file)
        # init Robos
        for robo_id in range(self.robo_init):
            power_init = int(random.random() * power_max)
            sex = random.choice(["♂", "♀"])
            r = Robo.Robo(robo_id, power_init, sex, self.idel_max, self)
            self.robo_list.append(r)
        self.setDaemon(True)
        self.start()

    def run(self):
        while True:
            self.ktk.clearScreen()
            self.printYard(10)
            self.childbearingPolicy(2)

            self.printStatistics()
            time.sleep(self.idel_max / 2)
            if self.yard_queue.empty():
                break
        self.byeBye()

    def childbearingPolicy(self, max_child=2):
        for r in self.robo_list:
            if "alive" == r.state:
                new_child = r.bornChild(max_child)
                if new_child:
                    self.robo_list.append(new_child)
                if r.dad:
                    if 1 == r.dad.childNum() or 1 == r.mom.childNum():
                        new_child_2 = r.bornChild(max_child)
                        if new_child_2:
                            self.robo_list.append(new_child_2)

    def printYard(self, limit="unlimited"):
        counter = 0
        for r in self.robo_list:
            if counter == limit:
                break
            if "alive" == r.state:
                counter += 1
                # power
                power_bar = ""
                for i in range(r.power):
                    power_bar = "".join((power_bar, "*"))
                conn = "".join((str(r.id), r.sex))
                if r.mate:
                    conn += "".join(("+", str(r.mate.id), r.mate.sex))
                if r.dad and r.mom:
                    conn += "".join((" by (", str(r.dad.id), "+", str(r.mom.id), ")"))
                print("".join(("== ", conn, " ", power_bar, " (", str(r.power), ")")))
                # grow & age
                grow_bar = ""
                age_bar = ""
                for i in range(r.grow):
                    grow_bar += "-"
                for i in range(r.age - r.grow):
                    age_bar += "="
                print("==+" + grow_bar + ">", end="")
                # match
                if r.mate:
                    print("Matched" + age_bar + ">", end="")
                if r.child:
                    print("Born*" + str(r.childNum()), end="")
                print("\n")

    def printStatistics(self):
        word_list = []

        def printAll():
            nonlocal word_list
            frame = ""
            longest_1st = 0
            longest_2nd = 0
            for w in word_list:
                if longest_1st < len(w[0]):
                    longest_1st = len(w[0])
                if longest_2nd < len(w[1]):
                    longest_2nd = len(w[1])
            for i in range(longest_1st + longest_2nd + 7):
                frame = "".join((frame, "="))
            print(frame)
            for w in word_list:
                for i in range(longest_1st - len(w[0])):
                    w = ("".join((" ", w[0])), w[1])
                for i in range(longest_2nd - len(w[1])):
                    w = (w[0], "".join((w[1], " ")))
                print("".join(("| ", w[0], " : ", w[1], " |")))
            print(frame)

        def printInfo(first, second):
            nonlocal word_list
            word_list.append((first, second))

        def printWithSex(title, li):
            printInfo(title, "".join((str(sum(li)), " (", str(li[0]), ":", str(li[1]), ")")))

        def getRoboInfo():
            total = [0, 0]
            alive = [0, 0]
            power_off = [0, 0]
            old_enough = [0, 0]
            matched = [0, 0]
            avg_matched = 0
            self.current_power = [0, 0]
            self.lastest_gene = 0
            for r in self.robo_list:
                if "♂" == r.sex:
                    sex = 0
                else:
                    sex = 1
                total[sex] += 1
                if "alive" == r.state:
                    alive[sex] += 1
                    self.current_power[sex] += r.power
                elif "power_off" == r.state:
                    power_off[sex] += 1
                elif "old_enough" == r.state:
                    old_enough[sex] += 1
                if r.mate:
                    avg_matched += r.grow
                    matched[sex] += 1
                if self.lastest_gene < r.gene:
                    self.lastest_gene = r.gene
                if self.peak_power < sum(self.current_power):
                    self.peak_power = sum(self.current_power)
            printWithSex("Total Robo", total)
            printInfo("Init #", str(self.robo_init))
            printWithSex("Alive #", alive)
            printWithSex("Power off #", power_off)
            printWithSex("Old enough #", old_enough)
            printWithSex("Current Power", self.current_power)
            printInfo("", "")
            if sum(matched):
                printInfo("Average Matched", self.floatToStr(avg_matched / sum(matched)) + " steps")
                printInfo("Matched Rate", self.floatToStr(sum(matched) / sum(total) * 100) + " %")
            if sum(alive):
                printInfo("Power per Alive", self.floatToStr(sum(self.current_power) / sum(alive)))
            printInfo("Civilization Point", self.floatToStr(self.peak_power / sum(total)))
            printInfo("Peak Power", str(self.peak_power))
            printInfo("Generation", str(self.lastest_gene) + " G")
            if 0 == sum(alive):
                return False
            # CSV_FORM.append((round(time.time()-start_time,2),sum(self.current_power),sum(alive),sum(total)))
            return True
        continued = getRoboInfo()
        printAll()
        if not continued:
            self.byeBye("-- The Silent of the Yard --")

    def get_queue(self):
        return self.yard_queue

    def floatToStr(self, num):
        return str(round(num, 2))

    def byeBye(self, words=""):
        self.end_time = time.time()
        self.ktk.pressToContinue("\n" + words + "\nYard exsits: " + self.floatToStr(self.end_time - self.start_time) + "s\n")
        self.ktk.byeBye()
