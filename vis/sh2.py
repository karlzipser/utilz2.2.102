
from utilz2.vis.sh_ import *



def imagemenu(d):
    showtime=3
    timer=Timer(showtime)
    ctr2kys={}
    kys2ctr={}
    selected={}
    ctr=0
    for i in range(ord('0'),ord('9')+1):
        ctr2kys[ctr]=chr(i)
        kys2ctr[chr(i)]=ctr
        ctr+=1
    for i in range(ord('a'),ord('z')+1):
        ctr2kys[ctr]=chr(i)
        kys2ctr[chr(i)]=ctr
        ctr+=1
    for i in range(ord('A'),ord('Z')+1):
        ctr2kys[ctr]=chr(i)
        kys2ctr[chr(i)]=ctr
        ctr+=1


    fs=kys(d)

    numkys = len(fs)
    if numkys>len(kys2ctr):
        cE('Warning, numkys>len(ks)')
        numkys=len(kys2ctr)

    for k in kys(kys2ctr)[:numkys]:
        selected[k]=False

    lastkey='0'

    while True:
        
        clear_screen()

        assert lastkey in selected

        ctr=0
        for k in selected.keys():
            if k==lastkey:
                star='*'
            else:
                star=''
            #print(k,selected[k],star,'\t',fs[ctr])
            if selected[k]:
                c='`--b'
            else:
                c='`---'
            clp(k,star,'\t',fname(fs[ctr]),c,ctr+1,'`m--')
            ctr+=1
        print("Press '`' to exit")

        displaydic={}
        for k in kys(selected):
            
            i=kys2ctr[k]
            s=ctr2kys[i]
            displaydic[s]=1*d[fs[i]]
            a=displaydic[s]
            u=max(iwidth(a)//100,1)
            if selected[k]:
                a[:,-3*u:,:]=(255,0,0)
                a[:,:3*u,:]=(255,0,0)
                a[-3*u:,:,:]=(255,0,0)
                a[:3*u,:,:]=(255,0,0)
            if k==lastkey:
                a[:,-u:,:]=(0,255,0)
                a[:,:u,:]=(0,255,0)
                a[-u:,:,:]=(0,255,0)
                a[:u,:,:]=(0,255,0)
        shc(displaydic,titles_font_scale=1,e=0,figsize=15)
        spause()

        c=getch()

        if c=='`':
            break

        elif c in selected.keys():
            lastkey=c

        elif c==']':
            i=kys2ctr[lastkey]+1
            if i in ctr2kys and i < numkys:
                lastkey=ctr2kys[i]

        elif c=='[':
            i=kys2ctr[lastkey]-1
            if i in ctr2kys:
                lastkey=ctr2kys[i]

        elif c=='}':
            i=kys2ctr[lastkey]+int(np.ceil(sqrt(len(fs))))
            if i in ctr2kys and i < numkys:
                lastkey=ctr2kys[i]

        elif c=='{':
            i=kys2ctr[lastkey]-int(np.ceil(sqrt(len(fs))))
            if i in ctr2kys:
                lastkey=ctr2kys[i]

        elif c==' ':
            selected[lastkey]=not selected[lastkey]

    selectedfs=[]
    for k in selected:
        if selected[k]:
            selectedfs.append(fs[kys2ctr[k]])
    return selectedfs,list(set(fs)-set(selectedfs))




if __name__ == '__main__':
    eg(__file__)

    _d=load_img_folder_to_dict(opjD('j-and-k-to-12-12-2023/IMG_0423'))#opjh('samimgs'))#opjD('j-and-k-to-12-12-2023/IMG_0423'))
    side=np.ceil(sqrt(len(_d)))
    windowsize=int(0.8*min(SCREEN_RESOLUTION))
    maxwidth=intr(windowsize/side)
    d={}
    for k in _d:
        d[k]=resize_to_extent(_d[k][:,:,:3],maxwidth)
    selected,notselected=imagemenu(d)
    kprint(selected,title='selected')
    kprint(notselected,title='notselected')




#EOF
