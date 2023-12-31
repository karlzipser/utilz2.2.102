from utilz import *

#g7 7qg7 4g q(sys.argv)

if len(sys.argv) != 5:
    print("Usage: python click_segmentation.py <img_path> <mask_path> <category_name> <width>")
    sys.exit(1)
img_path =  sys.argv[1]
mask_path =  sys.argv[2]
category_name = sys.argv[3]
width = int(sys.argv[4])
view_size = 2048
timer = Timer(20)

#print( img_path, _path, category_name, width )
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
drawing = False # true if mouse is pressed
mode = False # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
last_x,last_y=None,None
red = True
dofill = False
clr = 'red'
brush_size = 5*3
mult = 1

# mouse callback function
def mouse_callback(event,x,y,flags,param):
    global ix,iy,drawing,mode,dofill,last_x,last_y,brush_size
    if event == cv2.EVENT_LBUTTONDOWN:
        ix,iy = x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True and not dofill:
            if clr == 'red':
                c = (0,0,255)
            elif clr == 'green':
                c = (0,255,0)
            elif clr == 'black':
                c = (0,0,0)
            if not isNone(last_x):
                print(last_x,last_y,x,y)
                cv2.line(img,(last_x,last_y),(x,y),c,brush_size)
            last_x=x;last_y=y
            cv2.circle(img,(x,y),brush_size,c,-1)
    elif event == cv2.EVENT_LBUTTONUP:
        if dofill:
            if clr == 'red':
                c = (50,50,128)
            elif clr == 'green':
                c = (50,128,50)
            elif clr == 'black':
                c = (0,0,0)
            cv2.floodFill(img, None, (x,y), c)
            dofill = False


def put_image_into_square(img,width):
    img = resize_to_extent(img, width, interpolation=3)
    sq = np.zeros((width, width, 3), np.uint8) + 128
    h,w,_ = shape(img)
    if w == width and h == width:
        b = img
    elif w == width:
        sq[width//2-h//2:width//2+h-+h//2,:,:] = img
        b = sq
    else:
        sq[:,width//2-w//2:width//2+w-w//2,:] = img
        b = sq
    return b

img = zimread(img_path)
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
img[img>=250] = 250
img[img<=5] = 5
img = put_image_into_square(img,width)
img = cv2.resize(img, (view_size, view_size))
rgb = 1*img

cv2.namedWindow(category_name)
cv2.moveWindow(category_name, 200,200)
cv2.setMouseCallback(category_name, mouse_callback)

while False:#True:
    if timer.rcheck():
        beep()
    cv2.imshow(category_name, img)
    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (30,70)
fontScale              = 2
fontColor              = (255,0,0)
thickness              = 2
lineType               = 2

first_key = False

timer = Timer()
while True:
    img_with_time = 1*img

    cv2.putText(img_with_time,fname(img_path)+'  '+str(int(timer.time())), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        thickness,
        lineType)
    cv2.imshow(category_name, img_with_time)
    cv2.imshow(category_name,img_with_time)
    k = cv2.waitKey(1) & 0xFF

    if k == ord('m'):
        mode = not mode
    elif k == ord(' '):
        last_x = None
        drawing = not drawing
    elif k == ord('r'):
        clr = 'red'
    elif k == ord('g'):
        if not first_key:
            first_key = True
            os_system('say green')
        clr = 'green'
    elif k == ord('b'):
        clr = 'black'
    elif k == ord('t'):
        img[img<255] = 0
    elif k == ord('f'):
        dofill = True
    elif k == ord('q'):
        sys.exit()
    elif k == ord('s'):
        break
    elif k == ord('1'):
        brush_size = 1*mult       
    elif k == ord('2'):
        brush_size = 2*mult       
    elif k == ord('3'):
        brush_size = 3*mult       
    elif k == ord('4'):
        brush_size = 4*mult       
    elif k == ord('5'):
        brush_size = 5*mult       
    elif k == ord('6'):
        brush_size = 6*mult       
    elif k == ord('7'):
        brush_size = 7*mult       
    elif k == ord('8'):
        brush_size = 8*mult       
    elif k == ord('9'):
        brush_size = 9*mult       

    elif k == 27:
        break


cv2.destroyAllWindows()
t = int(timer.time())
print(t,'s')
os_system('say',t,'seconds')

mask = cv2.resize(img, (width, width))
imsave( mask_path, mask )




    

def batch(category_name='rhib-wake-hard-mask'):
    category_name='rhib-wake-hard-mask'
    #src_rgb_path = opjD('itc-2023-unified/boats/processed/rgb-all')
    src_rgb_path = opjD('itc-2023-unified/boats/processed/rgb-hard')
    #mask_path = opjD('itc-2023-unified/boats/processed/',category_name)
    mask_path = opjD('itc-2023-unified/boats/processed/rhib-wake-hard-mask')#,category_name)
    mkdirp( mask_path )

    fs = sggo(src_rgb_path,'*.*')
    ms = sggo(mask_path,'*.*')
    #cm(ms)
    md = {}
    for m in ms:
        md[fname(m)] = m
    #kprint(md)

    print(len(fs),'files to process')
    for f in fs:
        if fname(f) in md:
            cr('***',fname(f),'already processed.')
            continue
        print(f)

        l = [
                    'python3',
                    'k3/misc/ger/utils/draw_segmentation-with-line.py',
                    f,
                    opj(mask_path,fname(f)),
                    category_name,
                    '512',
                ]
        cg(' '.join(l))
        cb(l)
        subprocess.run(
            l,
            check=True
        )

    print('Done.')
    os_system('say done')


if False:
    category_name='rhib-wake-hard-mask'
    mask_path = opjD('itc-2023-unified/boats/processed/',category_name)
    dst_path = mask_path.replace(category_name,category_name+'-1024')
    mkdirp(dst_path)
    ms = sggo(mask_path,'*.*')
    a1024 = get_blank_rgb(1024,1024)
    for m in ms:
        img = imread(m)
        a1024 *= 0
        a1024[255:255+512,255:255+512,:]=img
        imsave(opj(dst_path,fname(m)),a1024)
        #raw_enter()
