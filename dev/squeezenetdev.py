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
        self,
        inplanes,
        squeeze_planes,
        expand1x1_planes,
        expand3x3_planes
    ):
        super(Fire, self).__init__()
        self.inplanes = inplanes
        self.squeeze = nn.Conv2d(inplanes, squeeze_planes, kernel_size=1)
        self.squeeze_activation = nn.ReLU(inplace=True)
        self.expand1x1 = nn.Conv2d(squeeze_planes, expand1x1_planes, kernel_size=1)
        self.expand1x1_activation = nn.ReLU(inplace=True)
        self.expand3x3 = nn.Conv2d(squeeze_planes, expand3x3_planes, kernel_size=3, padding=1)
        self.expand3x3_activation = nn.ReLU(inplace=True)
    def forward(self, x):
        x = self.squeeze_activation(self.squeeze(x))
        return torch.cat([
            self.expand1x1_activation(self.expand1x1(x)),
            self.expand3x3_activation(self.expand3x3(x))
        ], 1)


class SqueezeNet(nn.Module):

    def __init__(self):
        super(SqueezeNet, self).__init__()
        self.A = {}
        self.lr = 0.01
        self.momentum = 0.001 #0.0001
        self.N_FRAMES = 2
        self.N_STEPS = 10
        self.main = nn.Sequential(
                                                                    dscl('SqueezeNet input',True),
            nn.Conv2d(1, 64, kernel_size=3, stride=2, padding=1),              dscl('\ta Conv2d output',True),
            nn.ReLU(inplace=True),                                  dscl('\tb ReLU output',True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),  dscl('\tc MaxPool2d output',True),
            Fire(64, 8, 16, 16),                                      dscl('\td Fire output',True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),  dscl('\te MaxPool2d output',True),
            Fire(32, 16, 32, 32),                                      dscl('\tf Fire output',True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),  dscl('\tg MaxPool2d output',True),
            Fire(64, 32, 64,64),                                      dscl('\th Fire output',True),
            nn.MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),  dscl('\ti MaxPool2d output',True),
            nn.Conv2d(128,1,kernel_size=1),                        dscl('\tj Conv2d output',True),
            nn.AvgPool2d(kernel_size=3, stride=2),                  dscl('\tk AvgPool2d output',True),
        )

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                if False:#m is final_conv:
                    init.normal(m.weight.data, mean=0.0, std=0.01)
                else:
                    init.kaiming_uniform(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()


    def forward(self, x):
        return self.main(x)


#self.nets[k].apply(f___weights_init)

def unit_test():
    print(__file__,'unit_test()')
    test_net = SqueezeNet()
    for i in range(10):
        t0=time.time()
        a = test_net(Variable(torch.randn(304, 1, 128, 128)))
        print(i,time.time()-t0)
        #t0=time.time()
        #a = test_net(Variable(torch.randn(1, 1, 2464, 2064)))
        #print(i,time.time()-t0)  
    print('Tested SqueezeNet')


if __name__=='__main__':
    unit_test()



#EOF

