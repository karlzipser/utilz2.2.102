
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
