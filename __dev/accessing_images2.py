
def num_bins_with_n_percent_signal(q):
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


def thumbnail( img, extent ):
    height, width = img.shape[:2]
    if height > width:
        tmb = img[height//2-width//2:height//2+width//2:,:]
    else:
        tmb = img[:,width//2-height//2:width//2+height//2,:]
    tmb = cv2.resize( tmb, (extent,extent) )
    return tmb


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


def make_d_dict(start):
    a = find_files(
        start=start,
        patterns=[
        '*.jpeg',
        '*.jpg',
        '*.png',
        '*.JPEG',
        '*.JPG',
        '*.PNG',
        ],
        ignore=['_IGNORE'],
        noisy=True,
    ) 
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
    return d

def make_thumbnails( d, thumb_path ):
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
        except KeyboardInterrupt:
            cr('*** KeyboardInterrupt ***')
            sys.exit()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('Exception!')
            print(d2s(exc_type,file_name,exc_tb.tb_lineno))  


def strip_t_and_s_from_filename( f ):
    if ('t=' not in f) or ('s=' not in f):
        print('*** strip_t_and_s_from_filename unchanged:',f)
        return f
    return ' '.join(f.split(' ')[2:])

def split_filename( f ):
    if ('t=' not in f) or ('s=' not in f):
        print('*** strip_t_and_s_from_filename unchanged:',f)
        return f
    l = f.split(' ')
    t = float(l[0].replace(',','').split('=')[1])
    s = int(l[1].replace(',','').split('=')[1])
    return t,s,' '.join(l[2:])

def move_graphics( d, src_path, dst_path, graphics_threshold=90 ):
    os_system('mkdir -p',qtd(dst_path))
    for y in d: 
        if 'nb' not in d[y] or d[y]['nb'] < graphics_threshold:
            os_system(
                'mv',
                qtd(opj(src_path,y)),
                qtd(opj(dst_path,y)))


#######################################################
#
#start='/Users/karlzipser/Library/Photos/Libraries/Syndication.photoslibrary',
#start='Library/Messages/Attachments',
start=opjh('Library/Messages/Attachments')
#start = opjD()
#start='/Users/karlzipser/Pictures/picture_data/pictures/graphics',

#thumb_path = opjh('Pictures/picture_data/thumbnails/people/graphics')
#thumb_path = opjh('Pictures/picture_data/thumbnails/graphics')
thumb_path = opjh('Pictures/picture_data/thumbnails/uncategorized')

d = make_d_dict( start )

make_thumbnails( d, thumb_path )

move_graphics(
    d,
    thumb_path,
    thumb_path.replace('uncategorized','graphics'),
    90,
)
#
#######################################################



#thumbnail_src_path = opj(thumb_path,'people/myhan')
#thumbnail_src_path = opj(thumb_path)#,'people/az')
thumbnail_src_path = opjh('Pictures/picture_data/thumbnails/delete')

raw_enter(thumbnail_src_path)

t = find_files(
    thumbnail_src_path,
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

picture_action = 'cp'
print_ = True
action_ = True
ctr = 0
for o in t:
    o = o.replace('thumbnails','pictures')
    p = d[fname(o)]['path']
    if not os.path.exists(pname(o)):
        os_system(d2s('mkdir -p',qtd(pname(o))),e=print_,a=action_)
    if not os.path.exists(o):
        os_system(
            picture_action,
            qtd(p),
            qtd(opj(pname(o),fname(o))),
            e=print_,a=action_
        )
        print(o)
    ctr += 1
    print(d2n(int(ctr/len(t)*100),'%'))





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
