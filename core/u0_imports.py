




if False:
    def print(*args, stdout=False, **kwargs):
        import sys
        import builtins as __builtins__
        if stdout:
            f = sys.stdout
        else:
            f = sys.stderr
        return __builtins__.print(*args, file=f, **kwargs)


def printr(*args, stdout=False, **kwargs):
    print(*args, end='\r', flush=True,**kwargs)


def interactive():
    import sys
    if hasattr(sys,'ps1'):
        return True
    else:
        return False
    import __main__ as main
    return not hasattr(main, '__file__')





imports = (
    'os',
    'os.path',
    #'shutil',
    #'scipy',
    #'scipy.io',
    #'copy',
    #'string',
    'glob',
    'time',
    'sys',
    #'datetime',
    #'random',
    're',
    #'subprocess',
    #'threading',
    #'serial',
    #'inspect',
    #'fnmatch',
    #'h5py',
    'socket',
    #'getpass',
    #'numbers',
    #'math',
    #'pickle',
    'time',
    #'importlib',
    #('FROM','pprint','pprint'),
    #('FROM','termcolor','cprint'),
    ('FROM','collections','OrderedDict'),
    ('AS','numpy','np'),
    'fire',
    ('FROM','copy','deepcopy'),
    ('FROM','importlib','reload'),
)
# imports are commented out so that they are called when needed, to increase core load speed

for im in imports:
    if type(im) == str:
        try:
            exec('import '+im)
        except:
            pass
            print('Failed to import '+im)
    else:
        assert type(im) == list or type(im) == tuple
        if im[0] == 'FROM':
            try:
                exec('from '+im[1]+' import '+im[2])
            except:
                pass
                print('Failed to from '+im[1]+' import '+im[2])
        else:
            assert(im[0] == 'AS')
            try:
                exec('import '+im[1]+' as '+im[2])
            except:
                pass
                print('Failed to import '+im[1]+' as '+im[2]) 



    
if __name__ == '__main__':
    print('\n*** Testing',__file__,'***')
    print(time.time())
    print()


#EOF
