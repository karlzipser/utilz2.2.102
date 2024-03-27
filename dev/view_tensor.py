from utilz2 import *
from utilz2.torch_.init import *

a=torch.randn(2,5,10,20)
mapping={
	0:0,
	1:1,
	2:None,
	3:2,
	4:2,
	5:2,
}
ks=kys(mapping)
for i in range(max(ks)+1):
	assert i in ks
s=a.size()
b=torch.zeros(s[0],max(ks)+1,s[2],s[3])
for k in ks:
	if mapping[k] is not None:
		b[:,k,:,:]=a[:,mapping[k],:,:]
cs=[]
for i in range(0,max(ks)+1,3):
	cs.append(b[:,i:i+3,:,:])

ds=[]
for c in cs:
	d=[]
	for i in range(c.size()[0]):
		d.append(c[i,:])
	ds.append(d)