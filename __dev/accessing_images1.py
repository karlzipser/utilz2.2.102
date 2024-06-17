a = find_files(
    #start='/Users/karlzipser/Library/Photos/Libraries/Syndication.photoslibrary',
    #start='Library/Messages 10-5-2023/Attachments',
    opjD(),
    #start='/Users/karlzipser/Pictures/picture_data/pictures/graphics',
    patterns=[
    '*.jpeg',
    '*.jpg',
    '*.png',
    '*.JPEG',
    '*.JPG',
    '*.PNG',
    #'*.*'
    ],
    ignore=[],
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
    #c = os.path.getctime(b)
    c = os.stat(b).st_birthtime
    sizes.append(s)
    f = fname(b)
    n = d2n('t=',c,', s=',s,' ',f)
    if n not in d: 
        d[n] = dict(ctr=1,path=b,size=s,ctime=c)
    else: 
        d[n]['ctr'] += 1
    ctr += 1
    if timer.rcheck():
        print(ctr)




if False:
    so( d, opjD(d2p('unique_images') ) )

if False:
    sizes = []
    for k in d:
        sizes.append(d[k]['size'])
    figure(10); hist(na(sizes)/10**6,bins=5000)

    ctr = 0
    c2 = 0
    for n in d:
        if d[n]['ctr'] > 1:
            c2 += d[n]['ctr']
            ctr += 1
            print(d2n(ctr,')'),n,d[n]['ctr']) 
    print(len(d),c2)


def num_bins_with_n_percent_signal(q):
    #p=plt.hist(q,bins=256)[0]
    p = np.histogram(q,bins=256)[0]
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





ctr = 0
for y in d:
    k = d[y]['path']
    s = os.path.getsize(k)
    ctr += 1
    if s > 20000:
        try:
            b = zimread(k)
            r = resize_to_extent(b,32)
            q = r.flatten()
            nb = num_bins_with_n_percent_signal(q)
            d[y]['nb' ]= nb
            kprint(d[y],title=d2n(int(ctr/len(d)*100),'% ','d[',y,']'))
            if False:#nb > 85:
                hist(q)
                title( nb)
                spause()
                mi(b,0)
                mi(r,1)
                spause() 
                #raw_enter() 
        except KeyboardInterrupt:
            cr('*** KeyboardInterrupt ***')
            sys.exit()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('Exception!')
            print(d2s(exc_type,file_name,exc_tb.tb_lineno))  







def thumbnail( img, extent ):
    height, width = img.shape[:2]
    if height > width:
        tmb = img[height//2-width//2:height//2+width//2:,:]
    else:
        tmb = img[:,width//2-height//2:width//2+height//2,:]
    tmb = cv2.resize( tmb, (extent,extent) )
    return tmb


#thumb_path = opjh('Pictures/picture_data/thumbnails/people/graphics')
#thumb_path = opjh('Pictures/picture_data/thumbnails/graphics')
thumb_path = opjh('Pictures/picture_data/thumbnails/uncategorized')
os.system(d2s('mkdir -p',thumb_path))
ctr = 0
for y in d:
    k = d[y]['path']
    s = os.path.getsize(k)
    ctr += 1
    try:
        if s > 20000:
            b= zimread(k)
            f = fname(d[y]['path'])
            t = thumbnail(b,256)
            print(d2n(int(ctr/len(d)*100),'%'))
            imsave(opj(thumb_path,y),
                cv2.cvtColor(t, cv2.COLOR_BGR2RGB)
                )
            """
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
            """ 
    except KeyboardInterrupt:
        cr('*** KeyboardInterrupt ***')
        sys.exit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Exception!')
        print(d2s(exc_type,file_name,exc_tb.tb_lineno))  




if False:
    
    if 'txt' not in locals():
        txt = ''
    
    txt = text_editor(txt)


if False:
    import subprocess
    import time

    # Specify the file path you want to open in TextEdit
    file_path = opjD('temp.txt')

    # Open the file in TextEdit
    subprocess.Popen(['open', '-a', 'TextEdit', file_path])

    # Wait for TextEdit to open and for you to make changes
    time.sleep(5)  # Adjust the sleep time as needed

    # Read the text from the TextEdit file
    with open(file_path, 'r') as file:
        file_contents = file.read()

    print(file_contents)


if False:
    for y in d:
        if 'nb' not in d[y] or d[y]['nb'] < 96:
            os.system(d2s('mv',qtd(opj(thumb_path,'uncategorized',y)),qtd(opj(thumb_path,'graphics'))))


#tumbnail_src_path = opj(thumb_path,'people/myhan')
tumbnail_src_path = opj(thumb_path)#,'people/az')
raw_enter(tumbnail_src_path)

t = find_files(
    tumbnail_src_path,
    patterns=[
    '*.jpeg',
    '*.jpg',
    '*.png',
    '*.JPEG',
    '*.JPG',
    '*.PNG',
    ],
    ignore=[],
    noisy=True,
)

print_ = True
action_ = True
ctr = 0
for o in t:
    o = o.replace('thumbnails','pictures')
    p = d[fname(o)]['path']
    if not os.path.exists(pname(o)):
        os_system(d2s('mkdir -p',qtd(pname(o))),e=print_,a=action_)
    if not os.path.exists(o):
        os_system(d2s('mv',qtd(p),qtd(opj(pname(o),fname(o)))),e=print_,a=action_)
        print(o)
    ctr += 1
    print(d2n(int(ctr/len(t)*100),'%'))



def dragged_osx_files_to_list_of_paths():
    u = input('Drag files here: ')
    u = u.replace('\\ ','~')
    u = u.replace(' ','\n')
    u = u.replace('\\','')
    u = u.replace('~',' ')
    v = u.split('\n')
    v = remove_empty(v)
    kprint(v)
    return v

if False:
    paths = dragged_osx_files_to_list_of_paths()
    for p in paths:
        img = zimread(p)
        mi(img)
        spause()
        raw_enter()


if False:
q = dict(
        rating=0,
        str='a',
    )
#EOF
