
import time

class Looper:

	def __init__(self):
		self.a = "asdfasdfasdfasdf"
		self.n = len(self.a)

	def loop(self):

		t1 = time.time()
		for i in range(33):
			for j in range(33):
				for k in range(16):
					b = 10
					c = b<<4
					d = c>>4
					asdf = i*j*k
					kk = asdf%self.n
					dd = self.a[kk]
					dd2 = self.a[kk]
					dd3 = self.a[kk]
					dd4 = self.a[kk]
					dd5 = self.a[kk]
		return time.time()-t1

lp = Looper()
import loopc
lpc = loopc.Looper()

t1 = 0
for i in range(10):
	t1 += lpc.loop()

print(t1)

t2 = 0
for j in range(1):
	t2 += lp.loop()
print(t2)

