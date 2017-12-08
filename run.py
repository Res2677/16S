import os
import sys
#print sys.argv[0]
path = sys.argv[0].split('/')
del path[-1]
m = "/".join(path)
if m != '':
  m = m +'/'
o1 = os.popen('python ' + m +'1.filter.py ' + sys.argv[1])
print o1.read()
o2 = os.popen('python ' + m +'2.fastqc.py ' + sys.argv[1])
print o2.read()
o3 = os.popen('python ' + m +'3.merge.py ' + sys.argv[1])
print o3.read()
o4 = os.popen('python ' + m +'4.otus.py ' + sys.argv[1])
print o4.read()
o5 = os.popen('python ' + m +'5.removehuman.py ' + sys.argv[1])
print o5.read()
