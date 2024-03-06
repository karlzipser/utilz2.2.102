
imgs={}
fs=sggo(opjD('predict-seg/yolov7-seg3/*.png'))
for f in fs:
    p=imread(f)
    a=fnamene(f)
    b=a.split('-')
    imgname=b[0]
    c=b[1].split(',')
    x=int(c[0])
    y=int(c[1])
    if imgname not in imgs:
        imgs[imgname]={}
    imgs[imgname][(x,y)]=p


    


figure(1);
mx=0
for k in imgs:
    for l in imgs[k]
    png=get_blank_rgb(2064,2464)
    clf()
    a=1.*png
    md=np.median(a.flatten())
    a-=md
    #plt_square()
    r1=0
    r2=0
    for xy in imgs[k]:
        x,y=xy
    #    plot(y,x,'k.')
        t=imgs[k][xy]
        if t>0.6:
            t=1
        else:
            t=0
        r1+=1
        r2+=t
        a[x:x+128,y:y+128,:]=
    #spause()
    a+=md
    png=a.astype(u8)
    sh(png)#png[64:2240,64:2240,1],1,title=pct(r2,r1))
    a=len(imgs[k].values())
    mx=max(a,mx)
    cm(k,a,pct(r2,r1),r=1)
print('max=',mx)




