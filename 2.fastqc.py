import pipe_main
import os
import linecache
import time
process= pipe_main.main()
option_dict = pipe_main.option_dict

def as_num(x):
  if 'E' in x:
    y = x.split('E')
    try:
      k = float(y[0])
      return k*pow(10,int(y[1]))
    except:
      return x
  else:
    try:
      return float(x)
    except:
      return x

def ff_num(x):
  try:
    k = int(x)
    #print type(x),type(k)
    return k
  except:
    return x
def mm_num(x):
  try:
    k = float(x)
    return k
  except:
    return x

def N_base():
  n_cun =0
  process = option_dict['process output path'] + "/2.fastqc"
  if option_dict['data type'] == 'PE':
    pathDir =  os.listdir(process)
  if 'r1_fastqc' in pathDir and 'r2_fastqc' in pathDir:
    r1_rep = open(process + '/r1_fastqc' + '/fastqc_data.txt').read()
    elem = r1_rep.split('>>END_MODULE\n')
    n_line = elem[6].split('\n')
    for mmm in n_line:
      n_v = mmm.split('\t')
      if len(n_v) > 1 and isinstance(as_num(n_v[1]), float):
        #print n_v[1]
        if as_num(n_v[1]) > float(option_dict['N content']):
          n_cun = n_cun + 1
          print n_v[1]
      else :
        pass
  if n_cun > 0:
    return False
  else:
    return True

def Q_pass(kk,Q30_s,Q20_s):
  Q30_n = 0
  Q20_n = 0
  TO_n = 0
  q_line = kk.split('\n')
  for qqq in q_line:
    q_v = qqq.split('\t')
    if len(q_v) >1:
      if isinstance(ff_num(q_v[0]),int):
        if ff_num(q_v[0]) >=30:
          Q30_n = Q30_n + mm_num(q_v[1])
        if ff_num(q_v[0]) >=20:
          Q20_n = Q20_n + mm_num(q_v[1])
        TO_n = TO_n + mm_num(q_v[1])
  Q30_p = Q30_n/TO_n
  Q20_p = Q20_n/TO_n
  if Q30_p >= Q30_s and Q20_p >= Q20_s:
    return True
  else:
    return False

def judge_pass():
  process = option_dict['process output path'] + "/2.fastqc"
  os.popen('mkdir -p ' + process)
  pathDir =  os.listdir(process)
  if 'r1_fastqc' in pathDir:
    os.popen('rm -rf ' + process + '/r1_fastqc')
  if 'r2_fastqc' in pathDir:
    os.popen('rm -rf ' + process + '/r2_fastqc')
  if option_dict['data type'] == 'PE':
    fastqc_cmd = option_dict['fastqc path'] + ' ' + option_dict['process output path'] + '/1.filter/r1.fq ' + option_dict['process output path'] + '/1.filter/r2.fq -o ' + process
    #unzip_cmd = 'unzip '+process + '/r1_fastqc.zip'
    os.popen(fastqc_cmd)
    pathDir =  os.listdir(process)
    if 'r1_fastqc.zip' in pathDir and 'r2_fastqc.zip' in pathDir:
      os.popen('unzip '+ process + '/r1_fastqc.zip -d '+ process)
      os.popen('unzip '+ process + '/r2_fastqc.zip -d '+ process)
      r1_rep = open(process + '/r1_fastqc' + '/fastqc_data.txt').read()
      elem1 = r1_rep.split('>>END_MODULE\n')
      res1 = Q_pass(elem1[3],float(option_dict['Q30']),float(option_dict['Q20']))
      r2_rep = open(process + '/r2_fastqc' + '/fastqc_data.txt').read()
      elem2 = r2_rep.split('>>END_MODULE\n')
      res2 = Q_pass(elem2[3],float(option_dict['Q30']),float(option_dict['Q20']))
      if(res1 and res2):
        return True
      else:
        return False
  if option_dict['data type'] == 'SE':
    fastqc_cmd = option_dict['fastqc path'] + ' ' + option_dict['process output path'] + '/1.filter/r1.fq -o ' + process
    os.popen(fastqc_cmd)
    pathDir =  os.listdir(process)
    if 'r1_fastqc.zip' in pathDir:
      os.popen('unzip '+ process + '/r1_fastqc.zip -d '+ process)
      r1_rep = open(process + '/r1_fastqc' + '/fastqc_data.txt').read()
      elem1 = r1_rep.split('>>END_MODULE\n')
      res1 = Q_pass(elem1[3],float(option_dict['Q30']),float(option_dict['Q20']))
    if(res1):
      return True
    else:
      return False
ll = judge_pass()
cc = N_base()
print ll,cc
if ll ==True and cc == True:
  print "QC pass successfully."
else:
  print "QC failed.You may should improve the indicator for step1(filter)"


#print Q30_p,Q20_p,Q30_n,Q20_n,TO_n


'''
elif option_dict['data type'] == 'SE':
  fastqc_cmd = option_dict['fastqc path'] + ' ' + option_dict['process output path'] + "/1.filter/r.fq " + '-o ' + option_dict['process output path'] + "/2.fastqc"
  os.popen(fastqc_cmd)
  pathDir =  os.listdir(filepath)
  if 'dd' in pathDir:
    os.popen()
'''
