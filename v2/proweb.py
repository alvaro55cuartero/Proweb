import Proweb.Commands.Commands as Commands
import Proweb.Commands.Elements as Elements
import Proweb.Commands.Snippets as Snippets
import Proweb.Commands.Process as Process
import Proweb.Commands.Tasks as Tasks
import Proweb.Commands.Libs as Libs
import Proweb.Exceptions as Ex
import Proweb.Output as Output
import Proweb.Tools as Tools
import Proweb.Input as Input
import Proweb.Order as Order
import Proweb.Conf as C

import threading
import pathlib
import shutil
import json
import time
import glob
import sys
import re
import os



class Main(Commands.Commands):
	def __init__(self):
		self.snippets = Snippets.Snippets();
		self.elements = Elements.Elements();
		self.checkDir();

	
	def cmd_echo(self, args):
		"""Repeats the input"""
		print(args[0])


	def cmd_echo(self, c, t):
		"""Repeats the input with color"""
		Output.ColorPrint(c, t)

	
	def cmd_exit(self, *args):
		"""Exits the program"""
		return True;

	
	def cmd_show(self, *args):
		"""Shows hirachical tree of current dir"""
		if len(args) == 1:
			Order.tree(C.DIR, int(args[0]));
		else:
			Order.tree(C.DIR);


	def cmd_cd(self, *args):
		"""Changes directory"""
		temp = (C.DIR / args[0]).resolve();
		if not temp.is_relative_to(C.ROOT):
			print("No puedes subir mas!");
			return 
		C.DIR = temp;
		self.checkDir();
	

	def cmd_pwd(self):
		"""Shows current path"""
		print(C.DIR);


	def cmd_mkdir(self, *args):
		"""Creates new dir"""
		args = C.DIR / args[0]
		Tools.mkdir(args);


	def cmd_mkfile(self, *args):
		"""Creates new file"""

		if len(args) > 1:
			Tools.mkfile(args[0], args[1]);
			return
		Tools.mkfile(args[0]);


	def cmd_rm(self, *args):
		"""Removes file/dir"""
		Tools.rm(C.DIR / args[0]);


	def cmd_cp(self, *args):
		"""Copies file/dir"""
		Tools.cp(args[0], args[1]);


	def cmd_mv(self, *args):
		"""Moves file/dir"""
		Tools.mv(args[0], args[1]);


	def cmd_read(self, *args):
		"""Reads file"""
		print(Tools.read(args[0]));


	def cmd_init(self, *args):
		if not Tools.exists(C.DIR / "proweb.json"):
			props = {};
			props["name"] = input("Name: ");
			props["elements"] = "./IN/ELEMENTS/";
			snips = input("Snippets [E]mpty [D]efault:");
			if snips == "E":
				props["snippets"] = {};
			elif snips == "D":
				props["snippets"] = {
					"GET":"document.querySelector",
    				"GETALL":"document.querySelectorAll",
    				"NEW":"document.createElement",
    				"CHILD":"appendChild",
    				"EVENT":"addEventListener"
    			}
			else:
				print("No project was created");
				return

			Tools.writeJson(C.DIR / "proweb.json", props);
			Tools.mkdir(C.DIR / "IN");
			Tools.mkdir(C.DIR / "IN" / "CSS");
			Tools.mkdir(C.DIR / "IN" / "JS");
			Tools.mkdir(C.DIR / "IN" / "ELEMENTS");
			Tools.mkfile(C.DIR / "index.html");
		else:
			print("there is another project in this folder");

	def cmd_process(self, *args):
		"""Process Web"""
		Process.call(C.DIR);


	def cmd_tasks(self, *args):
		"""Task commands"""
		Tasks.command(args);


	def cmd_libs(self, *args):
		"""Libs commands"""
		Libs.command(args, Main.DIR);


	def cmd_elements(self, *args):
		"""Elements commands"""
		self.elements.call(*args);


	def cmd_project(self, *args):
		"""Project commands"""
		Project.command(args, Main.DIR);


	def cmd_snippet(self, *args):
		"""Snippets commands"""
		self.snippets.call(*args);


	def checkDir(self):
		if Tools.exists(C.DIR / "proweb.json"):
			txt = Tools.readJson(C.DIR / "proweb.json");
			C.P_NAME = f" [Pro-{txt['name']}]";
			C.P_FILE = C.DIR / "proweb.json";
			C.P_PATH = C.DIR;

		elif Tools.exists(C.DIR / "lib.json"):
			txt = Tools.read(C.DIR / "lib.json");
			data = json.loads(txt);
			C.P_NAME = f" [Lib-{data['name']}";
			C.P_FILE = C.DIR / "lib.json";
			C.P_PATH = C.DIR;
		
		else:
			C.P_NAME = "";
			C.P_FILE = pathlib.Path();
			C.P_PATH = pathlib.Path();



def Run():
	global exit, main
	while not exit.is_set():
		try:
			Tasks.process(main.call);
			exit.wait(10);
		except KeyboardInterrupt:	
			pass
	print("\nbye...");


main = Main();
exit = threading.Event()
inputThread = Input.Input(exit, main.call);

Run();