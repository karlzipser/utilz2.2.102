from utilz2 import *
from utilz2.torch_.init import *
import math
import torch
import torch.nn as nn
import torch.nn.init as init
from torch.autograd import Variable


def f___weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        #cm(classname,r=1)
        nn.init.normal_(m.weight.data, 0.0, 0.02)
    if classname.find('ConvTranspose2d') != -1:
        nn.init.normal_(m.weight.data, 0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        nn.init.normal_(m.weight.data, 1.0, 0.02)
        nn.init.constant_(m.bias.data, 0)

class Describe_Layer(nn.Module):
    def __init__(
        _,
        name,
        show,
        endl='',
    ):
        super( Describe_Layer, _).__init__()
        _.name = name
        _.show = show
        _.first_pass = True
        _.endl = endl
    def forward(_, x):
        if _.first_pass and _.show:
            s = shape_from_torch(x)
            print(_.name+':',s,dp(s[1]*s[2]*s[3]/1000.,1),'\bk',_.endl)
            _.first_pass = False
        return x
dscl=Describe_Layer
#
########################################


class Fire(nn.Module):

    def __init__(
        _,
        inplanes,
        squeeze_planes,
        expand1x1_planes,
        expand3x3_planes,
        godown=False,
        goup=False,
    ):
        super(Fire, _).__init__()
        _.inplanes = inplanes
        _.godown=godown
        _.goup=goup
        _.squeeze = nn.Conv2d(inplanes, squeeze_planes, kernel_size=1)
        _.squeeze_activation = nn.ReLU(inplace=True)
        _.expand1x1 = nn.Conv2d(squeeze_planes, expand1x1_planes, kernel_size=1)
        _.expand1x1_activation = nn.ReLU(inplace=True)
        _.expand3x3 = nn.Conv2d(squeeze_planes, expand3x3_planes, kernel_size=3, padding=1)
        _.expand3x3_activation = nn.ReLU(inplace=True)
        _.relu=nn.ReLU(inplace=True)
        _.down=nn.Conv2d(squeeze_planes, squeeze_planes, kernel_size=3, stride=2, padding=1)
        _.up=nn.ConvTranspose2d(squeeze_planes, squeeze_planes, kernel_size=3, stride=2, padding=0)

    def forward(_, x):
        x = _.squeeze_activation(_.squeeze(x))
        if _.godown:
            x=_.down(x)
            x=_.relu(x)
        if _.goup:
            x=_.up(x)
            x=_.relu(x)

        return torch.cat([
            _.expand1x1_activation(_.expand1x1(x)),
            _.expand3x3_activation(_.expand3x3(x))
        ], 1)


"""
class SqueezeNet_down(nn.Module):
    def __init__(
        _,
        nin=3,
        n=8,
        nout=1,
        sigmoid=True,
    ):
        super(SqueezeNet_down, _).__init__()
        if sigmoid:
            final=nn.Sigmoid
        else:
            final=nn.Identity
        _.main1 = nn.Sequential(
            nn.Identity(),                                              dscl('SqueezeNet input',True),
            nn.Conv2d(nin, 2*n, kernel_size=3, stride=2, padding=1),    dscl('\ta Conv2d output',True),
            nn.BatchNorm2d(2*n),
            nn.ReLU(inplace=True),                                      dscl('\tb ReLU output',True),
            
            Fire(2*n, n, n, n,True),                                         dscl('\td Fire output',True),
            Fire(2*n, 2*n, 2*n, 2*n),                               dscl('\te Fire output',True),
            nn.BatchNorm2d(4*n),
            Fire(4*n, 2*n, 2*n, 2*n,True),                               dscl('\tg Fire output',True),
            Fire(4*n, 2*n, 4*n, 4*n),                               dscl('\th Fire output',True),
            nn.BatchNorm2d(8*n),
            Fire(8*n, 4*n, 4*n, 4*n,True),                               dscl('\tj Fire output',True),
            Fire(8*n, 4*n, 8*n, 8*n,True),                               dscl('\tk Fire output',True),
            nn.BatchNorm2d(16*n),
            nn.Conv2d(16*n,nout,kernel_size=3,stride=2),                     dscl('\tm Conv2d output',True),
            #nn.AvgPool2d(kernel_size=2, stride=2),                  dscl('\tn AvgPool2d output',True),
            final(),
        )
        for m in _.modules():
            if isinstance(m, nn.Conv2d):
                if False:#m is final_conv:
                    init.normal(m.weight.data, mean=0.0, std=0.01)
                else:
                    init.kaiming_uniform(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()
    def forward(_, x):
        return _.main1(x)
"""




"""
class SqueezeNet_deconv(nn.Module):
    def __init__(
        _,
        nin=1,
        n=8,
        nout=1,
    ):
        super(SqueezeNet_deconv, _).__init__()
        _.main1 = nn.Sequential(
            nn.Identity(),                                          dscl('SqueezeNet_deconv input',True),
            nn.ConvTranspose2d(nin, 2*n, kernel_size=3, stride=1, padding=0),   dscl('\ta ConvTranspose2d output',True),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(2*n, 2*n, kernel_size=3, stride=2, padding=0),   dscl('\tmp ConvTranspose2d output',True), 
            nn.ReLU(inplace=True),                                 dscl('\tb ReLU output',True),
            Fire(2*n, n, 2*n, 2*n,False,True),                                         dscl('\td up Fire output',True),
            #Fire(2*n, 2*n, 2*n, 2*n),                                   dscl('\td Fire output',True),
            nn.ConvTranspose2d(4*n, 4*n, kernel_size=3, stride=2, padding=0),   dscl('\tmp ConvTranspose2d output',True),
            nn.ReLU(inplace=True),
            #Fire(4*n, 2*n, 2*n, 2*n),                                   dscl('\td Fire output',True),
            Fire(4*n, 2*n, 4*n, 4*n),                                   dscl('\tf Fire output',True),
            nn.ConvTranspose2d(8*n, 8*n, kernel_size=3, stride=2, padding=0),   dscl('\tmp ConvTranspose2d output',True),
            nn.ReLU(inplace=True),
            #Fire(8*n, 4*n, 4*n, 4*n),
            Fire(8*n, 4*n, 8*n, 8*n),                                   dscl('\th Fire output',True),
            nn.ConvTranspose2d(16*n, 16*n, kernel_size=3, stride=2, padding=1),   dscl('\tmp ConvTranspose2d output',True),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(16*n,nout,kernel_size=4),                          dscl('\tj ConvTranspose2d output',True),

        )
        
        for m in _.modules():
            if isinstance(m, nn.ConvTranspose2d):
                if False:#m is final_conv:
                    init.normal(m.weight.data, mean=0.0, std=0.01)
                else:
                    init.kaiming_uniform(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()
        
    def forward(_, x):
        return _.main1(x)







class SqueezeNet_no_mp(nn.Module):
    def __init__(
        _,
        nin=1,
        n=8,
        nout=1,
        sigmoid=True,
    ):
        super(SqueezeNet_no_mp, _).__init__()
        if sigmoid:
            final=nn.Sigmoid
        else:
            final=nn.Identity
        _.main1 = nn.Sequential(
            nn.Identity(),                                              dscl('SqueezeNet input',True),
            nn.Conv2d(nin, 2*n, kernel_size=3, stride=2, padding=1),    dscl('\ta Conv2d output',True),
            nn.ReLU(inplace=True),                                      dscl('\tb ReLU output',True),
            nn.Conv2d(2*n, 2*n, kernel_size=3, stride=2, padding=1),   dscl('\tmp Conv2d output',True),
            Fire(2*n, n, n, n),                                         dscl('\td Fire output',True),
            Fire(2*n, 2*n, 2*n, 2*n),                               dscl('\te Fire output',True),
            nn.Conv2d(4*n, 4*n, kernel_size=3, stride=2, padding=1),   dscl('\tmp Conv2d output',True),
            Fire(4*n, 2*n, 2*n, 2*n),                               dscl('\tg Fire output',True),
            Fire(4*n, 2*n, 4*n, 4*n),                               dscl('\th Fire output',True),
            nn.Conv2d(8*n, 8*n, kernel_size=3, stride=2, padding=1),   dscl('\tmp Conv2d output',True),
            Fire(8*n, 4*n, 4*n, 4*n),                               dscl('\tj Fire output',True),
            Fire(8*n, 4*n, 8*n, 8*n),                               dscl('\tk Fire output',True),
            nn.Conv2d(16*n, 16*n, kernel_size=3, stride=2, padding=1),   dscl('\tmp Conv2d output',True),
            nn.Conv2d(16*n,nout,kernel_size=3,stride=2),                     dscl('\tm Conv2d output',True),
            final(),
        )
        for m in _.modules():
            if isinstance(m, nn.Conv2d):
                if False:#m is final_conv:
                    init.normal(m.weight.data, mean=0.0, std=0.01)
                else:
                    init.kaiming_uniform(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()
    def forward(_, x):
        return _.main1(x)



class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.main = nn.Sequential(  
                                                                        Describe_Layer('Generator input',True),
            nn.ConvTranspose2d( nin, 16*n, 4, 1, 0),      Describe_Layer('ConvTranspose2d output',True),
            nn.ReLU(True),

            Fire(16*n, 4*n, 4*n, 4*n),                                         dscl('\td Fire output',True),

            nn.ConvTranspose2d(ngf * 8*8, ngf * 4*4, 4, 2, 1, bias=False),  Describe_Layer('ConvTranspose2d output',True),
            nn.BatchNorm2d(ngf * 4*4),
            nn.ReLU(True),

            nn.ConvTranspose2d( ngf * 4*4, ngf * 4, 4, 2, 1, bias=False), Describe_Layer('ConvTranspose2d output',True),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),

            nn.ConvTranspose2d( ngf * 4, ngf, 4, 2, 1, bias=False),     Describe_Layer('ConvTranspose2d output',True),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),

            nn.ConvTranspose2d( ngf, ngf//2, 4, 2, 1, bias=False),      Describe_Layer('ConvTranspose2d output',True),
            nn.BatchNorm2d(ngf//2),
            nn.ReLU(True),

            nn.ConvTranspose2d( ngf//2, nc, 4, 2, 1),       Describe_Layer('ConvTranspose2d output',True,'\n'),
            #nn.Upsample((image_size,image_size),mode='nearest'),        Describe_Layer('Upsample output',True,'\n'),
            nn.Tanh()
        )
    def forward(self, input):
        return self.main(input)
"""







class SqueezeNet(nn.Module):
    def __init__(
        _,
        nin=1,
        n=8,
        nout=1,
        sigmoid=True,
    ):
        super(SqueezeNet, _).__init__()
        if sigmoid:
            final=nn.Sigmoid
        else:
            final=nn.Identity
        _.main1 = nn.Sequential(
            nn.Identity(),                                              dscl('SqueezeNet input',True),
            nn.Conv2d(nin, 2*n, kernel_size=3, stride=2, padding=1),    dscl('\ta Conv2d output',True),
            nn.ReLU(inplace=True),                                      dscl('\tb ReLU output',True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),      dscl('\tc MaxPool2d output',True),
            #Fire(2*n, n, n, n),                                         dscl('\td Fire output',True),
            Fire(2*n, 2*n, 2*n, 2*n),                               dscl('\te Fire output',True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),  dscl('\tf MaxPool2d output',True),
            #Fire(4*n, 2*n, 2*n, 2*n),                               dscl('\tg Fire output',True),
            Fire(4*n, 2*n, 4*n, 4*n),                               dscl('\th Fire output',True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),  dscl('\ti MaxPool2d output',True),
            #Fire(8*n, 4*n, 4*n, 4*n),                               dscl('\tj Fire output',True),
            Fire(8*n, 4*n, 8*n, 8*n),                               dscl('\tk Fire output',True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),  dscl('\tl MaxPool2d output',True),
            nn.Conv2d(16*n,nout,kernel_size=2),                     dscl('\tm Conv2d output',True),
            nn.AvgPool2d(kernel_size=2, stride=2),                  dscl('\tn AvgPool2d output',True),
            final(),
        )
        for m in _.modules():
            if isinstance(m, nn.Conv2d):
                if False:#m is final_conv:
                    init.normal(m.weight.data, mean=0.0, std=0.01)
                else:
                    init.kaiming_uniform(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()
    def forward(_, x):
        return _.main1(x)



def unit_test():

    print(__file__,'unit_test()')
    device = torch.device('cuda:0' if (torch.cuda.is_available()) else "cpu")
    
    CA()
    ns={}
    nlist=[3,6,8,9,10,11,12,13,14,15,16,32,64]
    for n in nlist:
        try:
            test_net = SqueezeNet(1,n,1).to(device)
            dts=[]
            x=Variable(torch.randn(304, 1, 128, 128)).to(device)
            #x=Variable(torch.randn(1, 1, 2464, 2064)).to(device)
            for i in range(100):
                t0=time.time()
                a = test_net(x)
                dt=time.time()-t0
                #if dt>0.004 and dt < 0.02:
                #    dts.append(1/dt)
                dts.append(dt)
                print(i,dt,5*' ',end='\r') 
            #print('\nTested SqueezeNet.')
            #hist(dts[1:],bins=1000)
            m=np.median(dts)
            ns[n]=m
            #title(m)
            #spause()
            #cm(r=1)
        except:
            break
    plot(list(ns.keys()),1/na(list(ns.values())),'o-')
    plt.xlabel('n')
    plt.ylabel('Hz')
    plt.xlim(0,max(nlist))

def unit_test2():
    print(__file__,'unit_test()')
    device = torch.device('cuda:0' if (torch.cuda.is_available()) else "cpu")
    n=8
    test_net = SqueezeNet_deconv(100,n,3).to(device)
    x=Variable(torch.randn(304, 100, 1, 1)).to(device)
    a = test_net(x)
    print(a.size())

if __name__=='__main__':
    unit_test2()
    cm(r=1)


#EOF

