from utilz2 import *
# python3 utilz2/dev/project.py --src tac --tag himac1
args=dict(
    src='',
    tag='',
    termout=True,
)
p=getparser(**args)
assert ope(p.src)


def run_project(src,repos=[opjh('UTILS_')]):
	name=fname(src)
	s=time_str()
	if p.tag:
		s+='-'+get_safe_name(p.tag)
	dst=opjh('project_'+name,s)
	mkdirp(dst)
	os_system('rsync -ravL',src,dst,e=1,a=1)
	for d in ['env','figures','net/weights','stats']:
		mkdirp(opj(dst,name,d))
	for d in repos:
		os_system('rsync -ravL',d,opj(dst,name,'env'),e=1,a=1)

	m=most_recent_file_in_folder(opjh('project_'+name)).replace(opjh(),'')
	cg(m)
	o=opj(m,name,'stats/out.txt')
	cb(o)
	m=d2p(m.replace('/','.'),name,'code.main')
	cy(m)
	os_system('python3 -m',m,' > ',o,e=1)

if __name__ == '__main__':
	run_project(p.src)

#EOF