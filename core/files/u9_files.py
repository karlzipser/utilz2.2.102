from utilz2.core.u5_paths import *
from utilz2.core.u7_times import *
from utilz2.core.u6_printing import *
import fnmatch


def rb(s):
    return s.replace('\\','')

    
def txt_file_to_list_of_strings(path_and_filename):
    f = open(path_and_filename,"r")
    str_lst = []
    for line in f:
        str_lst.append(line.strip('\n'))
    return str_lst


def list_of_strings_to_txt_file(path_and_filename,str_lst,write_mode="w"):
    f = open(path_and_filename,write_mode)
    for s in str_lst:
        f.write(s+'\n')
    f.close()


def text_to_file(f,t,write_mode="w"):
    list_of_strings_to_txt_file(f,t.split('\n'),write_mode=write_mode)


def file_to_text(f):
    return '\n'.join(txt_file_to_list_of_strings(f))


def assert_disk_locations(locations):
    if type(locations) == str:
        locations = [locations]
    for l in locations:
        if len(gg(l)) < 1:
            raise ValueError(d2s('Could not find',l))


def percent_disk_free(disk='/'):
    statvfs = os.statvfs(disk)
    size_of_filesystem_in_bytes = statvfs.f_frsize * statvfs.f_blocks     # Size of filesystem in bytes
    number_of_free_bytes_that_ordinary_users_have = statvfs.f_frsize * statvfs.f_bavail     # Number of free bytes that ordinary users
    percent_free = dp(100*number_of_free_bytes_that_ordinary_users_have/(1.0*size_of_filesystem_in_bytes))
    return percent_free


def get_temp_filename(path=opjD()):
    t = time.time()
    r = opj(path,d2p('__temp__',t,random_with_N_digits(9),'txt'))
    while t >= time.time():
        print("get_temp_filename sleeping")
        time.sleep(1/10**9)
    return r


def text_editor( txt='', show=True, startinsert=True ):

    import os, subprocess, tempfile

    (fd, path) = tempfile.mkstemp()
    fp = os.fdopen(fd, 'w')
    fp.write(txt)
    fp.close()
    
    if startinsert:
        e = 'vim -c startinsert'
    else:
        e = 'vim'

    editor = os.getenv('EDITOR', e)

    #print(editor, path)

    subprocess.call('%s %s' % (editor, path), shell=True)

    txt = file_to_text(path)
    
    if show:
        box(txt)

    os.unlink(path)

    return txt




if __name__ == '__main__':
    eg(__file__)
    print("percent_disk_free(disk='/') =", percent_disk_free(disk='/'))



#EOF
