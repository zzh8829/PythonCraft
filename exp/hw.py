import time


n = 100
win1 = 0

for x in range(n):
	t1 = time.time()
	s = 0
	for x in range(100):
		for i in range(16):
			for j in range(16):
				for k in range(16):
					s+=1


	t2 = time.time()
	d1 = t2-t1

	s = 0
	for x in range(100):
		for i in range(16*16*16):
			s+=1
	t3 = time.time()
	d2 = t3-t2

	if d1<d2: win1 +=1

	print(d1<d2)

print(win1/n)