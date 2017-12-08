import pipe_main
import os
import linecache
import time
process= pipe_main.main()
option_dict = pipe_main.option_dict


process = option_dict['process output path'] + "/3.merge"
os.popen('mkdir -p ' + process)
if option_dict['data type'] == 'PE':
  c_read1 = option_dict['process output path'] + '/1.filter'+ '/r1.fq'
  c_read2 = option_dict['process output path'] + '/1.filter'+ '/r2.fq'
  merge_cmd = option_dict['flash path'] + ' ' + c_read1 + ' ' + c_read2 + ' -d ' + process + ' --allow-outies &> ' + process + '/merge.log'
  #print merge_cmd
  os.popen(merge_cmd)
  log = open(process + '/merge.log').read()

r1_c = len(open(process + '/out.extendedFrags.fastq').readlines())
out_fa = open(process + '/merge.fasta','w')
out_fq = open(process + '/merge.fastq','w')
for i in range(r1_c):
  if (i-1) % 4 == 0:
    fst_line=linecache.getline(process + '/out.extendedFrags.fastq',i)
    sec_line=linecache.getline(process + '/out.extendedFrags.fastq',i+1)
    print >> out_fa,'>' + fst_line + sec_line.strip()
    print >> out_fq,linecache.getline(process + '/out.extendedFrags.fastq',i) +linecache.getline(process + '/out.extendedFrags.fastq',i+1) +linecache.getline(process + '/out.extendedFrags.fastq',i+2) +linecache.getline(process + '/out.extendedFrags.fastq',i+3).strip()
#out_fa.close()
#out_fq.close()
if option_dict['unmerge add'] == 'y':
  #out_fq = open(process + '/merge.fastq','w+')
  #out_fa = open(process + '/merge.fasta','w+')
  un_r1_c = len(open(process + '/out.notCombined_1.fastq').readlines())
  for i in range(un_r1_c):
    if (i-1) % 4 == 0:
      fst_line=linecache.getline(process + '/out.notCombined_1.fastq',i)
      sec_line1=linecache.getline(process + '/out.notCombined_1.fastq',i+1)
      sec_line2=linecache.getline(process + '/out.notCombined_2.fastq',i+1)
      thr_line1=linecache.getline(process + '/out.notCombined_1.fastq',i+2)
      fou_line1=linecache.getline(process + '/out.notCombined_1.fastq',i+3)
      fou_line2=linecache.getline(process + '/out.notCombined_2.fastq',i+3)
      print >> out_fq,fst_line + sec_line1.strip() + 'NNNNNN' + sec_line2 + thr_line1 + fou_line1.strip() + 'NNNNNN' + fou_line2.strip()
      print >> out_fa,'>' + fst_line + sec_line1.strip() + 'NNNNNN' + sec_line2.strip()
out_fa.close()
out_fq.close()

print "merge read1,read2 done"
#cat_fq = 'cat ' + process + '/out.extendedFrags.fastq ' + process + '/unpair_merge.fastq > ' + process + '/out.merge.fastq'
#cat_fa = 'cat ' + process + '/out.extendedFrags.fasta ' + process + '/unpair_merge.fasta > ' + process + '/out.merge.fasta'
#sh = open(process + '/3.merge.sh','w')
#print >> sh,cat_fq + '\n' + cat_fa
#print cat_fq,cat_fa
#time.sleep(1)
#sh_cmd = process + '/3.merge.sh'
#os.system(sh_cmd)
#print sh_cmd
#time.sleep(1)
#os.popen(cat_fa)
