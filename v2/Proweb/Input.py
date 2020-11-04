import pathlib
import os
import threading

class Input(threading.Thread):
	def __init__(self,exit, DIR, PRO, input_cbk = None, name='keyboard-input-thread'):
		self.input_cbk = input_cbk
		self.exit = exit;
		self.DIR = DIR;
		self.PRO = PRO;
		self.loop = True;
		super(Input, self).__init__(name=name)
		self.start()

	def run(self):
		while self.loop:
			a = ""
			if self.PRO != "":
				a = "[" + str(self.PRO) + "]";
			a += "(" + os.path.basename(self.DIR) + ")";

			try:
				a = input(a).split(" ");
			except EOFError as e:
				break

			self.loop = self.input_cbk(a);
		self.exit.set()

	def setDir(DIR):
		self.DIR = DIR;

	def setPRO(PRO):
		self.PRO = PRO;