#!/usr/bin/env python3

from utilz2.misc.u13_printing import *
from utilz2.misc.u19_dict2args import *

crazy=-99999999

args=getparser(
    f=crazy,
    c=crazy,
)

if args.f == crazy and args.c == crazy:
	#cr(args)
	cE("One temperature must be specified.")
	sys.exit()

if args.f != crazy and args.c != crazy:
	#cr(args)
	cE("Only one temperature can be specified.")
	sys.exit()

if args.f != crazy:

	C = dp((args.f - 32.) * 5/9.,1)
	if C > 37:
		cc = cr
	elif C > 0:
		cc = cg
	else:
		cc = cb
	cc('\n\t',args.f,'degrees F =',C,'degrees C')
	print('\n')
	
else:
	F = dp((args.c * 9/5.) + 32,1)

	if F > 98.6:
		cc = cr
	elif F > 32:
		cc = cg
	else:
		cc = cb
	cc('\n\t',args.c,'degrees C =',F,'degrees F\n')

#EOF