#!/usr/bin/env python3
from utilz2 import *
import sys, os

args = ' '.join(sys.argv[1:])

print('\n')

os_system('grep -r -n -I ' + '"'+args+'"' + ' k3',e=1,a=1)

#EOF
