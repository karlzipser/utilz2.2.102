a=find_files(
    #start='/Users/karlzipser/Library/Photos/Libraries/Syndication.photoslibrary',
    #start='Library/Messages 10-5-2023/Attachments',
    opjD(),
    patterns=[
    #'5.png'
    '*.jpeg',
    '*.jpg',
    '*.png',
    '*.JPEG',
    '*.JPG',
    '*.PNG',
    #'*.*'
    ],
    ignore=['_IGNORE'],
    noisy=True,
) 

if False:
    so(opjD('all_image_files'),a)

d = {}
sizes = []
timer = Timer(10)
ctr = 0
for b in a: 
    if not os.path.exists(b):
        continue
    s = os.path.getsize(b)
    sizes.append(s)
    f = fname(b)
    n = d2n(f,'->',s)
    if n not in d: 
        d[n] = dict(ctr=1,path=b,size=s) 
    else: 
        d[n]['ctr'] += 1
    ctr += 1
    if timer.rcheck():
        print(ctr)




if False:
    for b in a: 
        if not os.path.exists(b):
            continue
        s = os.path.getsize(b)
        f = fname(b)
        n = d2n(f,'->',s)
        if n == '5.png->84515':
            clf()
            spause()
            img = zimread(b)
            mi(img,img_title=d2s(b))
            spause()
            #raw_enter()




if False:
    so( d, opjD(d2p('unique_images') ) )

sizes = []
for k in d:
    sizes.append(d[k]['size']/10**6)
figure(10); hist(sizes,bins=5000)

ctr = 0
c2 = 0
for n in d:
    if d[n]['ctr'] > 1:
        c2 += d[n]['ctr']
        ctr += 1
        print(d2n(ctr,')'),n,d[n]['ctr']) 
print(len(d),c2)


def num_bins_with_n_percent_signal(q):
    p=plt.hist(q,bins=256)[0]
    t = p.sum()
    s = np.sort(p)
    c = 0
    for i in rlen(s):
        y = -1-i
        c += s[y]
        if c > 0.9*t:
            break
    return i

def resize_by_percent( image, percentage ):
    height, width = image.shape[:2]
    new_width = int(width * (percentage / 100))
    new_height = int(height * (percentage / 100))
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image



def thumbnail( img, extent ):
    height, width = img.shape[:2]
    if height > width:
        tmb = img[height//2-width//2:height//2+width//2:,:]
    else:
        tmb = img[:,width//2-height//2:width//2+height//2,:]
    tmb = cv2.resize( tmb, (extent,extent) )
    return tmb


thumb_path = opjD('thumbnails')

for y in d:
    k = d[y]['path']
    #if '_AZ' in k:
    #    print('!!!!!!!!!')
    #    continue
    s = os.path.getsize(k)
    if s > 20000:
        b= zimread(k)
        f = fname(d[y]['path'])
        t = thumbnail(b,128)
        imsave(opj(thumb_path,f),
            cv2.cvtColor(t, cv2.COLOR_BGR2RGB)
            )
        r = resize_to_extent(b,32)
        q=r.flatten()
        figure(2)
        clf()
        nb = num_bins_with_n_percent_signal(q)
        d[y]['nb' ]= nb
        kprint(d[y],title='d')
        print(k)
        if nb > 85:
            hist(q)
            title( nb)
            spause()
            mi(b,0)
            mi(r,1)
            spause() 
            
            raw_enter() 





if 0:
        img = b#cv2.imread(in_img)
        #get size
        height, width, channels = img.shape
        #print (in_img,height, width, channels)
        # Create a black image
        x = height if height > width else width
        y = height if height > width else width
        square= np.zeros((x,y,3), np.uint8)
        #
        #This does the job
        #
        square[int((y-height)/2):int(y-(y-height)/2), int((x-width)/2):int(x-(x-width)/2)] = img
        cv2.imwrite(out_img,square)
        cv2.imshow("original", img)
        cv2.imshow("black square", square)
        cv2.waitKey(0)


if 0:
    for k in d:
        img = zimread( d[k]['path'] )
        mi(img,img_title=d2s(k,d[k]['ctr']))
        spause()
        raw_enter()



