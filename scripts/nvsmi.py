
#!/usr/bin/env python3

from utilz2.misc.u13_printing import *
from utilz2.misc.u19_dict2args import *
from utilz2.misc.u16_sys import *

args=getparser(
    t=0.1,
)

nvidia_smi_continuous(args.t)

#EOF

    