import re;


class iterable:
	def __init__(self, list):
		self.list = list;
		self.max = len(self.list)
		self.count = -1;

	def next(self):
		if self.count + 1 >= self.max:
			return None;
		else: 
			return self.list[self.count + 1];

	def move_next(self):
		if self.next():
			self.count += 1;
			return self.list[self.count];
		return None

	def scan(self, regex):
		r = "";
		while re.search(regex, self.next()):
			r += self.move_next();
		return r;

	def scanUntil(self, char):
		r = "";
		while not self.next() in (char, None):
			r += self.move_next();
		return r;

def lexer(path):
	file = open(path, "r");
	ite = iterable(list(file.read()));
	r = []
	temp = ""
	i = ite.next()
	while i:
		if i in '"':
			temp += ite.move_next()
			temp += ite.scanUntil('"');
			temp += ite.move_next();
			r.append(("string",temp));

		elif re.search("[\{\}\[\]\(\)\;]", i):
			r.append(("separator",ite.move_next()));
		
		elif re.search("[\+\-\*\/\=]", i):
			temp += ite.scan("[\*\+\-\/\=]")
			r.append(("operator",temp));

		elif re.search("[a-zA-Z]", i):
			temp += ite.scan("[a-zA-Z0-9]");
			if temp in ("var", "fun", "for", "in", "while", "ret", "if", "elif", "else"):
				r.append(("keyword", temp))
			else:
				r.append(("identifier", temp))

		elif re.search("[.0-9]", i):
			while re.search("[0-9]", ite.next()):
				temp += ite.move_next();
			r.append(("number", temp))

		else:	
			ite.move_next()

		i = ite.next()
		temp = ""
	file.close()
	return r;


def parser(tokens):
	ite = iterable(tokens);
	r = [];
	i = ite.next()

	while i:
		fun, name = ite.next()
		print fun + " " + name
		if fun is "keyword":
			if fun is "var":
				
		if fun is "operator":
			ite.move_next;
			sentence =  

		r.append(sentence); 
		i = ite.next();

	return r;



tokens = lexer("Test.pw")
parser(tokens);


