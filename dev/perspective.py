
from utilz2.torch_.init import *
from PIL import Image
#CA(); quit_Preview()

q=samimgs()
a0=q.sf[300:,300:,:]
a=embedinsquare(a0)
a=a[:,:,:3]
b=Image.fromarray(a)
h=iheight(a)
w=iwidth(a)
y=h-1
x=w-1
x0=0
y0=y//2
w=int(0.95*y/2)
#u=[[int(y*.4),0],[int(y*0.4),x//2],[int(y*0.6),x//2],[int(y*0.6),0]]
g=[[0,0],[0,x],[y,x],[y,0]]
h=[[0, 0], [w, x+300], [y-w, x+300], [y, 0]]
c=torchvision.transforms.functional.perspective(
    img=b,
    startpoints=g,
    endpoints=h,
    fill=(255,0,0)
)
#b.show(title='b')
#c.show(title='c')
sh(na(a0),1)
sh(na(c),2)