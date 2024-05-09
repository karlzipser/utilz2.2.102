#!/usr/bin/env python3

from utilz2 import *


if __name__ == '__main__':
    print('\n\n\n\n\n',__file__)

    args=getparser(
        path=os.getcwd(),
        file_types='jpg,jpeg,JPG,JPEG,png,PNG',
        shuffle=False,
        delay=1,
        loop=True,
        x=5,
        y=5,
        most_recent='',
    )

    gd=args.__dict__


    def process_gd():
        if gd['most_recent']:
            gd['path_most_recent']=most_recent_file_in_folder(gd['path'],[gd['most_recent']])
            assert(os.path.isdir(gd['path_most_recent']))
        else:
            gd['path_most_recent']=None
        gd['file_types_split'] = gd['file_types'].split(',')
        img_paths=[]
        for f in gd['file_types_split']:
            #img_paths += sggo(p,'*.'+f)
            if gd['path_most_recent']:
                p=gd['path_most_recent']
            else:
                p=gd['path']
            img_paths += find_files(start=p,patterns=['*.'+f],recursive=False,noisy=False)
        if gd['shuffle']:
            np.random.shuffle(img_paths)
        return img_paths


    
    

    #img_dic={}
    figure(1,figsize=(gd['x'],gd['y']))
    while True:
        kprint(gd, title='command_line_args')
        img_paths=process_gd()
        print('\n\nSlideshow with of',gd['path'],'with',len(img_paths),'images . . .',time.time())
        for f in img_paths:
            #img_dic[f]=rimread(f)
            sh(rimread(f),title=f,e=0)
            time.sleep(gd['delay'])
        if not gd['loop']:
            break

            

#EOF
