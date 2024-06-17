from utilz2 import *
from striprtf.striprtf import rtf_to_text 
import pdfkit


def rtf2html(src,dst,replace={}):
    t = f2t(src)
    t = t.replace('\\i0 ','</i>')
    t = t.replace('\\i ','<i>')
    t = t.replace("\\'94",'"')
    t = t.replace("\\'93",'"')
    t = t.replace("\\'92","'")
    t = t.replace("\\'91","'")
    t = t.replace("\\\'95","")
    t=rtf_to_text(t)
    t0=t.split('\n')
    t1=[]
    previous_is_tab=False
    for s in t0:
        if not s:
            previous_is_tab=False
        else:
            if previous_is_tab:
                s='&emsp;'+'&emsp;'+s
            previous_is_tab=True
        t1.append(s)
    t='\n'.join(t1)
    t=d2n(
        '<font face="Georgia" size="10"><center>Chapter X</center></font>\n\n',
        '<font face="Georgia" size="6">',
        t[0],
        '</font>',
        '<font face="Georgia" size="5">',
        t[1:],
        '</font>','\n\n<center>&#9679; &#9679; &#9679;</center>\n'
    )
    h=d2n(
        """
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
    <div align="justify" style="white-space: pre-line;">

        """,
        t,
        """

    </div>
    </body>
    </html>"""
    )
    for k in replace:
        h=h.replace(k,replace[k])
    t2f(dst,h)


def html2pdf(src,dst,show=False):
    margin='30mm'
    if show:
        quit_Preview()
    options = {
        'page-size': 'Letter',
        'margin-left': margin,
        'margin-right': margin,
        'margin-bottom': margin,
        'margin-top': margin,
        'footer-center': '[page]',
        'footer-font-size': 12,
        'footer-font-name': "Georgia",
        'footer-spacing':6,
        'no-outline': None
    }
    pdfkit.from_file(
        src,
        dst,
        options=options
    )
    if show:
        os_system('open',dst)


if __name__ == '__main__':
    fs=find_files(opjD('rtfs'),['*.rtf'])
    ctr=0
    for rtf in fs:
        ctr+=1
        replace={'Chapter X':d2s('Chapter',ctr)}
        html=rtf.replace('rtf','html')
        pdf=rtf.replace('rtf','pdf')
        mkdirp(qtd(pname(html)))
        mkdirp(qtd(pname(pdf)))
        rtf2html(rtf,html,replace)
        html2pdf(html,opj(pname(pdf),d2s('Chapter',ctr,'-',fname(pdf))),show=True)

#EOF
