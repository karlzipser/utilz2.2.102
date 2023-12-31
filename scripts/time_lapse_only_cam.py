#!/usr/bin/env python3

from k3.utils import *
from k3.utils.vis import *
import datetime
#,tcamo.a
"""
python3 k3/scripts/gen/time_lapse_only_cam.py\
    --long 1.\
    --beep_time 30000\
    --resize 350 \
"""
#,tcamo.b

A = get_Arguments(
    {
        ('path','path'):opjh('scratch'),
        ('long','longer interval (s)'):60.,
        ('beep_time','min beep time'):-1,
        ('resize','if zero no resize, else pixels'):0,
    },
    file=__file__,
)
exec(A_to_vars_exec_str)

video_capture = cv2.VideoCapture(1)

ret, frame = video_capture.read()

if frame is None:
    video_capture.release()
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    if frame is None:
        cE('camera not found')
        assert False

d = datetime.date.today()

if beep_time_ > 0:
    beep_timer = Timer(beep_time_)


path = opj(
    path_,
    str(d.year),
    str(d.today().month),
    str(d.today().day),
    'timelapse.'+time_str()
)

os_system('mkdir -p',path,e=1)

ctr = 0

while True:

    time.sleep(long_)

    ret, frame = video_capture.read()

    if resize_:
        frame = resize_to_extent(frame,resize_)

    cv2.imshow('Video',frame)

    k = cv2.waitKey(1)

    fname_ = opj(path,d2p(ctr,'jpg'))

    imsave(fname_,frame)#rgbframe)


    if beep_timer.rcheck():

        s = os.statvfs('/')

        fr = dp((s.f_bavail * s.f_frsize) / 1024 / 1000000)

        

        o=unix("pmset -g batt")
        p='\n'.join(o)
        r = "([0-9]+)%"
        per = re.search(r,p)[1]
        os_system('say',fr,'gigabytes free')
        os_system('say battery at',per,'percent')


    ctr += 1

    k = cv2.waitKey(1)

    if  k & 0xFF == ord('q'):
        break

video_capture.release()

cv2.destroyAllWindows()

#EOF

