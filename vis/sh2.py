
from utilz2.vis.sh_ import *


def menu(d):

    ctr2kys={}
    kys2ctr={}
    selected={}
    ctr=0
    for i in range(ord('0'),ord('9')+1):
        ctr2kys[ctr]=chr(i)
        kys2ctr[chr(i)]=ctr
        ctr+=1
    for i in range(ord('A'),ord('Z')+1):
        ctr2kys[ctr]=chr(i)
        kys2ctr[chr(i)]=ctr
        ctr+=1
    for i in range(ord('a'),ord('z')+1):
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
            clp(ctr+1,k,star,'\t',fname(fs[ctr]),c)
            ctr+=1
        print("Press '`' to exit")

        displaydic={}
        for k in sorted(kys(selected)):
            
            i=kys2ctr[k]
            s=str(i)
            displaydic[s]=1*d[fs[i]]
            a=displaydic[s]
            u=max(iwidth(a)//100,1)
            if selected[k]:
                s=s+'+'
                a[:,-3*u:,:]=(255,0,0)
                a[:,:3*u,:]=(255,0,0)
                a[-3*u:,:,:]=(255,0,0)
                a[:3*u,:,:]=(255,0,0)
            if k==lastkey:
                a[:,-u:,:]=(0,255,0)
                a[:,:u,:]=(0,255,0)
                a[-u:,:,:]=(0,255,0)
                a[:u,:,:]=(0,255,0)
        sh(displaydic,titles_font_scale=1,e=0)
        spause()

        c=getch()

        if c=='`':
            break

        elif c in selected.keys():
            lastkey=c
            #selected[c]=not selected[c]

        elif c==']':
            i=kys2ctr[lastkey]+1
            if i in ctr2kys and i < numkys:
                lastkey=ctr2kys[i]

        elif c=='[':
            i=kys2ctr[lastkey]-1
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
    d=load_img_folder_to_dict(opjD('128sa/a'),maxnumfiles=8)
    selected,notselected=menu(d)
    kprint(selected,title='selected')
    kprint(notselected,title='notselected')




#EOF
