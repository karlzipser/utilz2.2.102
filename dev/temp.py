
from pypdf import PdfMerger
pdfs=['/Users/karlzipser/out.pdf','/Users/karlzipser/snippets/06Jun24_09h44m36s.temp.py/test2.06Jun24_09h44m37s.pdf','/Users/karlzipser/snippets/06Jun24_09h44m36s.temp.py/test.06Jun24_09h44m36s.pdf']
merger = PdfMerger()
for pdf in pdfs:
    merger.append(pdf)
merger.write("result.pdf")
merger.close()
# enscript -E -q -Z -p - -f Courier10 Desktop/temp.py | ps2pdf - out.pdf


figure('test')
hist(randn(1000))

#, a
figure('test2')
from sampleimages import imgs
sh(imgs.mtum,'test2')
#, b

#,a
figure('randn',figsize=(3,1))
hist(randn(1000))
plt.title('randn')
#,b


figure('mtum')
from sampleimages import imgs
sh(imgs.mtum,'mtum')


#, a
f=opjD('temp.txt')
if ope(f):
	os_system('rm',f)
U2G['altout']=open(f,'w')
for i in range(13):
	prints('j=',i)
U2G['altout'].close()
#, b

#, a
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
code="""
def get_code_snippet_2(code_file=None,start='#,a',stop='#,b',snippet_path=opjh('snippets')):
    #T0=1717657224.065629
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
    cb(code_str)
    #t1=int(time.time()-T0)
    snippet_path=opj(snippet_path,d2p(time_str(),fname(code_file)))
    mkdirp(snippet_path)
    code_str=code_str.replace(start,d2n(30*'#','\n# WARNING, THIS IS A SNIPPET!'))
    code_str+='\n#\n'+30*'#'
    text_to_file(opj(snippet_path,fname(code_file)),code_str)
    code_str='CA()\n'+code_str+d2n('\nsavefigs(',qtd(snippet_path),')')
    return code_str"""
print(highlight(code, PythonLexer(), HtmlFormatter()))
print(HtmlFormatter().get_style_defs('.highlight'))
#, b

import pdfkit
pdfkit.from_file(opjD('temp.html'),opjD('temp.pdf'))
pdfkit.from_file(opjD('temp.html'),opjD('temp-.pdf'))
import pdfkit
pdfkit.from_file(opjD('temp.html'),opjD('temp-.pdf'))
history


#EOF
