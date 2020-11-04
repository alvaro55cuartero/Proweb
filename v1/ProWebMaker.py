import os
import shutil
import errno
import re
import json
from metafiles.modules.tools import ProjectReg, Project, ProjectMaster

PATH = os.path.dirname(os.path.realpath(__file__))
projectReg = ProjectReg(PATH) 
projectMaster = ProjectMaster(PATH)

loop = True
cmds = ["exit", "help", "create", "compile", "project", "load", "list", "delete"]


def struct_json(dire):
	global PROJECT_PATH
	f1 = open(PROJECT_PATH + "\\general\\html\\template.html", 'r')
	f = open(PROJECT_PATH + "\\" + dire + "\\json\\structure.json", "w")
	text = f1.read()
	f1.close()
	struct_tags = re.findall("##[A-z]*##", text)
	text = "{\n"
	for tag in struct_tags:
		text += "\t\"" + tag + "\":{\n\n\t},\n\n"
	text = text[:-3] + "\n\n}"
	f.write(text)
	f.close()


def index_php(path):
	f = open(path + "\\php\\index.php", "w")
	text = """
<?php

include "../../general/php/tools.php";

$html = file_get_contents("../../general/html/template.html");
$html = fromJson("../json/structure.json", $html);
$html = fromJson("../../general/json/structure.json", $html);
echo $html;

?>
"""
	f.write(text)
	f.close()


def cmd_help():
	for x in cmds:
		print(x)


def cmd_create(name):
	global PROJECT_PATH
	tempPath = PROJECT_PATH + "\\" + name
	if projectReg.contains(PROJECT_NAME):
		try:
			os.mkdir(tempPath)
			os.mkdir(tempPath + "\\html")
			os.mkdir(tempPath + "\\php")
			os.mkdir(tempPath + "\\json")
			os.mkdir(tempPath + "\\css")
			os.mkdir(tempPath + "\\js")

			f = open(PROJECT_PATH + "\\ProWebMaker\\Project.json", "r")
			text = f.read()
			f.close()
			input()
			f = open(PROJECT_PATH + "\\ProWebMaker\\Project.json", "w")
			data = json.loads(text)
			print(data[PROJECT_NAME])
			f.write(json.dumps(data))
			f.close()

			index_php(tempPath)
			struct_json(name)
		except Exception as e:
			pass
	else:
		print("First load a project!")
	
	
def cmd_compile():
	struct_json("general")

def cmd_load(name):
	projectMaster.load(name)
	

def cmd_project(name):
	projectMaster.addProject(name)
	#projectReg.addProject(name)
	#cmd_load(name)
	#
	#os.mkdir(PROJECT_PATH + "\\ProWebMaker")
	#copy(PATH + "\\metafiles\\general", PROJECT_PATH + "\\general")
	#f = open(PROJECT_PATH + "\\ProWebMaker\\Project.json", "w")
	#text = json.dumps({PROJECT_NAME:{}})
	#f.write(text)
	#f.close()
	#projectReg.save()


def cmd_list():
	projectMaster.list()

def cmd_delete(name):
	shutil.rmtree(PATH + "\\" + name)

while loop:
	text = input(">").split(" ");

	if text[0] == cmds[0]:
		loop = False
	
	elif text[0] == cmds[1]:
		cmd_help()
	
	elif text[0] == cmds[2]:
		cmd_create(text[1])
	
	elif text[0] == cmds[3]:
		cmd_compile()
	
	elif text[0] == cmds[4]:
		cmd_project(text[1])
	
	elif text[0] == cmds[5]:
		cmd_load(text[1])
	
	elif text[0] == cmds[6]:
		cmd_list()

	elif text[0] == cmds[7]:
		cmd_delete(text[1])

	else:
		print("El commando introducido no es correcto") 




