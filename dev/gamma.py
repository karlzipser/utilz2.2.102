from k3 import *
from skimage import exposure


def main():
    """s - save
    r - open r gamma, x axis
    g - open g gamma, y axis
    b - open b gamma, y axis
    R - lock r Gamma
    G - lock g gamma
    B - lock b gamma
    q - quit"""

    if '__file__' not in locals():
        __file__ = '__file__'
    Defaults = {
        ('src','path for image for gamma manipulation') : ('path_',''),
        ('dst','destination folder for gamma measurements') : ('path_',opjD()),
        'doc' : """
        s - save
        r - open r gamma, x axis
        g - open g gamma, y axis
        b - open b gamma, y axis
        R - lock r gamma
        G - lock g gamma
        B - lock b gamma
        q - quit"""
    }
    Defaults['src']='/Volumes/CalvaryLG Mexico 2022/sexy-frames/8A1BE4ED-6E2F-43D2-BD26-CB8EEBCF7FC3/0001.png'
    Defaults['dst']=opjD('temp')
    if False:#not interactive():
        A = get_Arguments2(Defaults,f=__file__)
        A['cmd_line_str'] = ' '.join(sys.argv[1:])
    else:
        A = Defaults
    A['_doc_'] = __doc__
    if not A['src']:
        A['src'] = select_file(path=opjh(), prompt='Select SRC image')[0]
    A['dst'] = opj(A['dst'],fnamene(A['src']))
    os_system('mkdir -p', A['dst'])

    cv2.namedWindow("src")
    cv2.setMouseCallback("src",z_track_mouse)

    q = 'src'
    img = zimread(A[q])
    A[q+'_img'] = img
    A[q+'_img_small'] = zresize(A[q+'_img'],0.25)
    mci(A[q+'_img_small'],title=q)


    _Mouse_['x_max'] = shape(A['src_img_small'])[1]
    _Mouse_['y_max'] = shape(A['src_img_small'])[0]
    spause()

    gamma_mode = ''
    M = _Mouse_
    while True:
        q = 'src'
        img = A[q+'_img_small']
        img_new = 0 * img
        if not M['gamma_lock'][0]:
            M['gamma'][0] = 1 +(M['x_proportion']-0.5)
        if not M['gamma_lock'][1]:
            if M['y_gamma_mode'] == 'gamma/g':
                M['gamma'][1] = 1 +(M['y_proportion']-0.5)
        if not M['gamma_lock'][2]:
            if M['y_gamma_mode'] == 'gamma/b':
                M['gamma'][2] = 1 +(M['y_proportion']-0.5)

        img_new[:,:,0] = exposure.adjust_gamma(img[:,:,0], M['gamma'][0] )
        img_new[:,:,1] = exposure.adjust_gamma(img[:,:,1], M['gamma'][1] )
        img_new[:,:,2] = exposure.adjust_gamma(img[:,:,2], M['gamma'][2] )

        k = mci(img_new,title=q)

        if k == ord('q'):
            break
        elif k == ord('R'):
            M['gamma_lock'][0] = 1
        elif k == ord('G'):
            M['gamma_lock'][1] = 1
        elif k == ord('B'):
            M['gamma_lock'][2] = 1
        elif k == ord('r'):
            M['gamma_lock'][0] = 0
        elif k == ord('g'):
            M['gamma_lock'][1] = 0
            M['y_gamma_mode'] = 'gamma/g'
        elif k == ord('b'):
            M['gamma_lock'][2] = 0
            M['y_gamma_mode'] = 'gamma/b'
        elif k == ord('s'):
            f = opj(
                A['dst'],
                d2p(fnamene(A['src']),
                    '('+d2c(dp(M['gamma'][0]),dp(M['gamma'][1]),dp(M['gamma'][2]))+')',
                    'gamma'
                ))
            #so(f,M['gamma'])
            
            img_t = cv2.cvtColor(img_new, cv2.COLOR_BGR2RGB)
            imsave(f+'.jpg',img_t)
            cg('Saved gamma to',f)
            time.sleep(1)
        if 'x' in _Mouse_ and _Mouse_['change']:
            clear_screen()
            kprint(_Mouse_,'_Mouse_')
            time.sleep(0.01)

_Mouse_ = {
    'x' : 0,
    'y' : 0,
    'x_prev' : 0,
    'y_prev' : 0,
    'x_max' : 0,
    'y_max' : 0,
    'x_proportion' : 0,
    'y_proportion' : 0,
    'dx' : 0,
    'dy' : 0,
    'x_temp_center' : 0,
    'y_temp_center' : 0,
    'x_temp_center_proportion' : 0,
    'y_temp_center_proportion' : 0,
    'change' : False,
    'gamma' : [1.,1.,1.],
    'gamma_lock' : [0,0,0],
    'y_gamma_mode' : 'gamma/g',
}

def z_track_mouse(event,x,y,flags,param):
    M = _Mouse_
    M['x'],M['y'] = x,y
    M['dx'] = M['x'] - M['x_prev']
    M['dy'] = M['y'] - M['y_prev']
    if M['dx'] != 0 or M['dy'] != 0:
        M['change'] = True
        if M['x_max'] > 1 and M['y_max'] > 1:
            M['x_proportion'] = M['x'] / (M['x_max']-1)
            M['y_proportion'] = M['y'] / (M['y_max']-1)
            if M['x_temp_center'] > 0:
                M['x_temp_center_proportion'] = (M['x']-M['x_temp_center']) / (M['x_max']-M['x_temp_center'])
            if M['y_temp_center'] > 0:
                M['y_temp_center_proportion'] = (M['y']-M['y_temp_center']) / (M['y_max']-M['y_temp_center'])
    else:
        M['change'] = False
    M['x_prev'] = M['x']
    M['y_prev'] = M['y']



def get_gammas_from_img_names(path):
    fs = sggo(path,'*.gamma.*')
    kprint(fs)
    gs = []
    for f in fs:
        a = f.split('(')[1].split(')')[0]
        print(a)
        b = a.split(',')
        c = []
        for d in b:
            c.append(float(d))
        gs.append(tuple(c))
    gs = list(set(gs))
    return gs



def apply_gamma_to_imgs(path,gamma):
    
    fs = sggo(path,'*.*')
    for f in fs:
        if exname(f) in IMAGE_EXTENSIONS:
            img = zimread(f)
            for i in range(3):
                img[:,:,i] = exposure.adjust_gamma(img[:,:,i], gamma[i] )
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            p = opj(d2n(path,'-',str(gamma).replace(' ','')),fname(f))
            #p = opj(d2n(path,'-'),fname(f))
            os_system('mkdir -p',qtd(pname(p)),e=1)
            cy(p)
            mi(img)
            spause()
            raw_enter()
            imsave(p,img)
        else:
            print(f,'is not image')


if __name__ == '__main__':
    main()




#EOF
