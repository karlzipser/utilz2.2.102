if False:
    jpegs=find_files(
        start='/home/karl/Desktop/temp-location/Data/trips',
        patterns=['*.jpeg'],
        recursive=True,
        noisy=True
    )
    for i in rlen(jpegs):
        jpegs[i]=jpegs[i].replace('/home/karl/Desktop/temp-location/','')
    so(opjD('data/mm/jpegs-list-5-24-2024.pkl'),jpegs)

    bloscs=find_files(
        start='/home/karl/Desktop/temp-location/Data/mm',
        patterns=['*.blosc'],
        recursive=True,
        noisy=True
    )
    for i in rlen(bloscs):
        bloscs[i]=bloscs[i].replace('/home/karl/Desktop/temp-location/','')
    # so(opjD('data/mm/bloscs-list-5-24-2024.pkl'),bloscs)

if False:
    jpegs=lo('/home/karl/Desktop/data/mm/jpegs-list-5-24-2024.pkl' )
    bloscs=lo('/home/karl/Desktop/data/mm/bloscs-list-5-24-2024.pkl' )



if False:
    traintxt='/home/karl/Desktop/data/data_san_jose_entron_train_30_04_6cams_turns_fwd_center_x3.txt'
    trainllines=txt_file_to_list_of_strings(traintxt)
    jpegbloscdic={}
    for l in trainllines:
        a=l.split(',')
        j=a[0]
        b=a[1]
        jpegbloscdic[j]=b


def get_blosc_pairing(jpeg,jpegbloscdic):
    k=opj('/home/',jpeg)
    cy(k)
    if k in jpegbloscdic:
        blosc=jpegbloscdic[k]
        return blosc.replace('/home/','')
    else:
        return ''

if False:
    JB={}
    for j in jpegs:
        b=get_blosc_pairing(j,jpegbloscdic)
        if b:
            JB[j]=b
            cg(j,'paired')
        else:
            cr(j,'unpaired')
    so(opjD('data/mm/JB.pkl'),JB)




    
#EOF
