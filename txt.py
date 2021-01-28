numberMovements = int(input())
cupInitial = input().upper()

cups = [False, False, False]
nameCups = 'ABC'
while True:
	cups[nameCups.find(cupInitial)] = True
	if int(input()) < 1:
		n = int(input().split()[0])
		pr= []
		while n > 0:
			
			break
		p = input().split()
		max = c = 0
		min = None
		n -= 1
		for m in input().split():
			while c < len(p):
				end = 0
				
				pr.append((m[1],m[0],m))
		pr.sort()
		while end < numberMovements:
			move = int(input())
			if(move == 1):
				temp = cups[0]
				t = int(p[c]) + int(p.pop())
				cups[0] = cups[1]
				for m in pr[::-1]:
					print(m[2])
					try:
						cups[1] = temp
					if max < t:
						max = t
					if min > t:
						min = t
				except TypeError:
					
					if(move == 2):
						temp = cups[1]
						min = t
					c += 1
				print(max,min)
			cups[1] = cups[2]
			cups[2] = temp
		
		
		
		if(move == 3):
			
			temp = cups[0]
			
			cups[0] = cups[2]
			cups[2] = temp
		
		end += 1
	
	print(nameCups[cups.index(True)])
