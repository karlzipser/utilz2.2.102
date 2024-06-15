from utilz2.core.files import *
from utilz2.misc.u13_printing import *
from utilz2.misc.u14_have_using import *
from utilz2.misc.u16_sys import *
from utilz2.misc.u17_osx import *
from utilz2.vis import *
import subprocess


def runu2(e=1):
    exec(f2t(opjh('utilz2/scripts/u2.py')))
    if e:
        u2.print()
runu2(e=0)


def mkdirp_( *args, e=0,r=0,a=1 ):
    path = opj(*args)
    os.system('mkdir -p '+path)#, e=e, r=r, a=a )


def open_url(url):
    if using_osx():
        os_system('open -a Firefox',url,'&')
    else:
        os_system('firefox -new-tab',url,'&')


def open_src():
    open_url(u2.sn.src)


def open_dst():
    open_url(u2.sn.dst)


def parse_dimensions(s):
    p=r'\(h(\d+)w(\d+)\)'
    m=re.search(p,s)
    if m:
        h=int(m.group(1))
        w=int(m.group(2))
        return h,w
    else:
        return None


def u2gcsp(run_=True):
    if run_:
        runu2()
    s=gcsp(
        code_file=          u2.sn.src,
        snippet_path=       pname(u2.sn.dst),
        save_snippet=       u2.sn.save_snippet,
        save_code=          u2.sn.save_code,
        include_codefile=   u2.sn.include_codefile,
        include_output=     u2.sn.include_output,
        show_snippet=       u2.sn.show_snippet,
        e=                  u2.sn.e,
    )
    return s

def u2merge(run_=True):
    if run_:
        runu2()
    merge_snippets(
        w=u2.sn.dst,
        show=u2.sn.show,
        default_height=u2.sn.default_height,
    )


def u2do():
    s=u2gcsp()
    s=s+'\n\nu2merge(run_=False)\n'
    return s


def esm():
    runu2()
    try:
        s=u2gcsp()
        exec(s)
    except KeyboardInterrupt:
        sys.stdout=u2.stdout
        cr('*** KeyboardInterrupt ***')
        sys.exit()
    except Exception as e:
        sys.stdout=u2.stdout
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Exception!')
        print(d2s(exc_type,file_name,exc_tb.tb_lineno))
    u2merge()
    CA()


def esp(use_except=True):
    runu2()
    if True:#try:
        s=gcsp(
            code_file=          u2.sn.src,
            snippet_path=       pname(u2.sn.dst),
            save_snippet=       False,
            save_code=          False,
            include_codefile=   False,
            include_output=     False,
            show_snippet=       u2.sn.show_snippet,
            e=                  u2.sn.e,
        )
        exec(s)
    """
    except KeyboardInterrupt:
        sys.stdout=u2.stdout
        cr('*** KeyboardInterrupt ***')
        sys.exit()
    except Exception as e:
        sys.stdout=u2.stdout
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Exception!')
        print(d2s(exc_type,file_name,exc_tb.tb_lineno))
    """
    

def ___u2merge():
    exec(f2t(opjh('utilz2/scripts/u2.py')))
    merge_snippets(
        w=u2.sn.dst,
        show=u2.sn.show,
        default_height=u2.sn.default_height,
    )


def merge_snippets(
    w=opjh('snippets/working'),
    show=True,
    default_height=120,
):
    """
    exec(gcsp(opjh('utilz2'),include_output=1));merge_snippets();CA()
    u2.sn.src=opjh('utilz2')
    u2.sn.dst=opjh('snippets/working')
    exec(gcsp(u2.spath,include_output=1));merge_snippets();CA()
    """
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters import HtmlFormatter
    css='\n'.join([
        '<head><style>',
        HtmlFormatter().get_style_defs('.highlight'),
        '</style></head>',
        ' '
    ])
    mkdirp_(w)
    fs=find_files(w,['*.snippet.py','*.pdf','*-out.txt'],noisy=False)
    fs = sorted(fs, key=get_file_mtime)
    fs.reverse()
    hs=[]
    for f in fs:
        div=''
        con=False
        for f_ in f.split('/'):
            if len(f_) and f_[0]=='_':
                con=True
        if con:
            continue
        dims=parse_dimensions(f)
        if not isNone(dims):
            height=dims[0]
            width=dims[1]
        else:
            height=0
            width=height
        if '.pdf' in f:
            if not height:
                height=512
                width=height
            div="""
<div>
<object data="PDFFILE"
        type="application/pdf"
        width="WIDTH"
        height="HEIGHT">
        <!--alt : <a href="test.pdf">test.pdf</a>-->
</object>
</div>
            """.replace('PDFFILE',f.replace(w+'/','')).replace('HEIGHT',str(height)).replace('WIDTH',str(width))
        else:
            txt=file_to_text(f)
            if txt:
                if '-out.txt' in f:
                    #div=d2n('<div style="white-space: pre-line;"># Out: ',pname(f).replace(w,'')[1:],'\n',txt,'</div>')
                    div=d2n('<div style="white-space: pre-line;">',txt,'</div>')
                else:
                    div=highlight(txt,PythonLexer(),HtmlFormatter())
                div='\n'.join([
                        """<div style="height:HEIGHTpx;border:1px solid ;overflow:auto;">""",
                        div,
                        '</div>\n',
                    ])
            if not height:
                height=default_height
            div=div.replace('HEIGHT',str(height))
        if div:
            hs.append(div)
    hs=[css]+hs
    htmlfile=opj(w,'_'+time_str()+'.html')
    text_to_file(
        htmlfile,
        '\n'.join(hs)
    )
    open_url(htmlfile)


def get_file_mtime(file_path):
    return os.path.getmtime(file_path)


def get_code_snippet(
    code_file=None,
    start='#,a',
    stop='#,b',
    snippet_path=opjh('snippets'),
    save_snippet=True,
    save_code=True,
    include_codefile=True,
    include_output=True,
    show_snippet=True,
    e=0,
):
    if code_file is None:
        code_file = most_recent_py_file(opjD(),e=e)
        print('*** Warning, setting src location to',code_file)
    elif os.path.isdir(code_file):
        code_file = most_recent_py_file(code_file,e=e)
    elif os.path.isfile(code_file):
        pass
    else:
        cE('Error, code_file',qtd(code_file),'is not valid.')
        assert False
    code_lst = txt_file_to_list_of_strings(code_file)
    snippet_lst = []
    started = False
    _code='\n'.join(code_lst)
    _split=_code.split(start)
    if d2n('start=',qtds(start)) in _code:
        cE('Error, this appears to be where get_code_snippet is defined, cannot use it here.')
        assert False
    elif len(_split)>2:
        cE('Error start token',qtds(start),'appears more than once in',code_file)
        return 'assert False'
    elif len(_split)<2:
        cE('Error start token',qtds(start),'does not appear in',code_file)
        return 'assert False'

        return 'assert False'        
    for c in code_lst:
        if not started and c == start:
            started = True
        elif started and c == stop:
            break
        elif started:
            snippet_lst.append(c)
        else:
            pass
    code_str = '\n'.join(snippet_lst)
    cg('snippet from',code_file)
    if show_snippet:
        cb(code_str)
    if save_snippet:
        snippet_path=opj(snippet_path,'working',d2p(time_str(),fname(code_file).replace('.','-')))
        mkdirp_(snippet_path)
        f=opj(snippet_path,fname(code_file))
        if include_codefile:
            code_str=d2n('# In: ',pname(f).replace(pname(snippet_path),'')[1:],'\n','# ',code_file.replace(opjh(),''),'\n',code_str)

        if save_snippet:
            text_to_file(f.replace('.py','.snippet.py'),code_str)
        if save_code:
            text_to_file(f,'\n'.join(code_lst))

        code_str='\n'.join([
                'CA()',
                code_str,
                d2n('savefigs(',qtd(snippet_path),')'),
            ])
        if include_output:
            code_str="import sys;orig_stdout = sys.stdout;f=open('"+f+"-out.txt','w');sys.stdout=f\n"+code_str+"\nsys.stdout=orig_stdout;f.close()\n"
    return code_str
gcsp = get_code_snippet


def most_recent_py_file(path=opjh(),return_mtime=False,e=0):
    if path==opjh():
        cE('using most_recent_py_file(opjh()), can take awhile')
        time.sleep(3)
    max_mtime = 0
    for dirname,subdirs,files in os.walk(path):
        for fname in files:
            if len(fname) >= 3:
                if fname[-3:] == '.py':
                    full_path = os.path.join(dirname,fname)
                    if e:
                        print(full_path)
                    try:
                        mtime = os.stat(full_path).st_mtime
                        if mtime > max_mtime:
                            max_mtime = mtime
                            max_dir = dirname
                            max_file = fname
                    except Exception as e_:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print('Exception!')
                        print(d2s(exc_type,file_name,exc_tb.tb_lineno))   
    if return_mtime:
        return opj(max_dir,max_file),max_mtime
    else:
        return opj(max_dir,max_file)


def getClipboardData():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    if type(data) != str:
        data = data.decode("utf-8")
    return data
gcd = getClipboardData

def setClipboardData(data):
    """
    setClipboardData
    """
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    try:
        p.stdin.write(data)
    except:
        p.stdin.write(bytes(data,'utf-8'))
    p.stdin.close()
    retcode = p.wait()
scd = setClipboardData

_delimiter = '\n<====>\n'   

def load_clipboards(dst_,delimiter_=_delimiter):
    try:
        clipboards = file_to_text(dst_).split(delimiter_)
    except:
        clipboards = []
    return clipboards


def save_clipboards(clipboard_data,clipboards,dst_,delimiter_=_delimiter,n_=20,verbose=True):
    c = clipboard_data
    if len(clipboards) == 0 or c != clipboards[-1]:
        if c in clipboards:
            clipboards.remove(c)
        clipboards.append(c)
        if len(clipboards) > n_:
            clipboards = clipboards[-n_:]
        text_to_file(dst_,delimiter_.join(clipboards))
        if verbose:
            print('wrote to',dst_)


def access_clipboards(dst_,set_clipboard=True,as_menu=True,delimiter_=_delimiter,shorten=False):
    try:
        while True:

            try:
                clipboards = file_to_text(dst_).split(delimiter_)
            except:
                clipboards = []
            while None in clipboards:
                clipboards.remove(None)
            while '' in clipboards:
                clipboards.remove('')

            clear_screen()

            for i in rlen(clipboards):
                c = clipboards[i]
                if shorten:
                    c = c.replace('\n',' ')
                    c = c.replace('\t',' ')
                    if len(c) > 60:
                        c = c[:60] + '...'

                clp(str(i)+')','`w-b',c,'`y')
                
            j = input_int_in_range(0,len(clipboards),'choice > ')
            if j == '<quit>':
                break
            if j is not None:
                if set_clipboard:
                    setClipboardData(clipboards[j])
                if not as_menu:
                    return clipboards[j].split('\n')

    except KeyboardInterrupt:
        cw('\n\n*** KeyboardInterrupt, done ***\n')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        cE(exc_type,file_name,exc_tb.tb_lineno) 


if __name__ == '__main__':
    


    code = """
clear_screen()
if '__file__' in locals(): eg(__file__)
clp('most_recent_py_file:', most_recent_py_file())
print('')
c = getClipboardData()
print("getClipboardData()")
print('')
clp(c,'`m--')
    """
    for c in code.split('\n'):
        if not c.isspace():
            clp(c,'`--u')
            exec(c)

#EOF
