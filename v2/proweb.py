import Proweb.Commands.Elements as Elements
import Proweb.Commands.Process as Process
import Proweb.Commands.Tasks as Tasks
import Proweb.Commands.Libs as Libs
import Proweb.Exceptions as Ex
import Proweb.Tools as Tools
import Proweb.Input as Input
import Proweb.Order as Order

import threading
import pathlib
import shutil
import json
import time
import glob
import sys
import re
import os

def checkDir(DIR, PRO):
	global inputThread;

	if Tools.containsFile(DIR / "lib.json"):
		txt = Tools.read(DIR / "lib.json");
		data = json.loads(txt);
		PRO = "[Lib]-" + data["name"];
	else:
		PRO = "";

	inputThread.setPRO(PRO);


class Commands():

	def __init__(self):
		self.DIR = pathlib.Path(os.getcwd())
		self.PRO = "";

	
	def cmd_echo(self, args):
		print(args[0])

	
	def cmd_exit(self):
		return True;

	
	def cmd_show(self, *args):
		if len(args) > 0:
			Order.tree(self.DIR, int(args[0]));
		else:
			Order.tree(self.DIR);


	def cmd_cd(self, *args):
		self.DIR = (self.DIR / args[0]).resolve();
		checkDir(self.DIR, self.PRO );
		inputThread.setDIR(self.DIR);
	

	def cmd_pwd(self):
		print(self.DIR);


	def cmd_mkdir(self, *args):
		Tools.mkdir(args[0]);


	def cmd_mkfile(self, *args):
		if len(args) > 1:
			Tools.mkfile(args[0], args[1]);
			return
		Tools.mkfile(args[0]);


	def cmd_rm(self, *args):
		Tools.rm(self.DIR / args[0]);


	def cmd_cp(self, *args):
		Tools.cp(args[0], args[1]);


	def cmd_mv(self, *args):
		Tools.mv(args[0], args[1]);


	def cmd_read(self, *args):
		print(Tools.read(args[0]));


	def cmd_process(self):
		Process.command();


	def cmd_tasks(self, *args):
		Tasks.command(args);


	def cmd_libs(self, *args):
		Libs.command(args, self.DIR);


	def cmd_elements(self, *args):
		Elements.command(args);


	def cmd_project(self, *args):
		Project.command(args, self.DIR);


	
	def callFunction(self, args):
		fn = getattr(self, 'cmd_' + args[0], None)
		if fn is not None:
			return not fn(*args[1:])
		else:
			print("No function call: " + args[0]);

		return True;


def Run():
	global exit, cmds
	while not exit.is_set():
		try:
			Tasks.process(cmds.callFunction);
			exit.wait(10);
		except KeyboardInterrupt:	
			pass
	print("\nbye...");


cmds = Commands();
exit = threading.Event()
inputThread = Input.Input(exit, cmds.DIR, cmds.PRO, cmds.callFunction);
Run();