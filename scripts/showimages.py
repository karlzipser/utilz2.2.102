#!/usr/bin/env python3

from utilz2 import *
from pathlib import Path

sys.setrecursionlimit(999*10)

def getparser( **argdic ):
    if interactive():
        return kws2class(**argdic)
    parser = argparse.ArgumentParser(description='Argument Parser')
    for k in argdic:
        if len(k)>1:
            s='--'
        else:
            s='-'
        parser.add_argument(s+k,type=type(argdic[k]),default=argdic[k])
    return parser.parse_args()





def get_list_of_img_data( gd ):

    timer = Timer(5)
    img_paths = []

    for p in gd['paths']:
        for f in gd['file_types']:
            #img_paths += sggo(p,'*.'+f)
            img_paths += find_files(start=p,patterns=['*.'+f],recursive=gd['recursive'],noisy=True)
    if len(img_paths) > gd['max_num_images']:
        img_paths = img_paths[:gd['max_num_images']]


    blank = zeros((gd['extent'],gd['extent'],3),np.uint8)

    gd['list_of_img_data'] = []
    gd['img_buffer'] = {}
    i = 0
    for p in img_paths:
        i += 1
        if i < gd['offset_image']:
            continue
        cm('reading',p,i,'of',len(img_paths))
        if gd['verbose']:
            print('Loading',p)
        q = Path(p).resolve().as_posix()
        img = zimread(q)
        gd['img_buffer'][q] = img
        img = resize_to_extent( img, gd['extent'] )
        img_data = {
            'file':q,
            'extent':gd['extent'],
            'square_embeding':None,
            'corner_x':0,
            'corner_y':0,
            }

        h,w,d = shape(img)
        blank = 0 * blank + gd['padval']
        e2 = gd['extent']//2
        blank[
            e2-h//2 : e2-h//2+h,
            e2-w//2 : e2-w//2+w,
            :d,
        ] = img
        img_data['square_embeding'] = blank

        gd['list_of_img_data'].append( img_data )

        if timer.rcheck():
            make_bkg_image( gd )
    print('done reading images')








def _mi( gd ):
    fig_name = d2s(*gd['paths'])
    if 'fig' not in gd:
        gd['fig'] = figure(fig_name,facecolor="0.0")
        #print(gd['paths'])
        
    mi(gd['bkg_image'],fig_name)
    gd['fig'].tight_layout(pad=0)
    spause()



def make_bkg_image( gd ):
    gd['cols'] = int(gd['rcratio']*sqrt(len(gd['list_of_img_data'])))
    padsize = gd['padsize']
    min_x = 10**9
    min_y = 10**9
    max_x = 0
    max_y = 0
    rows,cols = 0,0

    if not len(gd['list_of_img_data']):
        print('\n\n\n\nNo image data!')
        return 0

    for I in gd['list_of_img_data']:
        I['corner_x'] = cols * (gd['extent'] + padsize)
        I['corner_y'] = rows * (gd['extent'] + padsize)
        min_x = min(I['corner_x'],min_x)
        min_y = min(I['corner_y'],min_y)
        max_x = max(I['corner_x']+gd['extent'],max_x)
        max_y = max(I['corner_y']+gd['extent'],max_y)
        if cols < gd['cols']-1:
            cols += 1
        else:
            rows += 1
            cols = 0

    bkg = zeros((max_y+2*padsize,max_x+2*padsize,3),np.uint8) + gd['padval']
    for I in gd['list_of_img_data']:
        bkg[
            I['corner_y']+padsize:I['corner_y']+padsize+gd['extent'],
            I['corner_x']+padsize:I['corner_x']+padsize+gd['extent'],:] =\
            I['square_embeding']

    gd['bkg_image'] = bkg
    _mi( gd )
    return True




def handle_events(event):

    time.sleep(0.01) # needed to allow main tread time to run

    x, y, k = event.xdata, event.ydata, event.key
    
    if k == 'q':
        cv2.destroyAllWindows()
        CA()
        sys.exit()

    if x is None:
        return

    padsize = gd['padsize']

    if 'list_of_img_data' in gd:
        for I in gd['list_of_img_data']:
            if y >= I['corner_y']+padsize:
                if y <= I['corner_y']+padsize+gd['extent']:
                    if x >= I['corner_x']+padsize:
                        if x <= I['corner_x']+padsize+gd['extent']:
                            s = I['file'].replace(opjh(),'')
                            
                            if gd['verbose'] and s != gd['last_printed']:
                                print('\n'+qtd(s))
                                gd['last_printed'] = s
                            img = resize_to_extent(
                                    gd['img_buffer'][I['file']],
                                    gd['extent2'],
                                )
                            q = zeros((gd['image_info_area_height'],shape(img)[1],3),np.uint8)
                            imgq = np.concatenate((img,q),axis=0) 
                            fontsize = 0.4
                            cv2.putText(
                                imgq,
                                pname(s)+'/',
                                (10,shape(imgq)[0]-30),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                fontsize,
                                (150,150,150),
                                1,
                                cv2.LINE_AA
                            )
                            cv2.putText(
                                imgq,
                                fname(s),
                                (10,shape(imgq)[0]-10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                fontsize,#.3,
                                (150,150,150),
                                1,
                                cv2.LINE_AA
                            )                                
                            mci(
                                imgq,
                                title='mci'
                            )
                            return



if __name__ == '__main__':
    print('\n\n\n\n\n',__file__)

    args=getparser(
        paths=opjD(),
        recursive=False,
        file_types='jpg,jpeg,JPG,JPEG,png,PNG',
        extent=256,
        extent2=512,
        padval=0,
        padsize=5,
        rcratio=1.1,
        image_info_area_height=100,
        verbose=False,
        max_num_images=10*10,
        offset_image=0,
        )

    gd=args.__dict__

    gd['paths'] = gd['paths'].split(',')

    gd['file_types'] = gd['file_types'].split(',')

    gd['last_printed'] = ''


    kprint(gd, title='command_line_args')
    get_list_of_img_data( gd )
    if not make_bkg_image( gd ):
        pass
    else:
        cid0 = gd['fig'].canvas.mpl_connect('key_press_event', handle_events)
        cid1 = gd['fig'].canvas.mpl_connect('button_press_event', handle_events)
        cid2 = gd['fig'].canvas.mpl_connect('motion_notify_event', handle_events)
        plt.pause(10**9)
        raw_input()

#EOF
