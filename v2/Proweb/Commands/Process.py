import Proweb.ProcessHTML as HTML
import Proweb.ProcessJS as JS
import Proweb.Tools as Tools

import glob as glob;
import re as re;

HTMLS = {};



def searchLibs(OUT):
	global HTMLS
	files = list(OUT.glob("**/*.html"));

	for file in files:
		name = file.name[:-5]
		HTMLS[name] = {}
		HTMLS[name]["link"] = file; 
		HTMLS[name]["process"] = False;

def addScript(path):
	script = "<script src='" + path + "'></script>\n";
	HTMLS["index"]["text"] = HTMLS["index"]["text"].replace("</body>", "</body>" + script);

def processJS(DIR, name, args = []):
	path = "OUT/JS/" + name +".js";
	if Tools.exists(DIR / path):
		snippets = Tools.readJson("proweb.json")["snippets"];
		print("processing: " +name);
		path = "OUT/JS/" + name + ".js"
		text = Tools.read(path);

		for arg in args:
			print("arg:" + arg);
			text = arg + ";" + text;

		for k, v in snippets.items():
			k = "(?<=[\s\.])" + k + "\(";
			text = re.sub(k, v + "(", text);


		path = "EXT/JS/" + name + ".js"
		Tools.write(DIR / path , text);
		addScript("./JS/" + name + ".js");


def processChild(DIR, name):
	lista = re.findall(r"<(pro-[^\s]*)(.*)>(.*)</pro-.*>", HTMLS[name]["text"]);

	for item, args, content in lista:
		if not HTMLS[item]["process"]:
			process(DIR, item, args);

		HTMLS[name]["text"] = re.sub("<" + item + ".*>.*</" + item +">", HTMLS[item]["text"], HTMLS[name]["text"]);



def process(DIR, name, arg=[]):
	global HTMLS

	print("pro: " + name);

	HTMLS[name]["text"] = Tools.read(HTMLS[name]["link"]);
	
	processJS(DIR, name, arg);
	processChild(DIR, name);

	HTMLS[name]["process"] = True;



def call(DIR, *args):
	global HTMLS
	IN = DIR / "IN";
	OUT = DIR / "OUT";
	EXT = DIR / "EXT";

	Tools.rm(EXT);
	Tools.mkdir(EXT);
	Tools.mkdir(EXT / "JS");

	Tools.rm(OUT);
	Tools.cp(IN, OUT);

	searchLibs(OUT);
	process(DIR, "index");
	processJS(DIR, "tools");


	Tools.write(EXT / "index.html" , HTMLS["index"]["text"]);

	Tools.cp(OUT / "CSS", EXT / "CSS");

	Tools.rm(OUT)
	print("fin");