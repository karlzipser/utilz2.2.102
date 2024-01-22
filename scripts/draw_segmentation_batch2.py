from utilz2 import *

args=dict(
    category='',
    imgfolder='',
    maskfolder='',
    winx=0,
    winy=0,
    shuffle=False,
)
p=getparser(**args)


def batch():

    src_rgb_path = p.imgfolder
    mask_path = p.maskfolder
    mkdirp( mask_path )

    fs = sggo(src_rgb_path,'*.*')
    kprint(fs)
    if p.shuffle:
        np.random.shuffle(fs)
    ms = sggo(mask_path,'*.*')

    md = {}
    for m in ms:
        md[fname(m)] = m


    print(len(fs),'files to process')
    for f in fs:
        if fname(f) in md:
            cr('***',fname(f),'already processed.')
            continue
        print(f)

        l = [
            'python3',
            opjh('utilz2/scripts/draw_segmentation-with-line2.py'),
            '--img_path', f,
            '--mask_path', opj(mask_path,fname(f)),
            '--category_name', p.category,
        ]
        cg(' '.join(l))
        subprocess.run(
            l,
            check=True
        )

    print('Done.')
    os_system('say done')

if __name__=='__main__':
    batch()

#EOF

if False:
    fs=sggo('/Volumes/disk/JPEM_2023-12-21-08-31-50/*.npy')
    mkdirp(opjD('JPEM_2023-12-21-08-31-50/pngs'))
    for i in range(0,len(fs),10):#f in fs:
        f=fs[i]
        print(f)
        p=pname(f).replace('npy','png')
        n=np.load(f)
        rimsave(opjD('JPEM_2023-12-21-08-31-50/pngs',fnamene(f)+'.png'),fx(n))

