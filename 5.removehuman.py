import pipe_main
import time
import os
import linecache
import fq_to_fa
process= pipe_main.main()
option_dict = pipe_main.option_dict

process = option_dict['process output path'] + "/5.removehuman"
os.popen('mkdir -p ' + process)
balstn_cmd = option_dict['blastn path'] +' -db ' + option_dict['B_Hdatabase'] + ' -query ' + option_dict['process output path'] + '/4.otus/otus.fa -out ' + process + '/blastn_human.out -evalue '+ option_dict['B_evalue'] + ' -max_target_seqs 5 -num_threads '+ option_dict['B_threads'] + ' -outfmt 7'
os.popen(balstn_cmd)
print 'blastn done,please waiting a moment,grouping sequences into files....'
human_otu = []
pathDir =  os.listdir(process)
if 'blastn_human.out' in pathDir:
  bout = open(process + '/blastn_human.out').read()
  statout = open(process + '/human_otus.stat','w')
  elem = bout.split('# BLASTN 2.7.1+\n')
  for i in elem:
    if 'Fields:' in i:
      line = i.split('\n')
      otu = line[4].split('\t')
      human_otu.append(otu[0])
      print >> statout,line[4]
else:
  print 'no blastn_human.out in ' + process + ',blastn failed?'
#print human_otu
read_dict ={}
mapfile = open(option_dict['process output path'] + '/4.otus/map.txt').readlines()
for mapline in mapfile:
  mapelem = mapline.strip().split('\t')
  #read_dict[mapelem[1]] =1
  if mapelem[1] not in human_otu:
    if mapelem[1] in read_dict.keys():
      #read_dict[mapelem[1]] = []
      read_dict[mapelem[1]].append(mapelem[0])
    else:
      read_dict[mapelem[1]] = []
      read_dict[mapelem[1]].append(mapelem[0])
#print read_dict
#seq_dict ={}
fa_n = len(open(option_dict['process output path'] + '/3.merge/merge.fasta').readlines())
#for otu in read_dict.keys():
os.popen('mkdir -p '+process+'/group_fasta')
for otu in read_dict.keys():
  aa = open (process+'/group_fasta/'+otu+'.fasta','w')
  for i in range(fa_n):
    if(i-1)%2 == 0:
      k = linecache.getline(option_dict['process output path'] + '/3.merge/merge.fasta',i).split('>@')[1].strip()
      ks = linecache.getline(option_dict['process output path'] + '/3.merge/merge.fasta',i+1).strip()
    #linecache.getline(option_dict['process output path'] + '/3.merge/merge.fasta',i)  
    #k = i.split('>@')[1]
    #for otu in read_dict.keys():
      #print k 
      #print read_dict[otu]
      if k in read_dict[otu]:
        print >> aa,'>'+k+'\n'+ks
  aa.close()
ff = os.popen('ls -l ' + process +'/group_fasta').read()
#print ff
awk_cmd = 'ls -l ' + process +'/group_fasta|awk \'{print $5}\''
ss = os.popen(awk_cmd).read()
gg = ss.split('\n')
ton = 0
for i in gg:
  try:
    ton = ton + int(i)
  except:
    pass
if ton !=0:
  print "filter reads from human sucessfully."
else:
  print "filter reads from human failed."
