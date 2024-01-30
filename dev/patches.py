

def getpatches(image,patch_size=(128,128),overlap_size=0):
    num_patches_along_width = (image.shape[1] - patch_size[1]) // (patch_size[1] - overlap_size) + 1
    num_patches_along_height = (image.shape[0] - patch_size[0]) // (patch_size[0] - overlap_size) + 1
    patches = []
    patches_ijs={}
    for i in range(num_patches_along_height):
        for j in range(num_patches_along_width):
            start_i = i * (patch_size[0] - overlap_size)
            start_j = j * (patch_size[1] - overlap_size)
            patch = image[start_i:start_i + patch_size[0], start_j:start_j + patch_size[1]]
            patches.append(patch)
            patches_ijs[d2c(start_i,start_j)]=patch
    return patches_ijs

n=256
imgs={}
patches={}
fs=sggo('/home/karl/Desktop/data/JPEM_2023-12-21-08-31-50/train/mask/*.png')
for f in fs:
    for k in ['mask','png']:
        imgs[k]=rimread(f.replace('mask',k) )
        imgs[k]=imgs[k][:(iheight(imgs[k])//n)*n,:(iwidth(imgs[k])//n)*n,:]
    a=imgs['png']
    a[:,:,2]*=0
    b=imgs['mask'][:,:,0]
    b[b<255]=0
    a[:,:,0]=b
    patches=getpatches(a,patch_size=(n,n),overlap_size=n//2)
    CA()
    sh(patches,r=0)

    dst1=opjD('data/JPEM_2023-12-21-08-31-50/train-patches/1')
    dst0=opjD('data/JPEM_2023-12-21-08-31-50/train-patches/0')
    mkdirp(dst1)
    mkdirp(dst0)
    for p in patches:
        p128=patches[p][(n//4):(-n//4),(n//4):(-n//4),0]
        sh(p128,99)
        a=intr(np.sqrt(sum(p128.flatten()/255)))
        print(shape(p128),a)
        img=1*patches[p]
        img[:,:,0]=img[:,:,1]
        img[:,:,2]=img[:,:,1]
        if a<4:
            dst=dst0
        else:
            dst=dst1
        rimsave(opj(dst,fnamene(f)+'-'+p+'.png'),img)

#
#########################
#

imgs={}
fs=sggo(opjD('TEMP-outputs/*.pkl'))
for q in fs:
    o=lo(q)
    for i in rlen(o['f']):
        p=o['output'][i]
        f=o['f'][i]
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
    png=rimread(opjD('data/JPEM_2023-12-21-08-31-50/train/png',k+'.png'))
    clf()
    sh(png)
    plt_square()
    for xy in imgs[k]:
        x,y=xy
        plot(y,x,'k.')
    spause()
    a=len(imgs[k].values())
    mx=max(a,mx)
    cm(k,a,r=1)
print('max=',mx)



























"""

# reconstruct image from patches_ijs



fs=sggo(opjh('Downloads/1-28-2024-SF-Bay-boats/*.*'))
kprint(fs)
m=[]
for f in fs:
	if ' ' in fname(f):
		m.append(f)
mkdirp(opjh('Downloads/1-28-2024-SF-Bay-boats-duplicates'))
for f in m:
	os_system('mv',qtd(f),qtd(f.replace('1-28-2024-SF-Bay-boats','1-28-2024-SF-Bay-boats-duplicates')),a=1,e=1)



#EOF
=======
masks=sggo(opjD('data/JPEM_2023-12-21-08-31-50/train/mask/*.png'))
for f in masks:
    print(f)
    assert ope(f.replace('mask','png'))
"""





def split_and_save_image_into_four_monochrome_images(imgfilepath,dstfolder):
    mkdirp(dstfolder)
    g=fx(rimread(imgfilepath))
    a,b=g[:,:iwidth(g)//2,:],g[:,-iwidth(g)//2:,:]
    imgs=[]
    imgs.append(a[:iheight(a)//2,:])
    imgs.append(a[-iheight(a)//2:,:])
    imgs.append(b[:iheight(a)//2,:])
    imgs.append(b[-iheight(a)//2:,:])
    n=fnamene(imgfilepath)
    for i in rlen(imgs):
        rimsave(opj(dstfolder,d2p(n,i,'jpg')),imgs[i])

fs=sggo(opjD('data/1-28-2024-SF-Bay-boats/JPG/*.*'))
for f in fs:
    split_and_save_image_into_four_monochrome_images(f,opjD('data/1-28-2024-SF-Bay-boats/JPG-quarters'))

#EOF

