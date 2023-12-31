#!/usr/bin/env python3

#from k3.utils.vis import *
#from k3.drafts.other.arguments0 import *

import argparse

parser = argparse.ArgumentParser(description='Argument Parser')

parser.add_argument('-f', type=str, default='', help='src path')

parser.add_argument('--dst', type=str, default='', help='dst path')

parser.add_argument('-e', type=int, default=0, help='extent')

parser.add_argument('-r', type=int, default=0, help='rotate (-90,0,90,180)')

parser.add_argument('--skip', type=int, default=3, help='frames to skip with multiframe select')

parser.add_argument('--load_skip_frames', type=int, default=100, help='frames to skip with loading')

parser.add_argument('--mem', type=int, default=95, help='max virtual memory percent')

parser.add_argument('--margin', type=int, default=0, help='blank margin around extent')

parser.add_argument('--folder', action='store_true', default=False, help='load images from folder')

parser.add_argument('-c', action='store_true', default=True, help='convert BGR to RGB for image files')

parser.add_argument('--last', action='store_true', default=False, help='use last folder selected interactively')

# Parse the command-line arguments
args = parser.parse_args()
#print(args,args.folder)

from utilz2 import *

"""
A = get_Arguments_dictionary(
    {
        ('f', 'filename')  : '',
        ('dst', 'destination folder') : opjD(),
        ('e','extent') : 0,
        ('r','rotate (-90,0,90,180)') : 0,
        ('c','convert BGR to RGB for image files') : True,
        ('folder','load images from folder') : False,
        ('mem','max virtual memory percent') : 95,
        ('last','use last folder selected interactively') : False,
        ('margin','blank margin around extent') : 0,
    },
    verbose=True,
    file=__file__,
)
"""

A = dict(
        f = args.f,
        dst = args.dst,
        e = args.e,
        r = args.r,
        skip = args.skip,
        mem = args.mem,
        margin = args.margin,
        c = args.c,
        folder = args.folder,
        last = args.last,
        load_skip_frames = args.load_skip_frames,
    )
#print(args.f)
kprint(A)
#input()
if A['last']:
    A['f'] = file_to_text(opjD('_last'))
    if os.path.isdir(A['f']):
        A['folder'] = True
elif not A['f']:
  if not A['folder']:
    A['f'] = select_file()[0]
    text_to_file(opjD('_last'),A['f'])
  else:
    A['f'] = select_folder()[0]
    text_to_file(opjD('_last'),A['f'])
if type(A['f']) is list:
    A['f'] = ' '.join(A['f'])
os_system('mkdir -p',A['dst'])

mouse_X,mouse_Y = 0,0
def z_track_mouse(event,x,y,flags,param):
    global mouse_X,mouse_Y
    mouse_X,mouse_Y = x,y

"""
mouse_X,mouse_Y = 0,0
def draw_circle(event,x,y,flags,param):
    global mouse_X,mouse_Y
    mouse_X,mouse_Y = x,y
"""

img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow("image")
"""
cv2.setMouseCallback("image",draw_circle)
"""
cv2.setMouseCallback("image",z_track_mouse)

if os.path.isdir(A['f']):
    vidcap = False
else:
    vidcap = cv2.VideoCapture(A['f'])
    success,image = vidcap.read()
count = 0
success = True
frames,fullsize,names = [],[],[]
loading = True
exiting = False

if A['r'] == -90:
    rot = cv2.ROTATE_90_COUNTERCLOCKWISE
elif A['r'] == 90:
    rot = cv2.ROTATE_90_CLOCKWISE
elif A['r'] == 180:
    rot = cv2.ROTATE_180
else:
    assert A['r'] == 0

def append_to_lists(image,name):
    if A['r']:
      image = cv2.rotate(image, rot)
    fullsize.append(image)
    if A['e']:
        image = resize_to_extent(image,A['e'])
    frames.append(image)
    names.append(name)
    print('   ',name,'       ',end='\r')

import threading
if vidcap:
    
    def loader():
        global success,count,loading,exiting
        while success:
            if exiting:
                break
            try:

                for i in range( A['load_skip_frames'] ):
                    success,image = vidcap.read()
                    count += 1
                    time.sleep(1/1000000.)
                print('loaded',count)
                append_to_lists(image,str(count))

            except KeyboardInterrupt:
                print('*** KeyboardInterrupt ***')
                sys.exit()
            except:
                print('loader exception')
        print('  Finished loading.',end='\r')
        loading = False
    
else:
    def loader():
        global success,count,loading,exiting
        fs = sggo(A['f'],'*.*')
        for f in fs:
            if exiting:
                break
            image = zimread(f)
            if A['c']:
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            append_to_lists(image,fname(f))
            count += 1
        print('  Finished loading.',end='\r')
        loading = False
threading.Thread(target=loader,).start()

while not len(frames):
    print('  waiting...',end='\r')
    time.sleep(0.1)

if not A['e']:
    width = shape(frames[0])[1]
else:
    width = A['e'] + 2*A['margin']

red = frames[0] * 0
red[:,:,0] = 64
red[:,:,1] = 64
red[:,:,2] = 98

x_,y_ = mouse_X,mouse_Y

saved = set()

mem_timer = Timer(5)

if True:#A['folder']:
    blank = zeros( (A['e']+2*A['margin'],A['e']+2*A['margin'],3), np.uint8)
else:
    s = shape(image)
    blank = zeros( (s[0]+2*A['margin'],A['e']+2*A['margin'],3), np.uint8)

#print(len(frames))
#print(type(frames[0]))
#mi(frames[0])
#cm(r=1)
while True:
    #if mem_timer.rcheck():
    #    print(memory())
    if memory() > A['mem']:
        exiting = True
        print('maximum memory surpassed',memory())
    i = int(mouse_X/A['load_skip_frames']/width * count)
    i_ = min(i,len(frames)-1)
    g = frames[i_]
    g_full = fullsize[i_]
    name = names[i_]
    if mouse_X != x_ or mouse_Y != y_:
        x_,y_ = mouse_X,mouse_Y
        #print(i)#,count,mouse_X,mouse_Y)
    try:
        print('frame',i_,end='\r')
        
        g = 1*g
        if loading:
            #g = 1*g
            g[0:5,:,:] = 0
            g[0:5,:,2] = 255
        if i in saved:
            g[:,0:20,:] = 0
            g[:,0:20,2] = 255   



        

        if A['margin']:
            e = A['e']
            blank = 0*blank
            h,w,_ = shape(g)
            assert(w) <= e
            assert(h) <= e
            a = e-w
            b = e-h
            m = A['margin']
            blank[m+b//2:m+b//2+h, m+a//2:m+a//2+w, :] = g
            g = blank



        cv2.putText(
            g,
            name,
            (10,shape(g)[0]-20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255,255,255),
            1,
            cv2.LINE_AA
        )  



        cv2.imshow("image",g)


    except:
        print("""cv2.imshow("image",g) failed""")




    k = cv2.waitKey(33)
    if k & 0xFF == ord("q"):
        exiting = True
        break
    elif k & 0xFF == ord(" "):
        cv2.imshow("image",red)
        cv2.waitKey(33)
        if False:
            imsave(opj(A['dst'],d2p(fname(A['f']),i,'jpg')),g_full)
            print('saved',i)
            saved.add(i)

        if True:
            k = min(i,len(frames)-1)
            g_full = fullsize[k]
            if A['folder']:
                n = names[k]
                #cm(k,names[k],r=1)
            else:
                n = d2p(fname(A['f']),i,'jpg')
                #cm(0,r=1)
            imsave(opj(A['dst'],n),g_full)
            saved.add(i)
            print('saved',n)

    elif k & 0xFF == ord("a"):
        
        for j in rlen(frames):
            k = j
            g_full = fullsize[k]
            if A['folder']:
                n = names[k]
            else:
                n = d2p(fname(A['f']),j,'jpg')
            if type(g_full) is not type(None):
                imsave(opj(A['dst'],n),g_full)
                saved.add(j)
                print('saved',n)

    elif chr(k & 0xFF) in ['2','3','4','5','6','7','8','9']:
        cv2.imshow("image",red)
        cv2.waitKey(33)
        for j in range(0,int(chr(k & 0xFF)),A['skip']):

            k = min(i+j,len(frames)-1)
            g_full = fullsize[k]
            if A['folder']:
                n = names[k]
                #cm(k,names[k],r=1)
            else:
                n = d2p(fname(A['f']),i+j,'jpg')
                #cm(0,r=1)
            imsave(opj(A['dst'],n),g_full)
            saved.add(i+j)
            print('saved',n)


    try:
        k = cv2.waitKey(33)
        if k & 0xFF == ord("q"):
            exiting = True
            break
        elif k & 0xFF == ord(" "):
            cv2.imshow("image",red)
            cv2.waitKey(33)
            if False:
                imsave(opj(A['dst'],d2p(fname(A['f']),i,'jpg')),g_full)
                print('saved',i)
                saved.add(i)

            if True:
                k = min(i,len(frames)-1)
                g_full = fullsize[k]
                if A['folder']:
                    n = names[k]
                    #cm(k,names[k],r=1)
                else:
                    n = d2p(fname(A['f']),i,'jpg')
                    #cm(0,r=1)
                imsave(opj(A['dst'],n),g_full)
                saved.add(i)
                print('saved',n)


        elif chr(k & 0xFF) in ['2','3','4','5','6','7','8','9']:
            cv2.imshow("image",red)
            cv2.waitKey(33)
            for j in range(0,int(chr(k & 0xFF)),A['skip']):

                k = min(i+j,len(frames)-1)
                g_full = fullsize[k]
                if A['folder']:
                    n = names[k]
                    #cm(k,names[k],r=1)
                else:
                    n = d2p(fname(A['f']),i+j,'jpg')
                    #cm(0,r=1)
                imsave(opj(A['dst'],n),g_full)
                saved.add(i+j)
                print('saved',n)
    except:
        print("""keyboard input failed""")

# add start and end options
cv2.destroyAllWindows()
print('           ',end='\r')
print()


#EOF
