from utilz import *

def select_imgs( path_with_pattern, moved_name='moved' ):
    #fs = sggo(opjD('itc-2023-unified/boats/processed/masks/rgb_rc0/*.*'))
    fs = sggo(path_with_pattern)
    dst = pname(fs[0])+'--'+moved_name
    mkdirp(dst)
    fx = fix_bgr
    total = 0
    selected = 0
    for f in fs:
        
        total += 1
        while True:
            w = fx(imread(f))
            k = mci(w,delay=120)
            if k & 0xFF == ord('q'):
                os.sys.exit()
            if k & 0xFF == ord('u'):
                #os_system('mv',qtd(f_moved),qtd(opj(dst,fname(f))),a=1,e=1)
                break
            elif k & 0xFF == ord(' '):
                print('selected')
                selected += 1
                break
            elif k & 0xFF == 127: #backspace
                print('move')
                f_moved = f
                os_system('mv',qtd(f),qtd(opj(dst,fname(f))),a=1,e=1)
                break
        print( total, selected, f )


def retrieve_masks( mask_folder_list ):
    d = {}
    for m in mask_folder_list:
        fs = sggo(m,'*.*')
        for f in fs:
            n = fname(f)
            if n not in d:
                d[n] = f
    return d



if __name__ == '__main__':
    d = retrieve_masks( [
            opjD('itc-2023-unified/boats/processed/masks/rgb_rc2rc3'),
            opjD('itc-2023-unified/boats/processed/masks/rgb_rc1rc2'),
            opjD('itc-2023-unified/boats/processed/masks/rgb_rc0'),
        ])


#EOF
