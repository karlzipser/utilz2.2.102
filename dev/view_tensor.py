from utilz2 import *
from utilz2.torch_.init import *



def get_image_of_tensor(a,mapping,max_num_batches_to_show=0,warn_if_nan=True):

	if not max_num_batches_to_show:
		max_num_batches_to_show=a.size()[0]

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

	ds={}
	for channel_n in rlen(cs):
		c=cs[channel_n]
		d={}
		for batch_n in range(min(max_num_batches_to_show,c.size()[0])):
			d[batch_n]=c[batch_n,:].detach().cpu().numpy().transpose(1,2,0)
		ds[channel_n]=d
	#kprint(ds)

	rows=[]
	top=True
	for k in ds:
		rows.append(get_image_row(list(ds[k].values()),blank_width=1,top_blank=top,warn_if_nan=warn_if_nan))
		top=False
	g=get_image_column(rows)
	return g


if __name__ == '__main__':
	bs=4
	a=torch.randn(bs,5,10,20)
	mapping={
		0:0,
		1:1,
		2:None,
		3:2,
		4:2,
		5:2,
		6:0,
		7:None,
		8:None,
	}
	g=get_image_of_tensor(a,mapping,3)
	sh(g,r=1)


#EOF
