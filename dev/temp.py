
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

figure('test2')
from sampleimages import imgs
sh(imgs.mtum,'test2')

#,a
figure('randn')
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




#EOF
