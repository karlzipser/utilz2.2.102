#from utilz2 import *
from utilz2.core.files.u9_files import *


os.environ['GLOG_minloglevel'] = '2'

def sgg(d,r=0):
    return sorted(gg(d,recursive=r),key=natural_keys)

def sggo(d,*args,r=0):
    a = opj(d,*args)
    return sgg(a,r=r)

def sorted_by_cmtime(list_of_files):#,c=True):
    Mtimes = {}
    #if c:
    #    fn = os.path.getctime
    #else:
    #    fn = os.path.getmtime
    for f in list_of_files:
        Mtimes[f] = min(os.path.getctime(f),os.path.getmtime(f))
    lst0 = sorted(Mtimes.items(), key=lambda x:x[1])
    lst1 = []
    for l in lst0:
        lst1.append(l[0])
    return lst1

def get_files_sorted_by_mtime(path_specification):
    files = sggo(path_specification)
    Mtimes = {}
    for f in files:
        Mtimes[f] = os.path.getmtime(f)
    return sorted(Mtimes.items(), key=lambda x:x[1])

def tsggo(d,*args):
    a = opj(d,*args)
    #CS_(a)
    return get_files_sorted_by_mtime(a)


def most_recent_file_in_folder(
    path,str_elements=[],
    ignore_str_elements=[],
    return_age_in_seconds=False
):
    files = gg(opj(path,'*'))
    if len(files) == 0:
        return None
    candidates = []
    for f in files:
        fn = fname(f)
        is_candidate = True
        for s in str_elements:
            if s not in fn:
                is_candidate = False
                break
        for s in ignore_str_elements:
            if s in fn:
                is_candidate = False
                break
        if is_candidate:
            candidates.append(f)
    mtimes = {}
    if len(candidates) == 0:
        return None
    for c in candidates:
        mtimes[os.path.getmtime(c)] = c
    mt = sorted(mtimes.keys())[-1]
    c = mtimes[mt]
    if return_age_in_seconds:
        return c,time.time()-mt
    else:
        return c




IMAGE_EXTENSIONS = ['jpg','jpeg','JPG','JPEG','png','PNG','tif','tiff','TIF','TIFF']
IMAGE_PATTERNS = []
for k in IMAGE_EXTENSIONS:
    IMAGE_PATTERNS.append('*.'+k)


def files_to_dict(
    path,
    ignore_underscore=True,
    require_extension=[],
    ignore_extension=['pyc'],
    ignore=[],
    save_stats=False,
    list_symbol='*',
    process_symbol=True,
):
    D = {list_symbol : []}
    fs = sggo(path,'*')
    timer = Timer(0.01)
    for f in fs:
        if timer.check():
            timer.reset()
            #print(time.time())
            print(rndchoice(['/','\\']),end='\r',flush=True)
        if fname(f)[0] == '_' and ignore_underscore:
            continue
        do_continue = False
        for ig in ignore:
            if ig in f:
                do_continue = True
                break
        if do_continue:
            continue
        if not os.path.isdir(f):
            if save_stats:
                f_ = {
                    f:{
                        'mtime':os.path.getctime(f),
                        #'ctime':os.path.getctime(f),
                        'size':os.path.getsize(f),
                    }
                }
            else:
                f_ = f
            if not require_extension or exname(f) in require_extension:
                if not ignore_extension or exname(f) not in ignore_extension:
                    D[list_symbol].append(f_)
        else:
            D[fname(f)] =\
             files_to_dict(
                path=f,
                ignore_underscore=ignore_underscore,
                require_extension=require_extension,
                ignore=ignore,
                save_stats=save_stats,
                )
    return D
    
    


def files_to_list(path,**K):
    return all_values(files_to_dict(path,**K))



def find_list_of_files_recursively(path,pattern,verbose=True,ignore=[]):
    F = find_files_recursively(path,pattern,FILES_ONLY=True,verbose=verbose)
    l = []
    if 'o' not in locals():
        o = []
    for p in F['paths']:
        continue_ = False
        for i in ignore:
            #print('ignore =',i,'p =',p)
            #cy('ignore =',i,'p =',p)
            if i in p:
                continue_ = True
                break
        if continue_:
            #cr('ignoring',p)
            continue
        for f in F['paths'][p]:
            #if verbose:
            #    clp(p,'`r--',f,'`g--')        
            assert (p,f) not in l
            g = opj(F['src'],p,f)
            #g = opj(p,f)
            #g = g.encode('unicode_escape')
            #print('***',g,os.path.exists(g))
            l.append((p,f))
            assert os.path.exists(g)
            o.append(g)
    return o




def find_files(
    start=opjD(),
    patterns=["*"],
    ignore=['Photos Library','Photo Booth','Library'],
    file_list=[],
    __top=True,
    recursive=True,
    timer=Timer(1),
    noisy=True,
    minagedays=0,
    maxagedays=0,
):
    #if noisy and ignore:
    #    print('Ignorning files in',', '.join(ignore)+'.')
    if timer.rcheck() and noisy:
        print('find_files found',commas(len(file_list)),'files')
    if __top:
        file_list = []
    if type(patterns) == str:
        patterns = [patterns]
    for pattern in patterns:
        #print('start:',start,'len(file_list):',len(file_list))
        _fs= sggo(start,pattern)

        for f in _fs:
            #print(f)
            if os.path.isfile(f):
                file_list.append(f)

    a = sggo(start,'*')
    if not a and noisy:
        print('*** Warning, no files found with start',qtd(start),'and patterns',patterns,'***')

    if recursive:
        ds = []
        for b in a:
            if os.path.isdir(b):
                _ignore = False
                for ig in ignore:
                    if ig in b:
                        _ignore = True
                        break
                if not _ignore:
                    ds.append(b)
                else:
                    print('ignoring',b)

        for d in ds:
            find_files(
                start=d,patterns=patterns,ignore=ignore,file_list=file_list,__top=False,
                recursive=True,timer=timer,noisy=noisy)
    if (__top or timer.rcheck()) and noisy:
        print('find_files found',len(file_list),'files. done.')
    if __top:
        daysfilelist=[]
        now=time.time()
        for f in file_list:
            if minagedays:
                if now-os.path.getmtime(f)>minagedays*24*60*60:
                    if noisy:
                        print('\tSkipping',f,'too old')
                    continue
            if maxagedays:
                if now-os.path.getmtime(f)<maxagedays*24*60*60:
                    if noisy:
                        print('\tSkipping',f,'too new.')
                    continue
            daysfilelist.append(f)
        return sorted(list(set(daysfilelist)),key=natural_keys)



def ff(
    start=opjD(),
    pattern='*.*',
    d=True,
    e=True,
    test=False,
    ignore=[],
):
    """
    ff find-file wrapper
    """
    cg('Recursive mode on',e=d)
    def _test():
        fs=ff(start,pattern,d=0)
        kprint(fs,d2n('start=',start,' pattern=',pattern))
        cg('Completed first test. Second is recursive and could take longer.',r=1)
        fs=ff(start,pattern,d=1)
        kprint(fs,d2n('start=',start,' pattern=',IMAGE_PATTERNS))
        return fs
    if test:
        return _test()
    if type(pattern) is str:
        pattern=[pattern]
    return find_files(
                start,
                patterns=pattern,
                recursive=d,
                noisy=e,
            )

def fifs(
    start,
    pattern=IMAGE_PATTERNS,
    d=True,
    e=True,
    test=False,
):
    """
    fif find-image-files
    """
    return ff(
                start=start,
                pattern=pattern,
                d=d,
                e=e,
                test=test,
            )



def sfl(l,last=True,max=10,indicies=[],test=False):
    """
    sfl sample-from-list
    """
    def _test():
        m=sfl([1,2,3,4,5,6],)
        print(m)
        m=sfl([1,2,3,4,5,6],max=3)
        print(m)
        m=sfl([1,2,3,4,5,6],indicies=[-1,0,2])
        print(m)
    if test:
        _test()
        return
    m=[]
    if indicies:
        for i in indicies:
            cm(i,l[i])
            m.append(l[i])
        return m
    if max>=len(l):
        s=1
    else:
        s=len(l)//max
    assert s>=1
    for i in range(0,len(l),s):
        m.append(l[i])
    if last:
        while len(m)>=max:
            m.pop()
        m.append(l[-1])
    m=sorted(list(set(m)))
    return m







if __name__ == '__main__':
    eg(__file__)
    l = find_files(
        opjD(),
        "*.png",
    )
    l = sorted(l)
    for m in l:
        print(m)

#EOF
