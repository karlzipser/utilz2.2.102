#!/usr/bin/env python3

from k3.utils import *

#record_PID(__file__,just_one=True)

A = get_Arguments(
	{
		'dst' : opjb('_clipboards.txt'),
		'delimiter' : '\n<====>\n',
		't' : 0.333,
		'n' : 1000,
		'quoted' : False,
    },
    verbose=True,
    file=__file__,
)
exec(A_to_vars_exec_str)


clipboards = load_clipboards(dst_=dst_,delimiter_=delimiter_)

while True:

	c = getClipboardData()

	if A['quoted']:
		c = qtd(c)



	save_clipboards(c,clipboards,dst_,delimiter_,n_,verbose=True)

	time.sleep(t_)


#EOF
