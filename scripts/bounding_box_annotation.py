from utilz import *

#g7 7qg7 4g q(sys.argv)

if len(sys.argv) != 5:
    print("Usage: python click_segmentation.py <img_path> <mask_path> <category_name> <width>")
    sys.exit(1)

img_path =  sys.argv[1]
#rgb_path =  sys.argv[2]
mask_path =  sys.argv[2]
category_name = sys.argv[3]
width = int(sys.argv[4])
view_size = 2048
timer = Timer(20)
boxes = [[[110,110],[110,300]],[[0,0],[200,100]],[[1,0],[100,100]],[[100,100],[500,100]],]
box_colors = ((0,255,0),(255,0,0),(0,0,255),(255,255,255))
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
drawing = True # true if mouse is pressed
mode = False # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
red = True
dofill = False
clr = 'red'
brush_size = 5*3
on_upper_left = False
box_index = 0
# mouse callback function
def mouse_callback(event,x,y,flags,param):
    global ix,iy,drawing,mode,dofill,on_upper_left,boxes,box_index

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
            #img = 1*rgb
            #cv2.circle(img,(x,y),brush_size,c,-1)
            if on_upper_left:
                i = 0
            else:
                i = 1
            boxes[box_index][i] = (x,y)
             

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

    cv2.imshow(category_name, img)
    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (30,70)
fontScale              = 2
fontColor              = (0,0,0)
thickness              = 2
lineType               = 2

first_key = False

timer = Timer()
while True:
    img_with_time = 1*img
    img = 1*rgb
    for i in rlen(boxes):
        b,c = boxes[i],box_colors[i]
        ul,lr = b
        #print(ul,lr,shape(img))
        #cg(c)
        cv2.rectangle(img, ul, lr, c, 3)
    """
    if timer.time() > 20:
        thickness = 8
        fontColor              = (0,0,255)
    if timer.time() > 30:
        thickness = 16
    if timer.time() > 60:
        thickness = 32
        bottomLeftCornerOfText = (30,140)
        fontScale              = 4
    """
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
        on_upper_left = not on_upper_left
        #drawing = not drawing
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
        box_index = 0      
    elif k == ord('2'):
        box_index = 1        
    elif k == ord('3'):
        box_index = 2       
    elif k == ord('4'):
        box_index = 3        
    elif k == ord('5'):
        brush_size = 5*5       
    elif k == ord('6'):
        brush_size = 6*5       
    elif k == ord('7'):
        brush_size = 7*5       
    elif k == ord('8'):
        brush_size = 8*5       
    elif k == ord('9'):
        brush_size = 9*5       

    elif k == 27:
        break

#cv2.moveWindow('Image', x_position, y_position)

#cv2.imshow(category_name, img)


#mask = 1*img
#mask[mask<255] = 0
#mask01 = mask//255
#print('rgb masked')
#cv2.imshow(category_name, rgb*mask01)
#cv2.waitKey(0)

cv2.destroyAllWindows()
t = int(timer.time())
print(t,'s')
os_system('say',t,'seconds')

#rgb = cv2.cvtColor(rgb,cv2.COLOR_BGR2RGB)

#rgb,mask = click_segment_image( opjD('Unknown.jpeg'), 'vessel', width=512 )

#rgb = cv2.resize(rgb, (width, width))
mask = cv2.resize(img, (width, width))

f = mask_path.replace('.jpg','')
f =d2s(f,'{',shape(img),boxes)+'}.jpg'
imsave( f, mask )



def _batch2(v):
    category_name = 'rhib-wake-wide'
    src_path = opjD( 'itc-2023',v,'segs','rhib-wake','mask')
    rgb_path = opjD( 'itc-2023',v,'segs',category_name,'rgb')
    mask_path = opjD('itc-2023',v,'segs',category_name,'mask')
    for path in [rgb_path, mask_path]: 
        os_system('mkdir -p',path)

    fs = sggo(src_path,'*.jpg')
    print(len(fs))
    
    print(len(fs),'files to process')
    for f in fs:
        print(f)
        l = [
                    'python3',
                    'utilz/misc/draw_segmentation.py',
                    f,
                    opj(rgb_path,fname(f)),
                    opj(mask_path,fname(f)),
                    category_name,
                    '512',
                ]
        #print(f)
        subprocess.run(
            l,
            check=True
        )
    beep()
    print('Done.')
    os_system('say done')
    

def __batch(v):
    category_name = 'rhib-wake-box'
    rgb_path = opjD( 'itc-2023',v,'segs',category_name,'rgb')
    mask_path = opjD('itc-2023',v,'segs',category_name,'mask')
    for path in [rgb_path, mask_path]: 
        os_system('mkdir -p',path)

    fs = sggo(opjD('v'+v+'/*.jpg'))

    
    print(len(fs),'files to process')
    for f in fs:
        print(f)
        l = [
                    'python3',
                    'utilz/misc/bounding_box_annotation.py',
                    f,
                    opj(rgb_path,fname(f)),
                    opj(mask_path,fname(f)),
                    category_name,
                    '512',
                ]
        #print(f)
        subprocess.run(
            l,
            check=True
        )
    beep()
    print('Done.')
    os_system('say done')



def batch(category_name='box'):
     
    src_rgb_path = opjD('itc-2023-unified/boats/processed/rgb-all')
    mask_path = opjD('itc-2023-unified/boats/processed/',category_name)
    mkdirp( mask_path )

    fs = sggo(src_rgb_path,'*.*')
    ms = sggo(mask_path,'*.*')
    md = {}
    for m in ms:
        fm = m.split(' {')[0]+'.jpg'
        md[fname(fm)]=m
    kprint(md)
    print(len(fs),'files to process')
    for f in fs:
        cm(fname(f))
        if fname(f) in md:
            cr('***',fname(f),'already processed.')
            continue
        #print(f)

        l = [
                    'python3',
                    'k3/misc/ger/bounding_box_annotation.py',
                    f,
                    opj(mask_path,fname(f)),
                    category_name,
                    '512',
                ]
        cg(' '.join(l))
        subprocess.run(
            l,
            check=True
        )

    print('Done.')
    os_system('say done')

#EOF

