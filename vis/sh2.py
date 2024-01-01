

cs=[]

for i in range(ord('0'),ord('9')+1):
    cs.append(chr(i))
for i in range(ord('A'),ord('Z')+1):
    cs.append(chr(i))
for i in range(ord('a'),ord('z')+1):
    cs.append(chr(i))

kprint(cs)