#!/usr/bin/env python3

from utilz2 import *


if __name__ == '__main__':
    print('\n\n\n\n\n',__file__)

    args=getparser(
        path=os.getcwd(),
        file_types='jpg,jpeg,JPG,JPEG,png,PNG',
        extent=256,
        shuffle=True,
        delay=1,
        loop=True,
    )

    gd=args.__dict__

    gd['file_types'] = gd['file_types'].split(',')

    img_paths=[]
    for f in gd['file_types']:
        #img_paths += sggo(p,'*.'+f)
        img_paths += find_files(start=gd['path'],patterns=['*.'+f],recursive=False,noisy=True)

    if gd['shuffle']:
        np.random.shuffle(img_paths)

    kprint(gd, title='command_line_args')

    #kprint(img_paths)

    print('\n\nSlideshow with',len(img_paths),'images . . .')

    img_dic={}

    while True:
        for f in img_paths:
            img_dic[f]=rimread(f)
            sh(img_dic[f],title=fname(f),e=0)
            time.sleep(gd['delay'])
        if not gd['loop']:
            break

#EOF
