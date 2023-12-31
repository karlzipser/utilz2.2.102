#!/usr/bin/env python3

from k3.utils import *


A = get_Arguments(
	{
		'dst' : opjb('_clipboards.txt'),
		'delimiter' : '\n<====>\n',
    },
    verbose=True,
    file=__file__,
)
exec(A_to_vars_exec_str)

access_clipboards(dst_=dst_,delimiter_=delimiter_)


#EOF


