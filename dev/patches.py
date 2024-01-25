"""
if 'image' not in locals():
	image = cv2.imread('large_image.jpg')

image=image[:(2064//128)*128,:(2464//128)*128,:]

patch_size = (128, 128)
overlap_size = 0

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

sh(patches_ijs)
print(shape(image),len(patches_ijs))
"""

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


"""

masks=sggo(opjD('data/JPEM_2023-12-21-08-31-50/train/mask/*.png'))
for f in masks:
    print(f)
    assert ope(f.replace('mask','png'))
"""