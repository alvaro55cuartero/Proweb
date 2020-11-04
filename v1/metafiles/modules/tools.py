import os
import shutil
import errno
import re
import json

def copy(src, dest):
	try:
		shutil.copytree(src, dest)
	except OSError as e:
		if e.errno == errno.ENOTDIR:
			shutil.copy(src, dest)
		else:
			print('Directory not copied. Error: %s' % e)


class ProjectReg:

	def __init__(self, path):
		self.PATH = path
		self.data = json.loads(open(self.PATH + "\\metafiles\\register\\Projects.json", "r").read())

	def addProject(self, name):
		if name not in self.data: 
			self.data.append(name)
			self.save()

	def delProject(self, name):
		if name in self.data:
			self.data.remove(name)
			self.save()

	def list(self):
		for e in self.data:
			print(e)

	def contains(self, name):
		if name in self.data:
			return True
		else:
			return False

	def save(self):
		open(self.PATH + "\\metafiles\\register\\Projects.json", "w").write(json.dumps(self.data))

class Project:
	def __init__(self, name, path):
		self.name = name
		self.path = path
		self.tab = []
		
	def addTab(self, name):
		if name not in self.tab:
			self.tab.append(name)

	def create(self):
		os.mkdir(self.path + "\\" + self.name)

	def remove(self):
		shutil.rmtree(self.path + "\\" + name)

	def delTab(self, name):
		if name in self.tab:
			self.tab.remove(name)

class ProjectMaster:
	currentProject = None
	
	def __init__(self, path):
		self.path = path
		self.projectReg = ProjectReg(path)
		self.projects = []
		self.loadFile()

	def loadFile(self):
		for name in self.projectReg.data:
			self.projects.append(Project(name, self.path))

	def list(self):
		self.projectReg.list()

	def contains(self, name):
		for p in self.projects:
			if p.name == name:
				return True
		return False


	def getProject(self, name):
		for p in self.projects: 
			if p.name == name:
				return p
		return None

	def getNames(self):
		temp = []
		for p in self.projects:
			temp.append(p.name)
		return temp

	def addProject(self, name):
		if not self.contains(name):
			p = Project(name, self.path)
			p.create()
			self.projects.append(p)
			self.projectReg.addProject(name)
		self.load(name)

	def delProject(self, name):
		if self.contains(name):
			p = self.getProject(name)
			p.remove()
			self.projects.remove(p)
			self.projectReg.delProject(name)
			print("Project " + name + " was deleted")

	def load(self, name):
		p = self.getProject(name)
		if p != None:
			self.currentProject = p
			print("Project " + name + " selected!")
		else:
			print("There is no project with name: " + name)
