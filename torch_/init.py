from utilz2.vis import *
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

Global_ = dict(show=True)

def shape_from_tensor(x):
    return shape( x.cpu().detach().numpy() )

def cuda_to_rgb_image(cu):
    if len(cu.size()) == 3:
        return z55(cu.detach().cpu().numpy().transpose(1,2,0))
    elif len(cu.size()) == 4:
        return z55(cu.detach().cpu().numpy()[0,:].transpose(1,2,0))
    else:
        assert False

def shape_from_torch(x):
    s = shape(x)
    so = []
    for i in rlen(s):
        so.append(s[i])
    return tuple(so)

def layer_description_(name,x):
    if len(x.size()) == 4:
        k = x.size(1)*x.size(2)*x.size(3)//1000
    elif len(x.size()) == 3:
        k = x.size(1)*x.size(2)//1000
    else:
        k = -1
    print(name,tuple(x.size()),d2n(k,'k'))

def layer_description(name,x,indent=0,max_name_length=20):
    if not Global_['show']:
        return
    try:
        if len(x.size()) == 4:
            k = intr(x.size(1)*x.size(2)*x.size(3)/1000.)
        elif len(x.size()) == 3:
            k = intr(x.size(1)*x.size(2)/1000.)
        else:
            k = -1
        a = list(x.size())
        n_channels = a[1]
        dim = d2n(a[2],'x',a[3])
        cg(4*' '*indent,name,'.'*(4+max_name_length-len(name)),n_channels,dim,d2n(k,'k'))
    except:
        cy(4*' '*indent,name,'.'*(4+max_name_length-len(name)))


def ps(x,name='',print_shape=False,indent=0,max_name_length=20):
    if print_shape:
        layer_description(name,x,indent,max_name_length)

def ps_(x,name='',indent=0,max_name_length=20):
    layer_description(name,x,indent,max_name_length)

def one_in(n):
    a = randint(n)
    if a:
        return False
    else:
        return True

def icy(name,indent):
    if Global_['show']:
        cy(4*' '*indent,name)
        


#EOF
