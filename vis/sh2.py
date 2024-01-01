

d=load_img_folder_to_dict(opjD('128sa/a'),maxnumfiles=35)



def somehow_get_a_key():
    return getch()




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

    if len(fs)>len(kys2ctr):
        cE('Warning, len(fs)>len(ks)')
        len(fs)=len(kys2ctr)

    for k in kys(kys2ctr)[:len(fs)]:
        selected[k]=False

    lastkey=kys(selected)[0]

    while True:

        displaydic={}

        for k in selected:


        assert lastkey in selected
        clear_screen()    

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
            clp(k,star,'\t',fs[ctr],c)#clp(k,star,'\t',fname(fs[ctr]),c)
            ctr+=1

        c=somehow_get_a_key()

        if c=='`':
            break

        elif c in selected.keys():
            lastkey=c
            selected[c]=not selected[c]

        elif c==']':
            i=kys2ctr[lastkey]+1
            if i in ctr2kys and i < len(fs):
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
    return selectedfs

s=menu()
kprint(s)




#EOF
