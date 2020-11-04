import shutil
import os


def mkdir(ruta):
	try:
		os.mkdir(ruta);
	except Exception as e:
		print("Error");

def mkfile(path, text=""):
	try:
		f = open(path, "w");
		f.write(text);
		f.close();
	except Exception as e:
		print("Error");

def rmdir(path):
	try:
		shutil.rmtree(path);
	except Exception as e:
		print("Error");

def rmfile(path):
	try:
		os.remove(path);
	except Exception as e:
		print("Error");

def rm(path):
	if os.path.isdir(path):
		rmdir(path);
	elif os.path.isfile(path):
		rmfile(path);

def mv(src, dst):
	try:
		shutil.move(src, dst);
	except Exception as e:
		print("Error")

def cp(src, dst):
	try:
		shutil.copytree(src, dst);
	except Exception as e:
		print("Error");


def read(path):
	try:
		f = open(path, "r");
		text = f.read();
		f.close();
		return text;
	except Exception as e:
		print("Error");


