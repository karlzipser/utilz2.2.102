
from utilz2 import *

max_dic_len=500
imgdic={}
q=1/1

def augimg(img):
    #print(shape(img),img.min(),img.max())
    q=np.random.random()/4+0.75
    if len(imgdic)>2:
        mask=an_element(imgdic)
        if randint(2)<1: mask=cv2.flip(mask,flipCode=0)
        if randint(2)<1: mask=cv2.flip(mask,flipCode=1)
        m=mask[:,:,0]
        m[m>0.5]=1.
        m[m<1]=0.
        for i in range(3):
            mask[:,:,i]=m
        dimgs=[]
        for i in range(2):
            a=bound_value(q*rndn(),-1,1)
            g=an_element(imgdic)
            if randint(2)<1: g=cv2.flip(g,flipCode=0)
            if randint(2)<1: g=cv2.flip(g,flipCode=1)
            dimgs.append(a*g)
        new_img=1*img
        new_img+=mask*dimgs[0]
        new_img+=(1-mask)*dimgs[1]
        #sh(mask,2)
    else:
        new_img=img

    #print(len(imgdic))
    if len(imgdic)>=max_dic_len:
        del(imgdic[akey(imgdic)])
    
    imgdic[time.time()]=img

    return new_img

    



if __name__ == '__main__':

    imgdic={}
    max_dic_len=3
    q=1/3

    fs=sggo(opjh('Desktop/*.png'))

    for f in fs:
        img=rimread(f)
        img=cv2.resize(img,(300,200))
        img=(img/255.).astype(np.float32)
        img=augimg(img)
        sh(img,r=1)

#EOF
