from utilz2 import *

args=dict(
    img_path='',
    mask_path='',
    category_name='',
    winx=0,
    winy=0,
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

img = zimread(p.img_path)
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
img[img>=250] = 250
img[img<=5] = 5


cv2.namedWindow(p.category_name)
cv2.moveWindow(p.category_name, p.winx,p.winy)
cv2.setMouseCallback(p.category_name, mouse_callback)
#cv2.setWindowProperty(p.category_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#cv2.setWindowProperty(p.category_name, cv2.WND_PROP_VISIBLE, cv2.WINDOW_NORMAL)

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

    cv2.putText(img_with_time,fname(p.img_path)+'  '+str(int(timer.time())), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        thickness,
        lineType)
    cv2.imshow(p.category_name, img_with_time)
    cv2.imshow(p.category_name,img_with_time)
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
        img[img<255] = 0
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

imsave( p.mask_path, img )




    
