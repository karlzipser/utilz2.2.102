#!/usr/bin/env python3

from utilz2 import *

args=dict(
    t=0.1,
)
p=getparser(**args)

nvidia_smi_continuous(p.t)

#EOF

    