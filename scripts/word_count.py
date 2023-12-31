#!/usr/bin/env python3

from k3 import *
from k3.utils.vis import *
from striprtf.striprtf import rtf_to_text

path = select_folder()[0]

_fs = sggo(path,'*.rtf')
F = {}
for _f in _fs:
    if fname(_f)[0] != '_':
        if fnamene(_f) in F:
            print(_f)
            assert False
        _name = fnamene(_f)
        if 'ignore' in _f:
            continue
            print(fname(_f))
            _name = fname(_f).split('_ignore')[0]
            cr(_name)
        F[_name] = _f
del _f,_name


def get_Count(text):
    c = []
    for d in text: 
        if d.isalpha(): 
            c.append(d) 
        else: 
            c.append(' ')
    e=''.join(c)
    f=e.split(' ')
    g=remove_empty(f)
    C = {}
    for h in g:
        if h not in C:
            C[h] = 1
        else:
            C[h] += 1
    return len(g)


count = 0
for _f in F:
    count += get_Count( file_to_text(rtf_to_text(F[_f])))
print("Word count =",count)


#EOF
