
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