
from utilz2 import *

max_dic_len=500
imgdic={}
q=1/3

def augimg(img):
    if len(imgdic)>2:
        mask=an_element(imgdic)
        m=mask[:,:,0]
        m[m>0.5]=1.
        m[m<1]=0.
        for i in range(3):
            mask[:,:,i]=m
        dimgs=[]
        for i in range(2):
            a=bound_value(q*rndn(),-1,1)
            dimgs.append(a*an_element(imgdic))
        new_img=1*img
        new_img+=mask*dimgs[0]
        new_img+=(1-mask)*dimgs[1]
        #sh(mask,2)
    else:
        new_img=img

    print(len(imgdic))
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
