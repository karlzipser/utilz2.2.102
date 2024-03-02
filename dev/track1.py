
from utilz2 import *


colors=dict(
    hull='r',
    wake='b',
)



def generate_simple_boat(
    xcenter,
    ycenter,
    width,
    height,
    direction,
    dx,
    dy,
    imgwidth
):
    assert direction in [1,-1]
    meta=dict(
        direction=direction,
        dx=dx,
        dy=dy,
        imgwidth=imgwidth,
    )
    hull=dict(
        xcenter=xcenter,
        ycenter=ycenter,
        width=width,
        height=height,
        dropout_prob=imgwidth/(imgwidth+width*imgwidth/32),
    )
    if direction>0:
        a=hull['xcenter']/2
        b=hull['xcenter']
    else:
        a=(imgwidth+hull['xcenter'])/2
        b=imgwidth-hull['xcenter']
    wake=dict(
        xcenter=a,
        ycenter=hull['ycenter']-hull['height']/4,
        width=b,
        height=2*hull['height'],
        dropout_prob=imgwidth/(imgwidth+b*imgwidth/((16+32)/2)),
    )
    return dict(
        meta=meta,
        hull=hull,
        wake=wake,
    )


def generate_random_simple_boat(imgwidth):
    xcenter=randint(imgwidth)
    ycenter=randint(imgwidth)
    width=randint(10,30)
    height=randint(int(width/4),int(width/2))
    direction=np.random.choice([-1,1],1,p=[0.5,0.5])[0]
    dx=3*rndn()/3
    dy=rndn()/3
    return generate_simple_boat(
        xcenter,ycenter,width,height,direction,dx,dy,imgwidth)



def move_boat(b):
    h=b['hull']
    nb=generate_simple_boat(
        h['xcenter']+b['meta']['dx'],
        h['ycenter']+b['meta']['dy'],
        h['width'],
        h['height'],
        b['meta']['direction'],
        b['meta']['dx'],
        b['meta']['dy'],
        b['meta']['imgwidth'],
    )
    mergedict(b,nb)


def plot_bounding_box(bb,sym,linetype):
    x0=bb['xcenter']-bb['width']/2
    x1=bb['xcenter']+bb['width']/2
    y0=bb['ycenter']-bb['height']/2
    y1=bb['ycenter']+bb['height']/2
    plot([x0,x1,x1,x0,x0],[y0,y0,y1,y1,y0],sym+linetype)
    plot(bb['xcenter'],bb['ycenter'],'.'+sym)


def plot_compound_object(obj,linetype):
    imgwidth=obj['meta']['imgwidth']
    for k in obj:
        if k!='meta':
            n=obj[k] #get_noisy_version_of_simple_object(obj[k],noisy_parameter)
            if not len(n):
                continue
            noshow=False
            if n['xcenter']<0 or n['xcenter']>imgwidth:
                noshow=True
            if n['ycenter']<0 or n['ycenter']>imgwidth:
                noshow=True
            if n['width']>imgwidth or n['height']>imgwidth:
                noshow=True

            if len(n) and not noshow:
                plot_bounding_box(n,colors[k],linetype)



def get_noisy_version_of_compound_object(cobj,noisy_parameter):
    o={}
    for k in cobj:
        if k!='meta':
            o[k]=get_noisy_version_of_simple_object(cobj[k],noisy_parameter)
        else:
            o[k]=deepcopy(cobj[k])
    return o


def get_noisy_version_of_simple_object(obj,noisy_parameter):
    q=noisy_parameter
    n=deepcopy(obj)
    if q and rnd()<obj['dropout_prob']:#[n['category']]:
        return {}
    ks=['xcenter','ycenter','width','height']
    for k in ks:
        n[k]+=q*rndn()
        if n[k]<=0:
            n[k]=0.1*obj[k]
    return n




if __name__ == '__main__':

    if True:
        figure(1)
        clf()
        imgwidth=256
        nboats=randint(1,5)
        nsteps=50 #randint(5,30)
        boats_through_time=[]

        for i in range(nboats):
            boat=generate_random_simple_boat(imgwidth)
            boats_through_time.append(
                dict(
                    gt=[boat],
                    noisy=[get_noisy_version_of_compound_object(boat,1.)],
                )
            )

        for i in range(nsteps):

            #clf()
            xylim(-1,imgwidth+1,-1,imgwidth+1)
            plt_square()

            for j in range(nboats):
                boat=boats_through_time[j]
                if i+1==nsteps:
                    plot_compound_object(boat['gt'][0],'-')
                plot_compound_object(boat['noisy'][0],':')


        
                if len(boat['gt'])>=nsteps:
                    boat['gt'].pop()
                    boat['noisy'].pop()
                    assert len(boat['gt'])==len(boat['noisy'])
                boat['gt'].insert(0,boat['gt'][0])
                move_boat( boat['gt'][0] )
                noisy=get_noisy_version_of_compound_object(boat['gt'][0],1.)
                boat['noisy'].insert(0,noisy)

            spause()
            time.sleep(1/60)




#EOF