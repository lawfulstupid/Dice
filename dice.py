import random
from functools import reduce
from math import ceil, log10

class Die:

	def __init__(self, pdf):
		self.pdf = pdf
		if None in self.pdf:
			del self.pdf[None]
		self.totalWeight = sum(pdf.values())
	
	@staticmethod
	def d(n,s=None):
		if s == None:
			s = n
			n = 1
		pdf = {}
		for i in range(s):
			pdf[i+1] = 1
		d = Die(pdf)
		t = Die({0: 1})
		for i in range(n):
			t = t + d
		return t
	
	@staticmethod
	def pure(n):
		if n == None:
			return Die({})
		else:
			return Die({n: 1})
	
	@staticmethod
	def zero():
		return Die.pure(0)
	
	@staticmethod
	def wrap(d):
		return d if isinstance(d, Die) else Die.pure(d)
	
	def __iter__(self):
		return self.pdf.__iter__()
	
	def __next__(self):
		return self.pdf.__next__()
	
	def roll(self):
		r = random.uniform(0, self.totalWeight)
		s = 0
		for value in self:
			s += self[value]
			if r <= s:
				return value
	
	def explode(self, limit = 9):
		return self.map(lambda n: Die.pure(n) + (self.explode(limit - 1) if n == self.getMax() and limit > 0 else 0))
	
	def avg(self):
		s = 0
		for value in self:
			s += value * self[value]
		return s
	
	def getMax(self):
		return max(self.pdf.keys())
	
	def getMin(self):
		return min(self.pdf.keys())
	
	def prob(self, test):
		successes = 0
		failures = 0
		for value in self.pdf:
			result = Die.wrap(test(value))
			successes += self.pdf[value] * result[True]
			failures += self.pdf[value] * result[False]
		return successes / float(successes + failures)
	
	def values(self):
		values = list(self.pdf.keys())
		values.sort()
		return values
	
	def map(self, f):
		pdf = {}
		for value in self:
			result = Die.wrap(f(value))
			for newValue in result:
				if (newValue != None):
					pdf[newValue] = pdf.get(newValue, 0) + self[value] * result[newValue]
		return Die(pdf)

	def filter(self, test, failValue=0):
		return self.map(lambda x: x if test(x) else failValue)
	
	def combine(this, that, f):
		pdf = {}
		that = Die.wrap(that)
		for a in this:
			for b in that:
				value = f(a,b)
				pdf[value] = pdf.get(value,0) + this[a]*that[b]
		return Die(pdf)
	
	def compare(this, that, f):
		return this.combine(that, lambda a,b: int(f(a,b)))
	
	def __getitem__(self, value):
		return self.pdf.get(value,0) / float(self.totalWeight)
	
	def __add__(this, that):
		return this.combine(that, lambda a,b: a+b)
	
	def __sub__(this, that):
		return this.combine(that, lambda a,b: a-b)
	
	def __mul__(this, that):
		return this.combine(that, lambda a,b: a*b)
	
	def __xor__(this, that):
		return this.combine(that, max)
	
	def __truediv__(this, that):
		return this // that
	
	def __floordiv__(this, that):
		return this.combine(that, lambda a,b: a // b)
	
	def __mod__(this, that):
		return this.combine(that, lambda a,b: a % b)
	
	def __pow__(this, that):
		return this.combine(that, lambda a,b: a ** b)
	
	def __and__(this, that):
		return this.combine(that, lambda a,b: (a,b))
	
	def __or__(this, that):
		return this.combine(that, lambda a,b: max(a,b))
	
	def __eq__(this, that):
		return this.compare(that, lambda a,b: a == b)
	
	def __ne__(this, that):
		return this.compare(that, lambda a,b: a != b)
	
	def __le__(this, that):
		return this.compare(that, lambda a,b: a <= b)
	
	def __lt__(this, that):
		return this.compare(that, lambda a,b: a < b)
	
	def __ge__(this, that):
		return this.compare(that, lambda a,b: a >= b)

	def __gt__(this, that):
		return this.compare(that, lambda a,b: a > b)
	
	def __repr__(self):
		return reduce(lambda a,b: a + "\n" + b, self.lines())
	
	def __str__(self):
		return reduce(lambda a,b: a.strip() + ", " + b.strip(), self.lines())
	
	def lines(self):
		longestValue = 0
		longestProb = 0
		for value in self:
			longestValue = max(longestValue, len(str(value)))
			longestProb = max(longestProb, 2-ceil(log10(self[value])))
		valueFormat = "{0:>" + str(longestValue) + "s}"
		probFormat = "{1:." + str(longestProb) + "f}"
		format = valueFormat + ": " + probFormat
		return list(map(lambda value: format.format(str(value), self[value]), sorted(self.pdf)))
	
	def graph(self, screenWidth=100):
		maxNumWidth = 0
		maxProb = 0
		for n in self:
			maxNumWidth = max(maxNumWidth, len(str(n)))
			maxProb = max(maxProb, self[n])
		for n in self.values():
			print(str(n).rjust(maxNumWidth), end=' | ')
			bar_len = int(round(screenWidth * self[n] / maxProb))
			for i in range(bar_len):
				print('#', end='')
			print()

d = Die.d
coin = Die({0: 1, 1: 1})
d2 = d(2)
d4 = d(4)
d6 = d(6)
d8 = d(8)
d10 = d(10)
d12 = d(12)
d20 = d(20)
d100 = d(100)
fudge = Die({-1: 2, 0: 2, 1: 2})
chaos = d4+d6+d8+d10+d12

def test(confirmer):
	dice = [d4, d6, d8, d10, d12]
	for i in range(5):
		for j in range(i,5):
			da = dice[i]
			db = dice[j]
			result = (da & db).map(lambda r: confirmer(r[0], da, db) * 2 - 1 if r[0] == r[1] else 0)
			print("{0:f}\t{1:f}\t{2:f}".format(result[-1], result[0], result[1]))
