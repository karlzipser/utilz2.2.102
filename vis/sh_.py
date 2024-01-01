from utilz2.misc import *
from utilz2.vis.compose import *
from utilz2.core import *
from utilz2.core.u2b_arrays import *
import matplotlib
import matplotlib.pyplot as plt  # the Python plotting package
from utilz2.vis.matplotlib_ import *
from utilz2.vis.cv2_ import *
from utilz2.vis.cv2_ import *

def kws2dict(*args,**kwargs):
    if args:
        assert len(args)==1
        default_dic=args[0]
        for k in kwargs:
            if k not in default_dic:
                print('Warning, received unexpected keyword',k,'ignoring it.')
        for k in default_dic:
            if k in kwargs:
                if type(default_dic[k]) is not type(kwargs[k]):
                    print(
                        'Warning, type',
                        type_name_from_object(kwargs[k]),
                        'of',
                        qtds(k),
                        'is inconsistent with type',
                        type_name_from_object(default_dic[k]),
                        'of its default value',
                        default_dic[k],
                    )
                default_dic[k]=kwargs[k]
    else:
        default_dic=kwargs
    return default_dic


def classkws2dict(self,defaults,**kwargs):
    __=kws2dict(defaults,**kwargs)
    for k in __:
        self.__dict__[k]=__[k]


def kws2class(*args,**kwargs):
    default_dic=kws2dict(*args,**kwargs)
    class a:
        def __init__(_):
            pass
        def keys(_):
            return _.__dict__.keys()
        def get(_,k):
            return _.__dict__[k]
        def set(_,k,val):
            _.__dict__[k]=val
        def dic(_):
            return _.__dict__
        def print(_):
            kprint(_.__dict__)
    b=a()
    #kprint(default_dic,title='dd')
    for k in default_dic:
        setattr(b,k,default_dic[k])
    return b


try:
    r = txt_file_to_list_of_strings(opjh('.screen_resolution'))
    SCREEN_RESOLUTION = (int(r[0]),int(r[1]))
except:
    #clp("Didn't find or get data from",opjh('.screen_resolution'),'`wrb')
    try:
    #if using_osx:
        def screen_size():
            from Quartz import CGDisplayBounds
            from Quartz import CGMainDisplayID
            mainMonitor = CGDisplayBounds(CGMainDisplayID())
            return (mainMonitor.size.width, mainMonitor.size.height) 
        SCREEN_RESOLUTION = screen_size()
        print('should SCREEN_RESOLUTION be saved?')
    #else:
    except:
        SCREEN_RESOLUTION = (800,800)


def resize_to_extent(
    img,
    extent,
    fill=128,
    interpolation=cv2.INTER_AREA,
    e=0,
):
    if extent != max(shape(img[:2])) and extent != min(shape(img[:2])):
        q = extent / max(shape(img)[:2])
        new_img = get_blank_rgb(extent,extent) + fill
        #scale_percent = 60 # percent of original size
        width = int(img.shape[1] * q)
        height = int(img.shape[0] * q)
        dim = (width, height)
        r = cv2.resize(img, dim, interpolation=interpolation)
        if len(shape(img)) ==2:
            new_img = new_img[:,:,0]
            new_img[extent//2-height//2:extent//2-height//2+height,extent//2-width//2:extent//2-width//2+width] = r
        else:
            new_img[extent//2-height//2:extent//2-height//2+height,extent//2-width//2:extent//2-width//2+width,:] = r
        return new_img
    else:
        if e: print('resize_to_extent(): no resizing')
        return img


def png4ch_2_3ch( img ):
    assert shape(img)[2] == 4
    mask = 1*img[:,:,3]
    a = mask_it(img[:,:,:3],mask)
    red = 0*a
    red[:,:,0] = 255
    b = mask_it(red,255-mask)
    return a+b


def img_2_rgb_img( img ):
    new_imgs = []
    if len(shape(img)) == 2:
        img = 1.0 * img
    if type(img[0,0]) is not u8:
        if img.max() <= 1.0 and img.min() >= 0.0:
            img = 255*img
        else:
            img = 255*z2o(img)
        img = img.astype(u8)
    if len(shape(img)) == 2:
        new_img = get_blank_rgb(shape(img)[0],shape(img)[1])
        for i in range(3):
            new_img[:,:,i] = img
    else:
        if shape(img)[2] == 4:
            new_img = png4ch_2_3ch(img)
            #assert( img.max() == 255 and img.min() == 0 )
            #assert( type(img[0,0,0]) == u8 )
            #a = img[:,:,3]
            #new_img = img[:,:,:3]
            #new_img[a==0]=128
        else:
            new_img = img

    return new_img


def fix_up_image_list( imgs, maxsize=0 ):
    e =  0
    new_imgs = []
    if maxsize:
        e = maxsize
    else:
        for img in imgs:
            s = shape(img)
            w,h = s[0],s[1]
            e = max(w,h,e)

    for img in imgs:
        new_imgs.append( resize_to_extent( img_2_rgb_img( img ), e ) )
    return new_imgs


#https://stackoverflow.com/questions/60674501/how-to-make-black-background-in-cv2-puttext-with-python-opencv
def draw_text(
    img,
    text,
  pos=(0, 0),
  font=cv2.FONT_HERSHEY_PLAIN,
  font_scale=3,
  font_thickness=1,
  text_color=(0, 255, 0),
  text_color_bg=(0, 0, 0)
):
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
    if len(shape(img)) == 3 and shape(img)[2] == 4:
        img[x:x+text_h,y:y+text_w,3] = 255
    cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)

    return text_size



def sh(
    inpt,
    fignum = 1,
    title = '',
    cv=False,
    maxsize=0,
    cmap = 'gray',
    toolBar = True,
    do_clf = True,
    use_spause = True,
    do_axis = False,
    padsize=10,
    padval=127,
    use_dict_keys_as_titles=True,
    titles_font_scale=5,
    maxnumfiles=36,
    evenlyspacefiles=True,
    includefirstandlast=True,
    fileindicies=[],
    randomize=False,
    figsize=None,
    display_key_replacements={},
    sequential=False,
    crop=(0,0,0,0),
    r=0,
    a=1,
    e=1,
    t=0,
    include_shape_in_title=True,
 ):
    assert type(fignum) in [int,str]
    assert type(title) == str
    assert type(cv) == type(True)
    assert type(maxsize) == int
    assert type(cmap) == str

    if not a:
        return None

    def ___e():
        if e:
            try:
                q=shape(inpt)
            except:
                q='<shape of inpt not available>'
            s=d2s('...preparing',q,'fig:',fignum,'title',title)
            printr(s)
    ___e()

    if type(inpt) == str:
        if os.path.isdir(inpt):
            l=load_img_folder_to_dict(
                inpt,
                maxnumfiles=maxnumfiles,
                evenlyspacefiles=evenlyspacefiles,
                randomize=randomize,
                includefirstandlast=includefirstandlast,
                fileindicies=fileindicies,
                e=e,
            )
        elif os.path.isfile(inpt):
            cg(1)
            if exname(inpt) in IMAGE_EXTENSIONS:
                cg(2)
                l = [rimread(inpt)]
            else:
                cg(3)
                assert(False)
        else:
            assert(False)
        if not l:
            return None
        return sh(
            l,
            fignum = fignum,
            title = title,
            cv=cv,
            maxsize=maxsize,
            cmap = cmap,
            toolBar = toolBar,
            do_clf = do_clf,
            use_spause = use_spause,
            do_axis = do_axis,
            padsize=padsize,
            padval=padval,
            r=r,
            a=a,
            e=e,
            figsize=figsize,
            sequential=sequential,
            crop=crop,
            t=t,
            include_shape_in_title=include_shape_in_title,
            titles_font_scale=titles_font_scale,
            display_key_replacements=display_key_replacements,
        )


    if type(inpt) == dict:
        l = []
        for k in inpt:
            u = shape(inpt[k])[0]
            q = 1*inpt[k]
            if q.max() == 1:
                q *= 255

            if iwidth(q) != iheight(q):
                cE('*** Warning, sh requres square images, embedding as square. ***',e=e)
                q=resize_to_extent(q,max(iwidth(q),iheight(q)))
            if use_dict_keys_as_titles:
                if False:#display_key_replacements:
                    for kk in display_key_replacements:
                        k=k.replace(kk,display_key_replacements[kk])
                draw_text(q, k,
                          pos=(0, 0),
                          font=cv2.FONT_HERSHEY_PLAIN,
                          font_scale=titles_font_scale,
                          font_thickness=2,
                          text_color=(255,255,255),
                          text_color_bg=(16,16,16),
                        )
            l.append(q)
        return sh(
            l,
            fignum = fignum,
            title = title,
            cv=cv,
            maxsize=maxsize,
            cmap = cmap,
            toolBar = toolBar,
            do_clf = do_clf,
            use_spause = use_spause,
            do_axis = do_axis,
            padsize=padsize,
            padval=padval,
            r=r,
            a=a,
            e=e,
            figsize=figsize,
            sequential=sequential,
            crop=crop,
            t=t,
            include_shape_in_title=include_shape_in_title,
            display_key_replacements=display_key_replacements,
        )
        return inpt

    elif type(inpt) == list:
        if not title:
            title = 'multi-image plot'
        if maxsize:
            n = int(np.sqrt(len(inpt)))
            if np.sqrt(len(inpt)) > n:
                n += 1
            maxsize = maxsize // n
        if sequential:
            for img in inpt:
                sh(img,r=1)
            return inpt
        else:
            f = fix_up_image_list( inpt, maxsize )
            v = vis_square2( f, padsize=padsize, padval=padval )
            #v = get_image_row( f )
            #print( shape( v ), maxsize )
            return sh(
                v,
                fignum = fignum,
                title = title,
                cv=cv,
                maxsize=maxsize,
                cmap = cmap,
                toolBar = toolBar,
                do_clf = do_clf,
                use_spause = use_spause,
                do_axis = do_axis,
                r=r,
                a=a,
                e=e,
                figsize=figsize,
                sequential=sequential,
                crop=crop,
                t=t,
                include_shape_in_title=include_shape_in_title,
                display_key_replacements=display_key_replacements,
            )
            #sh( fix_up_image_list( vis_square2( inpt ) ) , padsize=4, padval=0.5 ) ) )
    
    if np.array(crop).max()>0:
        x0,x1,y0,y1=crop
        print(x0,y0,x1,y1)
        if len(shape(inpt))==2:
            inpt=inpt[y0:y1,x0:x1]
        else:
            inpt=inpt[y0:y1,x0:x1,:]
    if title or include_shape_in_title:
        if include_shape_in_title:
            title=d2s(title,shape(inpt))
    if cv:
        mci( inpt, title=d2s('fig.', fignum, title ))
        if r == 1:
            cm(r=1)
        return

    if toolBar == False:
        plt.rcParams['toolbar'] = 'None'
    else:
        plt.rcParams['toolbar'] = 'toolbar2'

    if not isNone(figsize):
        if figsize==0:
            figsize=int(np.sqrt(iwidth(inpt)/10))
            cm('*** auto figsize =',figsize,e=e)
        _figsize=(figsize,figsize)
    else:
        _figsize=(5,5)
    f = plt.figure(fignum,figsize=_figsize)
    if do_clf:
        plt.clf()

    imgplot = plt.imshow(inpt, cmap)
    imgplot.set_interpolation('nearest')
    #if not isNone(figsize):

    if not do_axis:
        """
        plt.xticks([])
        plt.yticks([])
        plt.spines['top'].set_visible(False)
        plt.spines['right'].set_visible(False)
        plt.spines['bottom'].set_visible(False)
        plt.spines['left'].set_visible(False)
        """
        plt.axis('off')

    plt.title(title)
    if use_spause:
        spause()
    if e:
        print('showing',shape(inpt),'fig:',fignum,'title',title)
    if r:
        cm(r=1)
    if t:
        time.sleep(t)

def shc( *args, **kwargs ):
    kwargs['cv'] = True
    sh( *args, **kwargs )
def shm( *args, **kwargs ):
    kwargs['maxsize'] = SCREEN_RESOLUTION[1]
    sh( *args, **kwargs )
def shcm( *args, **kwargs ):
    kwargs['cv'] = True
    kwargs['maxsize'] = SCREEN_RESOLUTION[1]
    sh( *args, **kwargs )



def load_img_folder_to_dict(
    img_folder,
    maxnumfiles=36,
    randomize=False,
    evenlyspacefiles=True,
    includefirstandlast=True,
    fileindicies=[],
    e=True,
    ):
    img_fns = sggo(img_folder,'*.*')
    if not img_fns:
        cE('Warning, folder',qtd(img_folder),'is empty.')
        return None
    if e: print('Loading from',img_folder)
    if randomize:
        np.random.shuffle(img_fns0)
        if e: print('\tRandomizing img file order.')
    len_imgs=len(img_fns)
    l=[]
    print(fileindicies)
    if fileindicies:
        for i in fileindicies:
            l.append(img_fns[i])
            kprint(l,title='indicies')
    else:
        if maxnumfiles:
            if evenlyspacefiles:
                n=max(1,len(img_fns)//maxnumfiles)
                mx=len(img_fns)
            else:
                n=1
                mx=maxnumfiles
            
            for i in range(0,mx,n):
                l.append(img_fns[i])
            if len(l)>maxnumfiles:
                l=l[:maxnumfiles]
        if includefirstandlast:
            if img_fns[0] not in l:
                l=[img_fns[0]]+l
            if img_fns[-1] not in l:
                l.append(img_fns[-1])
    if not len(l):
        l=img_fns
    imgs = {}
    for f in l:
        if f.split('.')[-1] in IMAGE_EXTENSIONS:
            f2 = f
            while True:
                if f2 in imgs:
                    f2 += '+'
                    cr(__file__,f2)
                else:
                    break
            imgs[fname(f2)] = rimread(f)
    if e:
        kprint(img_fns,title='Existing images')
        kprint(l,title='Loaded images')
        print('\tFinished loading',len(imgs),'images from',len_imgs, 'in',img_folder+'.')
    return imgs




def load_img_folder_to_list(img_folder,**kwargs):
    return dict_to_sorted_list(load_img_folder_to_dict(qtd(img_folder),**kwargs))


















#from utilz2 import *
import argparse


def imgsum(g):
    assert isimg(g)
    s=sum(g.flatten())
    if not is1ch(g):
        s/=3.
    if g.max()==255:
        s/=255.
    return intr(s)


def getparser( **argdic ):
    parser = argparse.ArgumentParser(description='Argument Parser')
    for k in argdic:
        if len(k)>1:
            s='--'
        else:
            s='-'
        parser.add_argument(s+k,type=type(argdic[k]),default=argdic[k])
    return parser.parse_args()

    
def isimg(g,e=0):
    c=cg
    c('isimg(',shape(g),')',e=e)
    if isNone(g):
        c('a',e=e)
        return False
    if not type(g) is type(na([0])):
        c('b',e=e)
        return False
    if not nchannels(g)>=1 and nchannels(g)<=4:
        c('c',e=e)
        return False
    if nchannels(g)>2:
        if type(g[0,0,0]) is u8:
            c('d',e=e)
            return True
        else:
            c('e',e=e)
            return False
    if type(g[0,0]) is not u8:
        if g.min()>=0 and g.max()<=1:
            c('f',e=e)
            return True
        else:
            c('g',e=e)
            return False
    else:
        if g.min()>=0 and g.max()<=255:
            c('f',e=e)
            return True
        else:
            c('g',e=e)
            return False
    c('h',e=e)
    return False


def png2rgba(g):
    assert isimg(g)
    assert len(shape(g))==3
    r=g[:,:,:3]
    if shape(g)[2]==4:
        a=g[:,:,3]
    else:
        a=255+0*g[:,:,0]
    return dic2tup(rgb=r,alpha=a)


def rgba2png(rgb,alpha):
    assert isimg(rgb)
    assert len(shape(rgb))==3
    if len(shape(alpha))==3:
        alpha=alpha[:,:,0]
    png=zeros((iwidth(rgb),iheight(rgb),4),u8)
    png[:,:,:3]=rgb
    png[:,:,3]=alpha
    return png


def nchannels(g):
    if len(shape(g))==2:
        return 1
    else:
        return shape(g)[2]


def is1ch(g):
    return nchannels(g)==1


def histimg(g,n=100):
    assert isimg(g)
    clf()
    if not is1ch(g):
        rr=g[:,:,0].flatten()
        gg=g[:,:,1].flatten()
        bb=g[:,:,2].flatten()
        plt.hist(rr, histtype='stepfilled', alpha=0.3, color=(1,0,0),bins=n)
        plt.hist(gg, histtype='stepfilled', alpha=0.3, color=(0,1,0),bins=n)
        plt.hist(bb, histtype='stepfilled', alpha=0.3, color=(0,0,1),bins=n)
    else:
        plt.hist(g.flatten(), histtype='stepfilled', color=(0.5,0.5,0.5),bins=n)
    plt.title(d2n('histimg(',shape(g),',n=',n,')'))




def fx(m):
    assert isimg(m)
    return cv2.cvtColor(m, cv2.COLOR_BGR2RGB)



def rimread(f,e=False,show=False):
    g = cv2.imread(f,cv2.IMREAD_UNCHANGED)
    assert isimg(g)
    if not is1ch(g):
        g[:,:,:3]=fx(g)
    assert isimg(g)
    if e: print('\trimread read',f,'with shape',shape(g))
    if show:
        shc([g])
        if type(show) is float:
            time.sleep(show)
    return g


def rimsave(f,g,e=False,show=False):
    assert isimg(g)
    if not is1ch(g):
        g=fx(g[:,:,:3])
    imsave(f,fx(g))
    if e: print('\trimsave saved',f,'with shape',shape(g))
    if show:
        shc(g,title=d2s('rimsave:',f))
        if type(show) is float:
            time.sleep(show)


def ope(f):
    return os.path.exists(f)



def _fnames_to_name_path_dict(fs):
    d={}
    for f in fs:
        d[fnamene(f)]=f
    return d



def dir_a_names_is_subset_of_dir_b_names(a,b):
    aa=_fnames_to_name_path_dict(sggo(a,'*'))
    bb=_fnames_to_name_path_dict(sggo(b,'*'))
    for n in aa:
        if n not in bb:
            return False
    return True



def blendab(a,b,s=0.5):
    assert s>=0 and s <=1
    assert isimg(a)
    assert isimg(b)
    assert shape(a) == shape(b)
    c=1.*s*a+(1.-s)*b
    c=c.astype(u8)
    return c


def kernelaltermask(m,n):
    if n<0:    
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (-n,-n))
        return cv2.erode(1*m,kernel)
    elif n>0:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n,n))
        return cv2.dilate(1*m,kernel)
    else:
        return m


def joinmaskm1(a,b):
    return m255(joinmaskm1(a,b))



def joinmaskm255(a,b):
    c=m1(a)+m1(b)
    c[c>1]=1
    return m255(c)


def maskjoin(a,b,m):
    m=m1(m)
    assert isimg(a)
    assert isimg(b)
    assert shape(a) == shape(b)
    a=maskit(a,m)
    b=maskit(b,1-m)
    assert maskit(a,b).max() == 0
    return a+b


def m1(g,e=0):
    """
    get 0 to 1 mask, 1 channel
    """
    sg=shape(g)
    assert isimg(g)
    if nchannels(g) == 1:
        g=z2o(g)
        g[g>=0.5]=1
        g[g<1]=0
    elif nchannels(g)>=3:
        g=m1(g[:,:,-1])
    else:
        assert False
    #cm('m1(',sg,')->',shape(g))
    return g.astype(u8)


def m255(g,e=0):
    """
    get 0 to 255 mask, 3 channels
    """
    x=(255*m1(g)).astype(u8)
    y=get_blank_rgb(iwidth(x),iwidth(x))
    for i in range(3):
        y[:,:,i]=x[:,:]
    return y


def maskit( g, m ):
    assert isimg(g)
    assert isimg(m)
    if nchannels(m)>1:
        m = m[:,:,0]
    return cv2.bitwise_and( g, g, mask=m )




def lumadd(a,b,s=0.5):
    a=1.*a
    b=z2o(cv2.cvtColor(b,cv2.COLOR_RGB2GRAY))*255.
    for i in [0,1,2]:
        a[:,:,i]=a[:,:,i]+s*b
    a[a>255]=255
    return a.astype(u8)


def embedinsquare(g,fill=128):
    assert isimg(g)
    width=max(iwidth(g),iheight(g))
    x=get_blank_rgb(width,width)+fill
    if is1ch(g):
        x=x[:,:,0]
    x[:iheight(g),:iwidth(g)]=g
    return x


#dic2tup=kws2tup


#def tup2dic(t):
#    return t._asdict()

if False:
    def dic2class(**kwargs):
        class a:
            def __init__(_):
                pass
            def keys(_):
                return _.__dict__.keys()
            def get(_,k):
                return _.__dict__[k]
        b=a()
        for k in kwargs:
            setattr(b,k,kwargs[k])
        return b

def fliplr(g,p=1):
    if rndint(100)/100<p:
        return cv2.flip(1*g,1)
    else:
        return g


def flipud(g,p=1):
    if rndint(100)/100<p:
        return cv2.flip(1*g,0)
    else:
        return g

#ga=getattr

#sa=setattr


def iheight(g):
    return shape(g)[0]


def iwidth(g):
    return shape(g)[1]


def extract_square_from_center(g,w):
    #assert isimg(g)
    #assert type(g) is int
    wg=shape(g)[0]
    assert wg==shape(g)[1]
    assert w<=wg
    w2=w//2
    wg2=wg//2
    if len(shape(g))==2:
        return g[wg2-w2:wg2-w2+w,wg2-w2:wg2-w2+w]
    else:
        return g[wg2-w2:wg2-w2+w,wg2-w2:wg2-w2+w]


def extract_or_place_in_center(g,wmin):
    if iwidth(g)>=wmin:
        cg(shape(g),wmin)
        return extract_square_from_center(g,wmin)
    else:
        cb(shape(g),wmin)
        return img2center(g,get_blank_rgb(wmin,wmin),0,0)


def center_img_on_bounding_box(g,xx,yy,width,height):
    def __():
        wg=iwidth(g)
        e=get_blank_rgb(wg*3,wg*3)
        uu=img2center(
            g,
            e,
            wg//2-(xx+width//2),
            wg//2-(yy+height//2),
        )
        return uu
    return __()


def resize_so_mx_size_goes_to_ref_size(g,mx,r):
    qq=int(r/mx*shape(g)[0])
    #cb('qq=',qq)
    return cv2.resize(g,(qq,qq))


def get_bounding_rect_from_object_mask(object_mask):
    cnts = cv2.findContours(1*object_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    assert len(cnts) == 1
    xx,yy,width,height = cv2.boundingRect(cnts[0])
    return xx,yy,width,height


def mask_out_val(g,val):
    m=0*g
    w=1*m[:,:,0]
    x=1*m[:,:,0]
    y=1*m[:,:,0]
    w[g[:,:,0]==val]=1
    x[g[:,:,1]==val]=1
    y[g[:,:,2]==val]=1
    w[g[:,:,0]==0]=1
    x[g[:,:,1]==0]=1
    y[g[:,:,2]==0]=1
    z=w*x*y
    m[z>0]=255
    return dic2class(masked=maskit(g,255-m),mask=m)


def random_circles(width=640,avg_radius=16,num_rows=8,max_num_circles_per_cell=4):
    image = get_blank_rgb(width,width)
    num_cols = num_rows
    cell_size_x = width // num_cols
    cell_size_y = width // num_rows

    for row in range(num_rows):
        for col in range(num_cols):
            for _ in range(randint(0,max_num_circles_per_cell+1)):
                radius = np.random.randint(avg_radius//2,avg_radius)#int(avg_radius*0.75,int(avg_radius*1.25)))
                x1,x2 = max(4,col * cell_size_x + radius), max(6,(col + 1) * cell_size_x - radius)
                y1,y2 = max(4,row * cell_size_y + radius), max(6,(row + 1) * cell_size_y - radius)
                if x1<x2:
                    x = (x1,x2+2)
                else:
                    x = (x2,x1+1)
                if y1<y2:
                    y = (y1,y2+2)
                else:
                    y = (y2,y1+1)

                center_x = np.random.randint(*x)
                center_y = np.random.randint(*y)
                color = (255,255,255)
                cv2.circle(image, (center_x, center_y), radius, color, -1)
    return image



def color_balance( content, reference ):
    import colortrans
    import numpy as np
    from PIL import Image

    output_lhm = colortrans.transfer_lhm(content, reference)
    output_pccm = colortrans.transfer_pccm(content, reference)
    output_reinhard = colortrans.transfer_reinhard(content, reference)
    return output_lhm, output_pccm, output_reinhard

def colorbal(g,ref,s=0.5):
    output_lhm,output_pccm,output_reinhard=color_balance(g,ref)
    return (s*g+(1-s)*output_reinhard).astype(u8)



if False:#__name__ == '__main__':
    CA()
    c=samimgs()
    sh(c.sunny,1)
    print(isimg(c.sunny))
    sh(blendab(c.sunny,fliplr(c.sunny)),2)
    for k in c.keys():
        shc(c.get(k),k)






def difference(a,b):
    return set(a).difference(set(b))


def logkeys(lcs):
    ks = list(lcs.keys())
    l=[]
    for k in ks:
        if k[0]!='_':
            l.append(k)
    return l

def saveses(l0,l1,lcs):
    d={}
    for k in difference(l1,l0):
        d[k]=lcs[k]
        cm(k)
    return d













def fs2dic(
    path=opjD(),
    last=True,
    max=10,
    indicies=[],
    e=True,
    d=False,
    test=False,
    ):
    def _test():
        l=fs2dic(opjh('sampleimages'),e=e,d=0)
        cm(r=1)
        l=fs2dic(opjh('sampleimages'),e=e,d=1)
    if test:
        _test()
        return
    if os.path.isfile(path):
        fs=[fs]
    else:
        fs=fifs(
                start=path,
                d=d,
                e=e,
            )
    if not fs:
        cE('Warning, folder',qtd(path),'is empty.')
        return None
    if e: print('Loading from',path)
    sfs=sfl(l=fs,last=last,max=max,indicies=indicies,test=test)
    imgs = {}
    for f in sfs:
        imgs[f] = rimread(f)
    if e:
        kprint(fs,title='Existing images')
        kprint(sfs,title='Loaded images')
        print('\tFinished loading',len(imgs),'images from',len(fs), 'in',path+'.')
    return imgs









import scipy

def img2tri( img, dx=0, dy=0 ):
    width = shape(img)[0]
    if len(shape(img)) > 2:
        triple_space = zeros( ( 3*width, 3*width, shape(img)[2] ), np.uint8 )
        triple_space[width+dy:2*width+dy,width+dx:2*width+dx,:] = img
    else:
        triple_space = zeros( ( 3*width, 3*width ), np.uint8 )
        triple_space[width+dy:2*width+dy,width+dx:2*width+dx ] = img        
    return triple_space

def tri2img( triple_space ):
    width = shape( triple_space )[0]//3
    if len(shape(triple_space)) > 2:
        img = triple_space[width:2*width,width:2*width,:]
    else:
        img = triple_space[width:2*width,width:2*width]
    return img

def img2center( img1, img2, dx=0, dy=0 ):
    #cm(shape(img1),shape(img2))
    w1 = shape(img1)[0]
    w2 = shape(img2)[0]
    if np.abs(w2//2-w1//2) < np.abs(dx):
        dx = np.sign(dx) * np.abs(w2//2-w1//2-2)
        #cr('dx =',dx)
    if np.abs(w2//2-w1//2) < np.abs(dy):
        dy = np.sign(dy) * np.abs(w2//2-w1//2-2)
        #cr('dy =',dy)
    assert( w1 <= w2 )
    if len(shape(img1)) > 2:
        #cy(shape(img2[ w2//2-w1//2+dy:w2//2-w1//2+w1+dy, w2//2-w1//2+dx:w2//2-w1//2+w1+dx, : ]))
        #cg(shape(img1))
        img2[ w2//2-w1//2+dy:w2//2-w1//2+w1+dy, w2//2-w1//2+dx:w2//2-w1//2+w1+dx, : ] = img1
    else:
        img2[ w2//2-w1//2+dy:w2//2-w1//2+w1+dy, w2//2-w1//2+dx:w2//2-w1//2+w1+dx ] = img1
    return img2

def transform_img_and_return_in_dst_img( img, dst_img, dx, dy, scaling_factor, rotation_degrees,  ):
    assert( scaling_factor <= 1.0 )
    width = shape(img)[0]
    s = int( width * scaling_factor )
    img = cv2.resize( img, (s,s) )
    img = scipy.ndimage.rotate( img, rotation_degrees, reshape=False )
    assert( shape(dst_img)[0] >= width )
    dst_img = img2center( img, 0*dst_img, dx, dy )
    return dst_img








if False:#__name__ == '__main__':

    a=rndn(100,100,4)
    a=z2o(a)
    a[:,:,3]=0
    a[:50,:,3]=1
    a = (255.*a).astype(u8)
    b=rndn(40,20,3);b=z2o(b)
    c=rndn(10,10)
    d=1*b#; d[:,:,3]=0;d[:,:50,3]=255
    l=[a,b,c,a]
    sh(l)
    raw_enter()
    shc(l)
    raw_enter()

#EOF