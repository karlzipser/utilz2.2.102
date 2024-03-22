
# ffmpeg -i /Users/karlzipser/Desktop/a.mov -r 2 'a/%04d.png'


fs=sggo(opjD('bouy-videos/*.mov'))
for f in fs:
	mkdirp(opj(pname(f),'frames',fnamene(f)))
	os_system('ffmpeg -i',f,'-r 1',opj(pname(f),'frames',fnamene(f),'%04d.png'),e=1,a=1)


fs=sggo('/Volumes/az-kz-6-10-2021-to-5-7-2022/*.MOV')
for f in fs:
	dstdir=opjD(fname(pname(f)),fnamene(f))
	if not ope(dstdir):
		mkdirp(opjD(fname(pname(f)),fnamene(f)))
		os_system('ffmpeg -i',f,'-r 1',opj(opjD(fname(pname(f)),fnamene(f)),'%04d.png'),e=1,a=1)


fs=['/Users/karlzipser/Desktop/clip_7.mp4']
for f in fs:
	dstdir=opjD(fname(pname(f)),fnamene(f))
	if not ope(dstdir):
		mkdirp(opjD(fname(pname(f)),fnamene(f)))
		os_system('ffmpeg -i',f,'-r 15',opj(opjD(fname(pname(f)),fnamene(f)),'%04d.png'),e=1,a=1)

"""
# to gif
convert *.png screens.gif; convert screens.gif -resize 640x360 screens640x360.gif
"""

#EOF