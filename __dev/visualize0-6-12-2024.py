
#l = [module for module in model.modules() if not isinstance(module, nn.Sequential)]
# exec(gcsp3(opjh('knets-before-5-21-2024'),include_output=1,show_snippet=0));merge_snippets2(default_height=300);CA()
# merge_snippets2('/home/karl/snippets/working')
if False:
    ndf=64
    net=dict(
        net=Net(1,ndf,29),
        criterion=nn.MSELoss(),
        loss_dic=None,
    )
    net['net'].to(device)
    net['optimizer']=optim.Adam(net['net'].parameters(),lr=.001,betas=(0.5,0.999))
    net_path='/home/karl/Desktop/rf-model.07Jun24_11h14m25s.pth'#opjD('rf-model.05Jun24_16h20m00s.pth')
    net_path='/home/karl/Desktop/rf-model.07Jun24_11h58m19s.pth'
    net_path='/home/karl/Desktop/rf-model.07Jun24_12h14m07s.pth'
    net_path='/home/karl/Desktop/rf-model.07Jun24_12h56m17s.pth'
    net_path='/home/karl/Desktop/rf-model.07Jun24_13h18m06s.pth'
    cb(net_path,r=1)
if True:
    nin=1
    ndf=64
    nout=2
    net=dict(
        net=Net(nin,ndf,nout),
        criterion=nn.MSELoss(),
        loss_dic=None,
    )
    net['net'].to(device)
    #net_path=opjD('rf-model.17May24_10h30m02s.pth')
    #net_path=opjD('rf-AJ-detector-92pct-253-samples.pth' )
    #net_path=opjD('rf-model.05Jun24_16h20m00s.pth')
    net_path=net_path='/home/karl/Desktop/rf-model.12Jun24_16h18m46s.pth'
    #cb('\t',net['net'].load_state_dict(torch.load(net_path),strict=False))


net['net'].to('cuda:0')
cb('\t',net['net'].load_state_dict(torch.load(net_path),strict=False))



#for i in range(100):
#    print(i,model[i])
"""
1 Describe_Layer()
2 Conv2d(1, 16, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1))
3 Describe_Layer()
4 LeakyReLU(negative_slope=0.2, inplace=True)
5 Conv2d(16, 64, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), bias=False)
6 Describe_Layer()
7 BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
8 LeakyReLU(negative_slope=0.2, inplace=True)
9 Conv2d(64, 256, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), bias=False)
10 Describe_Layer()
11 BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
12 LeakyReLU(negative_slope=0.2, inplace=True)
13 Conv2d(256, 1024, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), bias=False)
14 Describe_Layer()
15 BatchNorm2d(1024, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
16 LeakyReLU(negative_slope=0.2, inplace=True)
17 Conv2d(1024, 2048, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), bias=False)
18 Describe_Layer()
19 BatchNorm2d(2048, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
20 LeakyReLU(negative_slope=0.2, inplace=True)
21 Conv2d(2048, 29, kernel_size=(4, 4), stride=(1, 1))
22 Describe_Layer()
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
import matplotlib.pyplot as plt
import numpy as np

# Load a pre-trained model
model = [module for module in net['net'].modules() if not isinstance(module, nn.Sequential)]
#model.eval()

# Define the target layer and neuron
target_layer = 28  # For example, layer 28 in VGG16
target_neuron = 0  # The first neuron in the layer

# Create a random input image


# Define the optimizer


# Normalize the image
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])


imgs={}
# Optimization loop
blank=get_blank_rgb(128,128)

#,a
layers=[2]
layers=[2,4,5]
layers=[2,4,5,8,9]
layers=[2,4,5,8,9,12,13]
layers=[2,4,5,8,9,12,13,16,17]
#layers=[2,4,5,8,9,12,13,16,17,20,21]
for target_neuron in range(64):
    try:
        input_image = torch.randn(1, 1, 128, 128, requires_grad=True,device='cuda:0')
        input_image_big = torch.randn(1, 1, 128+4, 128+4, requires_grad=False,device='cuda:0')
        optimizer = optim.Adam([input_image], lr=0.1, weight_decay=1e-6)
        for i in range(200):
            if False:
                input_image.requires_grad=False
                input_image*=.75
                input_image.requires_grad=True
            if False:
                input_image.requires_grad=False
                input_image+=0.01*torch.randn(1, 1, 128, 128, device='cuda:0')
                input_image.requires_grad=True
            if True:
                input_image.requires_grad=False
                dx=np.random.choice([-1,0,1])
                dy=np.random.choice([-1,0,1])
                input_image_big[0,0,1+dx:1+128+dx,1+dy:1+128+dy]=input_image
                input_image[0,0,:,:]=input_image_big[0,0,1:128+1,1:128+1]
                #input_image+=0.01*torch.randn(1, 1, 128, 128, device='cuda:0')
                input_image.requires_grad=True

            optimizer.zero_grad()
            
            # Forward pass to the target layer
            x = input_image
            for j in layers:#,20,21]:#range(target_layer + 1):
                #print(j)
                #cg('xin',x.size())
                x = model[j](x)
                #cg('xout',x.size())
            # Define the loss as the negative of the target neuron's activation
            loss = -x[0, target_neuron].mean()+0e7*input_image.mean()
            # 21:40000 17:1000 13:100 9:10 5:1 2:0
            # Backward pass
            loss.backward()
            #cb('backward',j)
            # Update the input image
            optimizer.step()
            #cm('optimzer',j)
            
            #print(optimized_image.min(),optimized_image.max())
            # Apply normalization
            with torch.no_grad():
                input_image.clamp_(0, 1)

            # Print progress
            if (i + 1) % 50 == 0:
                print(f'Iteration {i + 1}, Loss: {loss.item()}')

        optimized_image = input_image.detach().cpu().numpy()[0].transpose(1, 2, 0)
        for i in range(3):
            blank[:,:,i]=(255*z2o(optimized_image[:,:,0])).astype(np.uint8)
        n=layers[-1]
        if n not in imgs:
            imgs[n]={}
        imgs[n][str(target_neuron)]=1*blank
        figure(d2s(n),figsize=(18,18))
        sh(imgs[n],d2s(n),r=0,use_dict_keys_as_titles=False)#optimized_image,target_neuron,r=0)





    
    
    except KeyboardInterrupt:
        cr('*** KeyboardInterrupt ***')
        sys.exit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Exception!')
        print(d2s(exc_type,file_name,exc_tb.tb_lineno))   
    
#,b

# Convert the optimized image to a NumPy array
#optimized_image = input_image.detach().cpu().numpy()[0].transpose(1, 2, 0)
#optimized_image = (optimized_image - optimized_image.min()) / (optimized_image.max() - optimized_image.min())

# Plot the optimized image
#plt.imshow(optimized_image)
#plt.title(f'Optimal input image for layer {target_layer}, neuron {target_neuron}')
#plt.show()