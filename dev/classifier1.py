#https://raw.githubusercontent.com/pytorch/tutorials/main/beginner_source/blitz/cifar10_tutorial.py
#,a
import torch
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from utilz2 import *
clear_screen()

num_epochs=10000

device = torch.device('cuda:1' if torch.cuda.is_available() else 'cpu')




###############################################
###############################################
##
if 'datadic' not in locals():
    if not ope(opjD('datadic.pkl')):
        cg('need to create datadic',r=1)
        transform = transforms.Compose(
            [transforms.ToTensor(),
             transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        batch_size = 1
        trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                                download=True, transform=transform)
        trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                                  shuffle=False, num_workers=2)
        testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                               download=True, transform=transform)
        testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                                 shuffle=False, num_workers=2)
        datadic=dict(train=dict(inputs={},labels={}),test=dict(inputs={},labels={}))
        timer=Timer(1)
        k='train'
        for i, d in enumerate(trainloader, 0):
            if timer.rcheck():
                printr(k,i)
            datadic[k]['inputs'][i], datadic[k]['labels'][i] = d[0].to(device), d[1].to(device)
        printr(k,i+1)
        k='test'
        for i, d in enumerate(testloader, 0):
            if timer.rcheck():
                printr(k,i)
            datadic[k]['inputs'][i], datadic[k]['labels'][i] = d[0].to(device), d[1].to(device)
        printr(k,i+1)
        datadic['classes']=('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
        soD('datadic',datadic)
    else:
        datadic=loD('datadic',noisy=True)
    complete_train_img_indices=list(range(len(datadic['train']['inputs'])))
else:
    print('datadic already loaded.')
##
###############################################
###############################################



#, a
###############################################
###############################################
##
from kmodule.module_functions import *


class Simple_Block(nn.Module):
    def __init__(
        self,
        nch,
        nout,
        show='once',
    ):
        super(Simple_Block,self).__init__()
        packdict(self,locals())
        self.mdic=nn.ParameterDict()#nn.ModuleDict()
    def forward(self,x):
        describe_input(x,self,show,0)
        x=conv2d(
            'a',
            x,
            out_channels=8,
            kernel_size=3,
            stride=2,
            padding=1,
            mdic=self.mdic,
            activation=nn.ReLU(True),
            show=show,
        )
        x=conv2d(
            'b',
            x,
            out_channels=16,
            kernel_size=3,
            stride=2,
            padding=1,
            mdic=self.mdic,
            activation=nn.ReLU(True),
            show=show,
        )
        
        x=conv2d(
            'c',
            x,
            out_channels=32,
            kernel_size=3,
            stride=2,
            padding=1,
            mdic=self.mdic,
            activation=nn.ReLU(True),
            show=show,
        )
        
        x=conv2d(
            'd',
            x,
            out_channels=self.nout,
            kernel_size=3,
            stride=2,
            padding=0,
            mdic=self.mdic,
            activation=nn.ReLU(True),
            show=show,
        )
        describe_output(x,self,show,0)
        return x


if True:
    if True:#mdic' not in locals():
        mdic=nn.ModuleDict()
    show='once'
    ___show=straskys("""
        Simple_Block
    """)
    bs=1
    nin=3
    nch=8 
    nout=10
    xin=torch.from_numpy(na(rndn(bs,nin,32,32))).float()
    simple_block=Simple_Block(nch,nout=nout,show='always')
    """
    describe_tensor(xin,'xin',show='always')
    for i in range(1):
        print('i=',i)
        x=simple_block(xin)
    describe_tensor(x,'xout',show='always')
    """



net=dict(
    net=Simple_Block(nch,nout=nout,show='always'),
    criterion=nn.MSELoss(),
    loss_dic={},
    median_loss_dic=None,
    own_train_indices=set(complete_train_img_indices),
)
x=net['net'](xin)
net['net'].to(device)
net['optimizer']=optim.Adam(net['net'].parameters(),lr=.001,betas=(0.5,0.999))


def look_at_own_train_indicies(net):
    l=list(net['own_train_indices'])
    print('len(own_train_indices)=',len(l))
    cats={}
    for i in l:
        c=datadic['classes'][datadic['train']['labels'][i]]
        if c not in cats:
            cats[c]=0
        cats[c]+=1
    kprint(cats,title='category breakdown',make_sorted=True)
    hist(net['loss_dic'].values())
    #plt.xlim(0,0.2)
##
###############################################
###############################################









def run_net_through_training_inputs(net,img_indices):
    running_loss=0.
    net['net'].train()
    run_indicies=deepcopy(img_indices)
    ctr=0
    for i in run_indicies[:1000]:
        ctr+=1
        inputs=datadic['train']['inputs'][i]
        targets=torch.zeros((1,len(datadic['classes']))).float().to(device)
        targets[0,int(datadic['train']['labels'][i])]=1
        printr('normal target',i,10*' ')
        net['optimizer'].zero_grad()
        outputs = net['net'](inputs)
        loss = net['criterion'](outputs[:,:,0,0],targets) 
        running_loss += loss.item()
        loss.backward()
        net['optimizer'].step()
    print('ctr=',ctr,'loss:',dp(running_loss/ctr,3))
    running_loss = 0.0



def egs_best_worst(loss_dic):
    s=0
    task='train'
    m=sort_by_value(loss_dic,reverse=False)
    ks=kys(m)
    a=[]
    for i in range(100):
        a.append(cuda_to_rgb_image(datadic[task]['inputs'][ks[i]]))
    q=d2s(s,'best')
    sh(a,q,title=q)
    a=[]
    for i in range(len(ks)-100,len(ks)):
        a.append(cuda_to_rgb_image(datadic[task]['inputs'][ks[i]]))
    q=d2s(s,'worst')
    sh(a,q,title=q)
    np.random.shuffle(ks)
    a=[]
    for i in range(100):
        a.append(cuda_to_rgb_image(datadic[task]['inputs'][ks[i]]))
    q=d2s(s,'random selection')
    sh(a,q,title=q)









###############################################
###############################################
##
#if 'training loop':
#def train():
task='train'
print('Start training . . .')
for epoch in range(num_epochs):
    print('epoch=',epoch)
    input_subset=deepcopy(complete_train_img_indices)
    np.random.shuffle(input_subset)
    input_subset=input_subset[:len(input_subset)//1]

    print('training net')
    run_net_through_training_inputs(
        net,
        input_subset,
        )

    print('Finished epoch training.')

    print('Start eval . . .')

    print('evaluating net')
    run_net_through_training_inputs(
            net,
            complete_train_img_indices,
            )
    print('Finished eval.')

    if epoch%3==0:
        task='test'
        correct_pred = {classname: 0 for classname in datadic['classes']}
        total_pred = {classname: 0 for classname in datadic['classes']}

        with torch.no_grad():
            for i in datadic[task]['inputs']:
                ##sh(datadic[task]['inputs'][i],1)
                ##figure(2);clf()
                #print(datadic[task]['labels'][i].item())
                #printr(i)
                output=None

                label=datadic[task]['labels'][i].item()
                o=net['net'](datadic[task]['inputs'][i])
                o=o.detach().cpu().numpy()[0]
                ##plot(range(10),o)#;cm(r=1);spause()
                if isNone(output):
                    output=0*o

                output+=o#z2o(o)
                ##plot(range(10),output,'.-')
                ##plot(label,max(output),'ko')
                prediction=np.argmax(output)
                mx=max(output)
                #print(datadic['classes'][label],label,'<-',prediction)
                if label==prediction:
                    correct_pred[datadic['classes'][label]] += 1
                    #print('correct')
                else:
                    pass
                    #print('incorrect')
                total_pred[datadic['classes'][label]] += 1
                ##spause()
                ##cm(r=1)

            for classname, correct_count in correct_pred.items():
                accuracy = 100 * float(correct_count) / total_pred[classname]
                print('Accuracy for class:',classname,'is',accuracy)


            #figure(d2s(100+n,time_str()))
            #look_at_own_train_indicies(net)

egs_best_worst(net['loss_dic'])
spause()
##
###############################################
###############################################






#,b


















"""
('0 plane',
 '1 car',
 '2 bird',
 '3 cat',
 '4 deer',
 '5 dog',
 '6 frog',
 '7 horse',
 '8 ship',
 '9 truck')
"""
pass

#EOF
