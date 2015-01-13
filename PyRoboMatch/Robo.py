import threading
import time
import random
import queue

class Robo(threading.Thread):
	'Robo class to create a robo'
	PREG_TIME = 10
	LIFE_LENGTH = 100
	def __init__(self, robo_id, init_pwr, sex, max_idle, yard, dad = None, mom = None, gene = 0):
		threading.Thread.__init__(self)
		self.id = robo_id
		self.power = init_pwr
		self.sex = sex
		self.max_idle = max_idle
		self.yard = yard
		self.msg_queue = yard.get_queue()
		self.dad = dad
		self.mom = mom
		self.gene = gene
		self.age = 0
		self.grow = 0
		self.mate = None
		self.child = []
		self.state = "alive" # alive / power_off / old_enough
		self.setDaemon(True)
		self.start()
	def __del__(self):
		pass

	def run(self):
		while "alive" == self.state:
			if (not self.mate):
				self.age += 1
				self.grow += 1
				# get and read msg
				trgt = self.getMsg()
				self.readMsg(trgt)
				# send self info
				self.sendMsg(self)

			if self.mate and (not self.child):
				self.age += 1

			if (self.mate and self.child):
				self.power -= 1
			# check state
			self.checkHealth()
			# Sleep random time
			self.goSleep(self.max_idle)

	def checkHealth(self):
		if 0 == self.power:
			# Not enough energy
			self.state = "power_off"

		if self.age > Robo.LIFE_LENGTH:
			# Can't hold on anymore
			self.state = "old_enough"


	def isMatch(self, target):
		if not target.mate:
			return target.power == self.power
		else:
			return False

	def adept(self, target):
		if target.power > self.power:
			self.power += 1
		elif target.power < self.power:
			self.power -= 1
		elif target.power == self.power:
			pass

	def sendMsg(self, msg):
		if not self.msg_queue.full():
			self.msg_queue.put(msg)

	def getMsg(self):
		if not self.msg_queue.empty():
			return self.msg_queue.get()
		else:
			return None

	def bornChild(self, restrict = 1):
		if (self.childNum() < restrict)	and ("♀" == self.sex) and (self.mate != None) and ((self.age-self.grow) >= Robo.PREG_TIME):
			# generation digit / dad last name digit / mom last name digit / kid number
			child_gene = self.gene + 1
			child_id = (child_gene)*1000 + (self.mate.id%10)*100 + (self.id % 10) * 10 + self.childNum()
			child_power = int(self.power * (random.choice([0.5, 1, 1.2])))
			child_max_idle = self.max_idle * (random.choice([0.5, 1, 1.2]))
			child_sex = random.choice(["♂","♀"])
			child = Robo(child_id, child_power, child_sex, child_max_idle, self.yard, self.mate, self, child_gene)
			self.child.append(child)
			self.mate.child.append(child)
			return child
		else:
			return None
	def childNum(self):
		return len(self.child)

	def readMsg(self, target):
		if target:
			if (not (target is self)):
				if (target.sex != self.sex):
					# follow the trends
					self.adept(target)
					# check matchability
					if self.isMatch(target):
						self.mate = target
						target.mate = self

	def goSleep(self, multiplexer):
		idle_time = random.random() * multiplexer
		time.sleep(idle_time)
