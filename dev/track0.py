
from utilz2 import *


def dict2nums(d,v=[]):
    for k in d:
        print(k)
        if type(d[k]) is dict:
            if len(d[k]):
                r=dict2nums(d[k],[])
                v+=r
            else:
                assert False
        elif type(d[k]) is list:
            vals=d[k]
            for _a in vals:
                assert is_number(_a)
            assert(len(vals))
            v+=vals
        elif is_number(d[k]):
            v.append(d[k])
        else:
            assert False
    return v


colors=dict(
    hull='r',
    wake='b',
)
dropout_prob=dict(
    hull=1/4,
    wake=1/8,
)


def generate_simple_boat(xcenter,ycenter,width,height,direction,imgwidth):
    assert direction in [1,-1]
    meta=dict(
        direction=direction,
        imgwidth=imgwidth,
    )
    hull=dict(
        xcenter=xcenter,
        ycenter=ycenter,
        width=width,
        height=height,
        dropout_prob=imgwidth/(imgwidth+width*imgwidth/16),
    )
    if direction>0:
        a=hull['xcenter']/2
        b=hull['xcenter']
    else:
        a=(imgwidth+hull['xcenter'])/2
        b=imgwidth-hull['xcenter']
    wake=dict(
        xcenter=a,
        ycenter=hull['ycenter'],
        width=b,
        height=hull['height'],
        dropout_prob=imgwidth/(imgwidth+b*imgwidth/16),
    )
    return dict(
        meta=meta,
        hull=hull,
        wake=wake,
    )


def move_boat(b,dx,dy):
    h=b['hull']
    nb=generate_simple_boat(
        h['xcenter']+dx,
        h['ycenter']+dy,
        h['width'],
        h['height'],
        b['meta']['direction'],
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
            n=obj[k] #get_noise_version_of_simple_object(obj[k],noise_parameter)
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



def get_noise_version_of_compound_object(cobj,noise_parameter):
    o={}
    for k in cobj:
        if k!='meta':
            o[k]=get_noise_version_of_simple_object(cobj[k],noise_parameter)
        else:
            o[k]=deepcopy(cobj[k])
    return o


def get_noise_version_of_simple_object(obj,noise_parameter):
    q=noise_parameter
    n=deepcopy(obj)
    if q and rnd()<obj['dropout_prob']:#[n['category']]:
        return {}
    n['xcenter']+=q*rndn()
    n['ycenter']+=q*rndn()
    n['width']+=q*rndn()
    n['height']+=q*rndn()
    return n



if __name__ == '__main__':
    if False:
        d=dict(
            a=1,
            c=[3,4.,5.],
            b=2,
            d=dict(
                a=1,
                c=[3,4.,5.],
                b=2,
                b2=22,
                f=dict(
                    aa=100,
                    cc=[300,400.,500.],
                    bb=200,
                    bb2=220,
                ),
            ),
            x=6,
            y=7, 
        )
        v=dict2nums(d)
        kprint(d,title='d')
        kprint(v,title='v')

    if True:
        imgwidth=256
        clf()
        a=generate_simple_boat(200,150,20,5,-1,imgwidth)
        b=generate_simple_boat(100,100,5,3,1,imgwidth)

        for i in range(100):
            a_=get_noise_version_of_compound_object(a,4.)
            b_=get_noise_version_of_compound_object(b,4.)
            clf()
            plot_compound_object(a,':')
            plot_compound_object(a_,'-')
            plot_compound_object(b,':')
            plot_compound_object(b_,'-')


            xylim(-1,imgwidth+1,-1,imgwidth+1)
            plt_square()
            spause()

            move_boat(a,-1,0.1)
            move_boat(b,3,-0.3)

            time.sleep(1/30)

if False:
    x,y=[],[]
    for i in range(512):
        x.append(i)
        y.append(512/(512+i*512/16))
    plot(x,y)


#EOF