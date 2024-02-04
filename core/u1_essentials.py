from utilz2.core.u0_imports import *

def mergedict(p,newp):
    if type(p) is not dict:
        p=p.__dict__
        print('*** Warning, p=p.__dict__')
    if type(newp) is not dict:
        newp=newp.__dict__
        print('*** Warning, newp=newp.__dict__')
    for k in newp:
        assert k in p
        if type(p[k])!=type(newp[k]):
            print('*** Error with mergedict(): key,',k,'type of src',type(newp[k]),'not same as type of dest',type(p[k]))
            assert False
        p[k]=newp[k]

def typename(o):
    """
    Get a string for the name of a type
    """
    return str(type(o)).split("'")[1]

def boxed(text,title=''):
    # https://stackoverflow.com/questions/20756516/python-create-a-text-border-with-dynamic-size
    title=' '+title+' '
    text = str(text)
    lines = text.splitlines()
    width = max(max(len(s) for s in lines),len(title)+1)
    #res = ['┌' + '─' * width + '┐']
    top = '┌' + '─' + title
    top += (width-len(top)+1) * '─' + '┐'
    res = [top]
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)
  

def box(text,title=''):
    print(boxed(text,title))


def sort_by_value(D,reverse=True):
    return {k: v for k, v in sorted(D.items(), reverse=reverse, key=lambda item: item[1])}


def print_dic_simple(D,title='<title>',html=False,print_=True,center=False):
    el = '\n'
    if html:
        el +=''
    if title != '':
        s = title+el
    else:
        s = ''
    if type(D) is not dict:
        if print_:
            print(D)
    else:
        longest = 0
        for k in sorted(D):
            if len(str(k)) > longest:
                longest = len(str(k))
        for k in sorted(D):
            if center:
                sk = ' '*(longest-len(str(k)))+str(k)
            else:
                sk = str(k)
            if k[0] != '-' and type(D[k]) is str:
                q = qtd(D[k],s=True)
            else:
                q = str(D[k])
            s += '   '+sk+':  '+q+el;
    if print_:
        print(s)
    return s


def clear_screen():
    print(chr(27) + "[2J")
    


def intr(n):
    #import numpy as np
    return int(np.round(n))


def qtd(a,s=False):
    if a == '':
        return "''"
    if type(a) == str and ((a[0] == '\'' and a[-1] == '\'') or (a[0] == '\"' and a[-1] == '\"')):
        print('*** qtd(): Warning, '+a+' seems to be quoted already ***')
    if not s:
        return '\"'+str(a)+'\"'
    else:
        return '\''+str(a)+'\''


def qtds(a):
	return qtd(a,s=1)


def raw_enter(optional_str=''):
    return input(optional_str+'   Hit enter to continue > ')


def is_even(q):
    import numpy as np
    if np.mod(q,2) == 0:
        return True
    return False
    

def str_is_int(s):
    try:
        int(s)
        return True
    except:
        return False


def str_is_float(s):
    try:
        float(s)
        return True
    except:
        return False


def rlen(a):
    return range(len(a))


def getch():
    import sys, termios, tty, os, time
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def k_in_D(k,D):
    if k not in D:
        return False
    else:
        return D[k]
kin = k_in_D


def is_number(n):
    import numbers
    if type(n) == bool:
        return False
    if type(n) == type(None):
        return False
    return isinstance(n,numbers.Number)


def bound_value(the_value,the_min,the_max):
    if the_value > the_max:
        return the_max
    elif the_value < the_min:
        return the_min
    else:
        return the_value


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    def atoi(text):
        return int(text) if text.isdigit() else text
    return [ atoi(c) for c in re.split('(\d+)', text) ]



    

def all_values(D):
    def get_all_values(d):
        #https://stackoverflow.com/questions/7002429/how-can-i-extract-all-values-from-a-dictionary-in-python
        if isinstance(d, dict):
            for v in d.values():
                yield from get_all_values(v)
        elif isinstance(d, list):
            for v in d:
                yield from get_all_values(v)
        else:
            yield d
    return sorted(list(get_all_values(D)))





def kys(D):
    return list(D.keys())



                

def advance(lst,e,min_len=1):
    len_lst = len(lst)
    if len_lst < min_len:
        pass
    elif len_lst > 1.2*min_len:
        lst = lst[-min_len:]
    else:
        lst.pop(0)
    lst.append(e)


def a_key(dic):
    keys_ = kys(dic)
    import numpy as np
    k = np.random.randint(len(keys_))
    return keys_[k]
akey=a_key


def an_element(dic):
    return dic[a_key(dic)]
aval=an_element

def kth( dic, i ):
    """
    get the ith key of dic
    """
    return kys( dic )[i]

def vth( dic, i ):
    """
    get the ith value of dic
    """
    return dic[ kth( dic, i ) ]

nth = vth


def remove_empty(l):
    m = []
    for a in l:
        if a != '':
            m.append(a)
    return m


def space(s):
    a = s.split(' ')
    return remove_empty(a)



"""
https://stackoverflow.com/questions/2673385/how-to-generate-random-number-with-the-specific-length-in-python
"""
from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
    

def is_None(a):
    if type(a) == type(None):
        return True
    return False
isNone = is_None
    


def shapes(*args):
    l=[]
    for a in args:
        l.append(str(shape(a)))
    return ' '.join(l)


def merg_dict(src,dst):
    a,b = src,dst
    for k in a:
        assert k not in b
        b[k] = a[k]
        return b


def straskys(s):
    s=s.replace(',',' ').replace('\n',' ')
    x=remove_empty(s.split(' '))
    return x



def eg(f,cs=False):
    if cs:
        clear_screen()
    else:
        print()
    if False:
        s = "│ Examples from "+f+":"
        print('┌'+(len(s)-1)*'─'+'\n'+s+'\n')
    box('E.g.s from '+f)





if True:
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


if __name__ == '__main__':
    eg(__file__)
    print("int(1.9) =",int(1.9))
    print("intr(1.9) =",str(intr(1.9)))
    print()

    
#EOF
