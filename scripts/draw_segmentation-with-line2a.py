from utilz2 import *

args=dict(
    imgfolder='',
    maskfolder='',
    shuffle=False,
    category_name='test',
    winx=200,
    winy=0,
    drawing= False, # true if mouse is pressed
    mode= False, # if True, draw rectangle. Press 'm' to toggle to curve
    red= True,
    dofill= False,
    clr= 'red',
    brush_size= 21,
    mult= 3,
    font=1,
    bottomLeftCornerOfText= (30,70),
    fontScale=2,
    fontColor= (255,0,0),
    thickness= 2,
    lineType= 2,
)
p=getparser(**args)

print("""

draw_segmentation.py

    ▪   R - set to red
    ▪   G - set to green3g3
    ▪   B - set to black
    ▪   1,2,3…9 set brush size
    ▪   <space> - turn drawing on/off
    ▪   T - threshold to set real image to black
    ▪   F - put in fill mode, fill once on next click
    ▪   S - save and quit
    ▪   Q - quit without save

Instructions:

    ▪   Select a good brush size
    ▪   Draw wake outline first (with green)
    ▪   Draw boat outline second (with red)
    ▪   Press T
    ▪   Press R
    ▪   Press F
    ▪   Click in center of boat to fill
    ▪   Press G
    ▪   press F
    ▪   Click in center of wake to fill
    ▪   Press S
""")



p.ix=-1
p.iy = -1
p.last_x=None
p.last_y=None




p.first_key = False
p.timer = Timer()

# mouse callback function
def mouse_callback(event,x,y,flags,p):
    #global ix,iy,drawing,mode,dofill,last_x,last_y,brush_size
    if p.clr == 'red':
        c = (0,0,255)
    elif p.clr == 'green':
        c = (0,255,0)
    elif p.clr == 'blue':
        c = (255,0,0)
    if event == cv2.EVENT_LBUTTONDOWN:
        p.ix,p.iy = x,y
        print(x,y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if p.drawing == True and not p.dofill:
            if not isNone(p.last_x):
                print(p.last_x,p.last_y,x,y)
                cv2.line(p.img,(p.last_x,p.last_y),(x,y),c,p.brush_size)
            p.last_x=x;p.last_y=y
            cv2.circle(p.img,(x,y),p.brush_size,c,-1)
    elif event == cv2.EVENT_LBUTTONUP:
        cv2.circle(p.img,(x,y),p.brush_size,c,-1)




#cv2.setWindowProperty(p.category_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#cv2.setWindowProperty(p.category_name, cv2.WND_PROP_VISIBLE, cv2.WINDOW_NORMAL)



def annotate(p):
    cv2.namedWindow(p.category_name)
    cv2.moveWindow(p.category_name, p.winx,p.winy)
    cv2.setMouseCallback(p.category_name, mouse_callback,p)
    p.drawing=False

    while True:
        p.img_with_time = 1*p.img

        cv2.putText(p.img_with_time,fname(p.img_path)+'  '+str(int(p.timer.time())), 
            p.bottomLeftCornerOfText, 
            p.font, 
            p.fontScale,
            p.fontColor,
            p.thickness,
            p.lineType)
        cv2.imshow(p.category_name, p.img_with_time)
        cv2.imshow(p.category_name,p.img_with_time)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('m'):
            p.mode = not p.mode
        elif k == ord(' '):
            p.last_x = None
            p.drawing = not p.drawing
        elif k == ord('r'):
            clr = 'red'
        elif k == ord('g'):
            if not p.first_key:
                p.first_key = True
                os_system('say green')
            p.clr = 'green'
        elif k == ord('b'):
            p.clr = 'blue'
        elif k == ord('t'):
            p.img[p.img<255] = 0
        elif k == ord('f'):
            p.dofill = True
        elif k == ord('q'):
            cE('Return without saving.')
            return
        elif k == ord('x'):
            cE('Exiting without saving.')
            sys.exit()
        elif k == ord('s'):
            #p.img[p.img<255] = 0
            break
        elif k == ord('1'):
            p.brush_size = 1*p.mult       
        elif k == ord('2'):
            p.brush_size = 2*p.mult       
        elif k == ord('3'):
            p.brush_size = 3*p.mult       
        elif k == ord('4'):
            p.brush_size = 4*p.mult       
        elif k == ord('5'):
            p.brush_size = 5*p.mult       
        elif k == ord('6'):
            p.brush_size = 6*p.mult       
        elif k == ord('7'):
            p.brush_size = 7*p.mult       
        elif k == ord('8'):
            p.brush_size = 8*p.mult       
        elif k == ord('9'):
            p.brush_size = 9*p.mult       

        elif k == 27:
            break


    cv2.destroyAllWindows()
    t = int(p.timer.time())
    print(t,'s')
    os_system('say',t,'seconds')

    imsave( p.mask_path, p.img )





def batch(p):

    src_rgb_path = p.imgfolder

    mkdirp( p.maskfolder )

    fs = sggo(src_rgb_path,'*.*')
    kprint(fs)
    if p.shuffle:
        np.random.shuffle(fs)
    ms = sggo(p.maskfolder,'*.*')

    md = {}
    for m in ms:
        md[fname(m)] = m


    print(len(fs),'files to process')
    for f in fs:
        if fname(f) in md:
            cr('***',fname(f),'already processed.')
            continue
        p.img_path=f
        p.mask_path=opj(p.maskfolder,fname(p.img_path))
        cg('Annotating',p.img_path)
        p.img = zimread(p.img_path)
        p.img = cv2.cvtColor(p.img,cv2.COLOR_BGR2RGB)
        p.img[p.img>=250] = 250
        p.img[p.img<=5] = 5
        annotate(p)

    print('Done.')
    os_system('say done')

if __name__=='__main__':
    batch(p)





#EOF

    
