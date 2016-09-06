import subprocess
from multiprocessing.dummy import Pool as ThreadPool

exe_path = 'D:/temp/pdf_html/pdf2htmlEX/pdf2htmlEX.exe'
args = [
    exe_path,
    'd:/temp/pdf_html/data/600637_P7.pdf',
    '--dest-dir', 'dest',
]

args_2 = [
    exe_path,
    'd:/temp/pdf_html/data/000005_P19.pdf',
    '--dest-dir', 'dest',
]

args_3 = [
    exe_path,
    'd:/temp/pdf_html/data/300055_P24.pdf',
    '--dest-dir', 'dest',
]

#
# popenargs = ' '.join(args)
# print 'popenargs:', popenargs
#
# print subprocess.call(popenargs, shell=True)


pool = ThreadPool(4)
res = pool.map(lambda cmd: subprocess.call(cmd, shell=True), [args, args_2, args_3])
pool.close()
pool.join()

print res


