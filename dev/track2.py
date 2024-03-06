
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
    xcenter=randint(1*scale_factor,imgwidth-1*scale_factor)
    ycenter=randint(1*scale_factor,imgwidth-1*scale_factor)
    width=randint(10,30)
    height=randint(int(width/4),int(width/2))
    direction=np.random.choice([-1,1],1,p=[0.5,0.5])[0]
    dx=3*rndn()/3
    dy=rndn()/3
    return generate_simple_boat(
        xcenter,ycenter,width,height,direction,dx,dy,imgwidth)


def xy2anchors(x,y,imgwidth,scale_factor):
    xa,ya=int(x/scale_factor),int(y/scale_factor)
    xb,yb=xa*scale_factor,ya*scale_factor
    dx,dy=xb-x,yb-y
    return xa,ya,dx,dy


def vectorize_boat(b,scale_factor):
    vb={}
    for kk in ['hull','wake']:
        h=b[kk]
        v=[]
        ks=straskys('width height')
        for k in ks:
            u=0
            if k in h:
                u=h[k]
            v.append(u)
        if 'xcenter' in h and 'ycenter' in h:
            x,y=h['xcenter'],h['ycenter']
        else:
            x,y=0,0
        xa,ya,dx,dy=xy2anchors(x,y,b['meta']['imgwidth'],scale_factor)
        v=[dx,dy]+v
        vb[kk]=dict(xy=(xa,ya),v=v)
    return vb



def devectorize_boat(v):
    b=dict(
        hull=dict(
            xcenter=v[2],
            ycenter=v[3],
            width=v[4],
            height=v[5],
        ),
        wake=dict(
            xcenter=v[6],
            ycenter=v[7],
            width=v[8],
            height=v[9],
        )
    )
    return b






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
            n=obj[k]
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



def get_noisy_version_of_compound_object(cobj,noise_parameter):
    print('noise_parameter=',noise_parameter)
    o={}
    for k in cobj:
        if k!='meta':
            o[k]=get_noisy_version_of_simple_object(cobj[k],noise_parameter)
        else:
            o[k]=deepcopy(cobj[k])
    return o


def get_noisy_version_of_simple_object(obj,noise_parameter):
    q=noise_parameter
    print('q=',q)
    n=deepcopy(obj)
    if False:#q and rnd()<obj['dropout_prob']:#[n['category']]:
        return {}
    ks=['xcenter','ycenter','width','height']
    for k in ks:
        n[k]+=q*rndn()
        if n[k]<=0:
            n[k]=0.1*obj[k]
    return n






if __name__ == '__main__':

    if True:

        imgwidth=256
        nboats=5#randint(1,5)
        nsteps=9 #randint(5,30)
        scale_factor=10
        noise_parameter=5
        boats_through_time=[]


        for i in range(nboats):
            boat=generate_random_simple_boat(imgwidth)
            boats_through_time.append(
                dict(
                    gt=[boat],
                    noisy=[get_noisy_version_of_compound_object(boat,noise_parameter)],
                )
            )


        for i in range(nsteps):
            for j in range(nboats):
                boat=boats_through_time[j]
                if nsteps>1:
                    if len(boat['gt'])>=nsteps:
                        boat['gt'].pop()
                        boat['noisy'].pop()
                        assert len(boat['gt'])==len(boat['noisy'])
                    boat['gt'].insert(0,deepcopy(boat['gt'][0]))
                    move_boat( boat['gt'][0] )
                    noisy=get_noisy_version_of_compound_object(boat['gt'][0],noise_parameter)
                    boat['noisy'].insert(0,noisy)

        for k in ['gt','noisy']:
            figure('a_'+k)
            clf()
            spause();
            xylim(-1,imgwidth+1,-1,imgwidth+1)
            plt_square()
            for j in range(nboats):
                boat=boats_through_time[j]
                for i in range(nsteps):
                    plot_compound_object(boat[k][i],'-')
            spause()



def pixel2simple_boat(p):
    pass

def get_ps(img):
    ps={}
    #k='gt'
    for x in range(shape(img)[0]):
        for y in range(shape(img)[1]):
            p=img[x,y,:]
            if p.max()>0:
                ps[(x,y)]=p

    return ps



final_imgs={}
final_sums={}
for k in ['gt','noisy']:
    imgs=[]
    for t in range(nsteps):
        img=zeros((imgwidth//scale_factor,imgwidth//scale_factor,8))
        for a_boat in boats_through_time:
            noise_level=a_boat[k]
            boat=noise_level[t]
            kprint(boat)
            b=vectorize_boat(boat,10)
            x,y=b['hull']['xy']
            x=bound_value(x,0,imgwidth//scale_factor-1)
            y=bound_value(y,0,imgwidth//scale_factor-1)
            img[x,y,:4]=b['hull']['v']
            x,y=b['wake']['xy']
            x=bound_value(x,0,imgwidth//scale_factor-1)
            y=bound_value(y,0,imgwidth//scale_factor-1)
            img[x,y,4:8]=b['wake']['v']
        imgs.append(img)
    final_img=np.concatenate(imgs,axis=2)
    finalsum=np.abs(final_img).sum(axis=2)
    finalsum[finalsum>0]=1
    sh(np.rot90(finalsum),k)
    final_imgs[k]=final_img
    final_sums[k]=finalsum
del final_img
del finalsum
#ps=get_ps(final_img)
#pv=list(ps.values())

"""
figure(2);clf()
for p in pv:
    plot(p,'.-')
    spause()
    cm(r=1)
"""

for k in ['gt','noisy']:
    objects={}
    indices = np.nonzero(final_sums[k])
    for i in rlen(indices[0]):
        xa,ya=indices[0][i],indices[1][i]
        for t in range(nsteps):
            if t not in objects:
                objects[t]=dict(
                    boats=[],
                    wakes=[],
                )
            a=t*8
            b=t*8+4
            c=t*8+4
            d=t*8+8
            p=final_imgs[k][xa,ya]
            for category,q in zip(['boats','wakes'],[p[a:b],p[c:d]]):
                #cm(t,category,q,r=0)
                dx=q[0]
                dy=q[1]
                width=q[2]
                height=q[3]
                if width*height:
                    objects[t][category].append(
                        dict(
                            xcenter=xa*scale_factor-dx,
                            ycenter=ya*scale_factor-dy,
                            width=width,
                            height=height,
                        )
                    )
    kprint(objects)

    figure('a_'+k)
    for i in range(nsteps):
        for j in range(nboats):
            o=objects[i]['boats'][j]
            plot_bounding_box(o,'k',':')
            o=objects[i]['wakes'][j]
            plot_bounding_box(o,'y',':')

"""
boats_through_time[
    noise_levels t0{
        gt[
            simple_boat{
                meta{}
                hull{
                    xcenter
                    ycenter
                    width
                    height
                }
                wake{
                    xcenter
                    ycenter
                    width
                    height
                }
            }
            simple_boat{
                meta{}
                hull{
                    xcenter
                    ycenter
                    width
                    height
                }
                wake{
                    xcenter
                    ycenter
                    width
                    height
                }
            }
        ]
        noisy[
            ...
        ]
    }
    noise_levels t1{
        gt[
            simple_boat{
                meta{}
                hull{
                    xcenter
                    ycenter
                    width
                    height
                }
                wake{
                    xcenter
                    ycenter
                    width
                    height
                }
            }
            simple_boat{
                meta{}
                hull{
                    xcenter
                    ycenter
                    width
                    height
                }
                wake{
                    xcenter
                    ycenter
                    width
                    height
                }
            }
        ]
        noisy[
            ...
        ]
    }
}



"""
pass

#EOF