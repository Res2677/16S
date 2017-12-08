import pipe_main
import time
import os
import linecache
import fq_to_fa
process= pipe_main.main()
option_dict = pipe_main.option_dict

process = option_dict['process output path'] + "/4.otus"
os.popen('mkdir -p ' + process)

#os.popen('grep \'>\' ' + option_dict['process output path'] + '/3.merge' + '/out.extendedFrags.fasta')
if option_dict['data type'] == 'PE':
  grep_cmd = 'grep \'>\' ' + option_dict['process output path'] + '/3.merge' + '/merge.fasta |wc -l'
  size = os.popen(grep_cmd).read().strip()
  #print size
  otus_cmd_0 = option_dict['usearch path'] + ' -fastx_uniques ' + option_dict['process output path'] + '/3.merge' + '/merge.fasta -fastaout ' + process + '/uniques.fa -sizeout -relabel Uniq'
  otus_cmd_1 = option_dict['usearch path'] + ' -cluster_fast ' + option_dict['process output path'] + '/3.merge' +'/merge.fasta -id ' + option_dict['O_cluster distance'] + ' -centroids ' + process + '/otus.fa' + ' -uc ' + process + '/clusters.uc'
  otus_cmd_2 = option_dict['usearch path'] + ' -cluster_otus ' + process + '/uniques.fa -otus ' + process + '/otus.fa -relabel Otu'
  otus_cmd_3 = option_dict['usearch path'] + ' -unoise3 ' + process + '/uniques.fa -zotus ' + process + '/zotus.fa'
  otus_cmd_4 = option_dict['usearch path'] + ' -otutab ' + option_dict['process output path'] + '/3.merge' + '/merge.fastq -otus ' + process + '/otus.fa -otutabout ' + process + '/otutab.txt -mapout ' + process + '/map.txt'
  otus_cmd_5 = option_dict['usearch path'] + ' -otutab_norm ' + process + '/otutab.txt -sample_size ' + size + ' -output ' + process + '/otutab_norm.txt'
  #otus_cmd_6 = option_dict['usearch path'] + ' -otutab ' + option_dict['process output path'] + '/3.merge' + '/merge.fastq' + ' -zotus ' + process + '/zotus.fa' + ' -otutabout ' + process + '/zotutab.txt -mapout ' + process + '/zmap.txt'
  #otus_cmd_7 = option_dict['usearch path'] + ' -otutab_norm ' + '/zotutab.txt' + ' -sample_size ' + size + ' -output ' + process + '/zotutab_norm.txt'
  os.popen(otus_cmd_0)
  os.popen(otus_cmd_1)
  os.popen(otus_cmd_2)
  os.popen(otus_cmd_3)
  os.popen(otus_cmd_4)
  os.popen(otus_cmd_5)
  #os.popen(otus_cmd_6)
  #os.popen(otus_cmd_7)
if option_dict['data type'] == 'SE':
  #size = os.popen('grep \'>\' ' + option_dict['process output path'] + '/1.filter' +'/r1.fa |wc -l').read()
  fq_to_fa.main(option_dict['process output path'] + '/1.fliter' + '/r1.fq ',option_dict['process output path'] + '/1.fliter' + '/r1.fasta')
  otus_cmd_1 = option_dict['usearch path'] + ' -fastx_uniques ' + option_dict['process output path'] + '/1.fliter' + '/r1.fasta' +  ' -fastaout uniques.fa -sizeout -relabel Uniq'

pathDir =  os.listdir(process)
if 'map.txt' in pathDir:
  ll_cmd = 'ls -l ' + process + '/map.txt'
  mm = os.popen(ll_cmd).read()
  print mm
  map_size = mm.split(' ')[4]
  map_szie = ''.join(map_size.split())
  print map_szie
  if int(map_size) !=0:
    print "successfully generate otus"
  else:
    print "no otus,please check"
