import Proweb.Commands.Commands as Commands
import Proweb.Tools as Tools
import Proweb.Conf as C

import glob as glob;
import re as re;

class Elements(Commands.Commands):

	def __init__(self):
		super().__init__();

	
	def cmd_create(self, name, path = None):
		"""Creates a dir with {name}.html {name}.css {name}.js"""

		if path == None:
			if C.P_FILE == None:
				print("No estas dentro de un projecto");
				return	
			DIR = Tools.readJson(C.P_FILE)["elements"];
		else:	
			DIR = path / name;

		Tools.mkdir(DIR);
		Tools.mkfile(DIR / f"{name}.html");
		Tools.mkfile(DIR / f"{name}.js");
		Tools.mkfile(DIR / f"{name}.css");