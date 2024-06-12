from utilz2.core.files import *
from utilz2.misc.u13_printing import *
from utilz2.misc.u14_have_using import *
from utilz2.misc.u16_sys import *
from utilz2.misc.u17_osx import *
import subprocess

def mkdirp_( *args, e=0,r=0,a=1 ):
    path = opj(*args)
    os.system('mkdir -p '+path)#, e=e, r=r, a=a )


def merge_snippets(w=opjh('snippets/working')):
    from pypdf import PdfMerger
    mkdirp(w)
    pdfs=find_files(w,['*.pdf'])
    pdfs = sorted(pdfs, key=get_file_mtime)
    pdfs.reverse()
    merger = PdfMerger()
    for pdf in pdfs:
        con=False
        for p in pdf.split('/'):
            #cg(p,len(p))
            if len(p) and p[0]=='_':
                #print('ignoring',p)
                con=True
        if con:
            continue
        else:
            pass #print('using',pdf)
        merger.append(pdf)
    f=opj(w,'_'+time_str()+'.pdf')
    merger.write(f)
    merger.close()
    if using_osx():
        quit_Preview()
        os_system('open',f)
    else:
        os_system('killall evince')
        os_system('evince',f,'&')





def open_working(w=opjh('snippets/working')):
    os_system('open -a Firefox',w)

def parse_dimensions(s):
    p=r'\(h(\d+)w(\d+)\)'
    m=re.search(p,s)
    print(m)
    if m:
        h=int(m.group(1))
        w=int(m.group(2))
        return h,w
    else:
        return None

def merge_snippets2(
    w=opjh('snippets/working'),
    show=True,
):
    """
    exec(gcsp3(opjh('utilz2'),include_output=1));merge_snippets2();CA()
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
    #text_to_file(f.replace('.py','.snippet.html'),div)
    mkdirp(w)

    fs=find_files(w,['*.snippet.py','*.pdf','*-out.txt'])
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
            height=dims[1]
            width=dims[0]
        else:
            height=350
            width=height
        if '.pdf' in f:
            div="""
<div>
<object data="PDFFILE"
        type="application/pdf"
        width="HEIGHT"
        height="WIDTH">
        alt : <a href="test.pdf">test.pdf</a>
</object>
</div>
            """.replace('PDFFILE',f.replace(w+'/','')).replace('HEIGHT',str(height)).replace('WIDTH',str(width))
        else:
            txt=file_to_text(f)
            if txt:
                if '-out.txt' in f:
                    txt=d2n('# Out: ',pname(f).replace(w,'')[1:],'\n',txt)
                div=highlight(txt,PythonLexer(),HtmlFormatter())
                div='\n'.join([
                        """<div style="height:120px;border:1px solid ;overflow:auto;">""",
                        div,
                        '</div>\n',
                    ])
        if div:
            hs.append(div)

    #hs=[css]+["""<a href="file:PATH">PATH</a>""".replace('PATH',w)]+hs
    hs=[css]+hs
    htmlfile=opj(w,'_'+time_str()+'.html')
    text_to_file(
        htmlfile,
        '\n'.join(hs)
    )
    if using_osx():
        os_system('open -a Firefox',htmlfile,'&')
    else:
        os_system('firefox -new-tab',htmlfile,'&')
         
        #os_system('killall evince')
        #os_system('evince',f,'&')






def get_file_mtime(file_path):
    return os.path.getmtime(file_path)




def get_code_snippet_3(
    code_file=None,
    start='#,a',
    stop='#,b',
    snippet_path=opjh('snippets'),
    save_snippet=True,
    save_code=True,
    include_codefile=True,
    include_output=False,
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
    if len(_split)>2:
        cE('Error start token',qtds(start),'appears more than once in',code_file)
        return 'assert False'
    elif len(_split)<2:
        cE('Error start token',qtds(start),'does not appear in',code_file)
        return 'assert False'
    for c in code_lst:
        if not started and c == start:
            started = True
        elif started and c == stop:
            break
        elif started:
            snippet_lst.append(c)
        else:
            print(qtd(c))
            #assert False
    code_str = '\n'.join(snippet_lst)
    cg('snippet from',code_file)
    if show_snippet:
        cb(code_str)
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
gcsp3 = get_code_snippet_3








def get_code_snippet_2(
    code_file=None,
    start='#,a',
    stop='#,b',
    snippet_path=opjh('snippets'),
    enscript=True,
    save_snippet=True,
    save_code=True,
    include_codefile=False,
    include_output=False,
    show_snippet=False,
    crop_code_margins=True,
    e=0,
):
    """
    Finds code snippet, saves snippet and figures if any.
    e.g.,
        exec(gcsp2(most_recent_py_file(opjD())))
    """
    #if include_output:
    #    os_system('rm',opjh('out.txt'))
    if code_file is None:
        code_file = most_recent_py_file(opjh(),e=e)
    elif os.path.isdir(code_file):
        code_file = most_recent_py_file(code_file,e=e)
    elif os.path.isfile(code_file):
        pass
    else:
        assert False
    code_lst = txt_file_to_list_of_strings(code_file)
    snippet_lst = []
    started = False
    for c in code_lst:
        if not started and c == start:
            started = True
        if started and c == stop:
            break
        if started:
            snippet_lst.append(c)
    code_str = '\n'.join(snippet_lst)
    cg('snippet from',code_file)
    if show_snippet:
        cb(code_str)
    snippet_path=opj(snippet_path,'working',d2p(time_str(),fname(code_file).replace('.','-')))
    mkdirp_(snippet_path)
    #code_str=code_str.replace(start,d2n(30*'#','\n# THIS IS A SNIPPET FROM\n# ',code_file))
    if include_codefile:
        code_str=code_str.replace(start,d2n('\n# ',code_file))
    else:
        code_str=code_str.replace(start,'')
    #code_str+='\n#\n'+30*'#'
    snippet_file_path=opj(snippet_path,fname(code_file))
    if save_snippet:
        code_str2=code_str
        #if include_output:
        #    code_str2+='\n'+10*'-'+' output:\n'+file_to_text(opjh('out.txt'))
        text_to_file(snippet_file_path,code_str2)
    if save_code:
        text_to_file(snippet_file_path+'-full.py','\n'.join(code_lst))
    if enscript:
        # enscript -E -q -Z -p - -f Courier10 Desktop/temp.py | ps2pdf - out.pdf
        os_system('enscript -E -q -Z -p - -f Courier10 --header \'\'',snippet_file_path,'| ps2pdf -',snippet_file_path.replace('.py','.pdf'),e=1,a=1,r=0)
        if crop_code_margins:
            os_system('pdfcropmargins',snippet_file_path.replace('.py','.pdf'),'-p 0 -o',snippet_file_path.replace('.py','.py.pdf'),e=1,a=1,r=0)
            os_system('rm',snippet_file_path.replace('.py','.pdf'))
    code_str='CA()\n'+code_str+d2n('\nsavefigs(',qtd(snippet_path),')')
    if include_output:
        code_str="import sys;orig_stdout = sys.stdout;f=open('"+snippet_file_path+"-out.txt','w');sys.stdout=f\n"+code_str+"\nsys.stdout=orig_stdout;f.close()\n"
    return code_str
gcsp2 = get_code_snippet_2


def get_code_snippet_(code_file=None,start='#,a',stop='#,b'):
    if code_file is None:
        code_file = most_recent_py_file()
    code_lst = txt_file_to_list_of_strings(code_file)
    snippet_lst = []
    started = False
    for c in code_lst:
        if not started and c == start:
            started = True
        if started and c == stop:
            break
        if started:
            snippet_lst.append(c)
    code_str = '\n'.join(snippet_lst)
    return code_str
gcsp = get_code_snippet_


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
