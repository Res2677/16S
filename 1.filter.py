#coding=utf-8
import sys
#import codecs
import pipe_main
#process={}
process= pipe_main.main()
#print option_dict
import re
import time
import os
import linecache
option_dict = pipe_main.option_dict
process = option_dict['process output path'] + "/1.filter"
os.popen('mkdir -p ' + process)
adaptor = option_dict['F_adapter'].split(' ')
ad_f = open(process + '/1.adaptor.list','w')
logfile = process + '/Trimmomatic_logfile'
#adaptor_file = open(process + '/1.adaptor.list','w+')
if option_dict['data type'] == 'PE':
    filter_cmd ='java -jar ' + option_dict['trimmomatic.jar path'] +' PE -threads ' + option_dict['F_threads'] + ' -' + option_dict['F_basephred'] + ' -trimlog '+ logfile + ' ' + option_dict['read1'] + ' ' + option_dict['read2'] + ' ' + process + '/r1.fq ' + process + '/r1-u.fq ' + process + '/r2.fq ' + process + '/r2-u.fq ' + 'ILLUMINACLIP:' + process + '/1.adaptor.list:' + option_dict['F_ILLUMINACLIP'] + ' LEADING:' + option_dict['F_LEADING'] + ' TRAILING:' + option_dict['F_TRAILING']  + ' SLIDINGWINDOW:' + option_dict['F_SLIDINGWINDOW'] + ' MINLEN:' + option_dict['F_MINLEN'] + ' &>' + process + '/process.log'
    print >> ad_f,'>5\n'+ adaptor[1] + '\n>3\n'+ adaptor[3]
elif option_dict['data type'] == 'SE':
    filter_cmd ='java -jar ' + option_dict['trimmomatic.jar path'] +' PE -threads ' + option_dict['F_threads'] + ' -' + option_dict['F_basephred'] + ' -trimlog '+ logfile + ' ' + option_dict['read1'] +' ' + process + '/r1.fq ' + process + '/r1-u.fq ' + 'ILLUMINACLIP:' + process + '/1.adaptor.list:' + option_dict['F_ILLUMINACLIP'] + ' LEADING:' + option_dict['F_LEADING'] + ' TRAILING:' + option_dict['F_TRAILING']  + ' SLIDINGWINDOW:' + option_dict['F_SLIDINGWINDOW'] + ' MINLEN:' + option_dict['F_MINLEN'] + ' &>' + process + '/process.log'
    print >> ad_f,'>5\n'+ adaptor[1]
else :   
    print 'data type input error,please check congifure file carefully!!!\n'

#print filter_cmd
os.popen(filter_cmd)
#ff = log.read()
#print 'ssss' + ff + 'sssss'
#n_f = open(logfile,'w')
#print >> n_f,ff
#time.sleep(0.5)
#print cc[3]
log = open(process +'/process.log') 
ff = log.read()
if "Completed successfully" in ff:
    print "filter successfully finished"
    message = open(process + '/filter_message.list','w')
    cc = ff.split('\n')
    pattern = re.compile(r"Input Read Pairs: (\S+) Both Surviving: (\S+) \((\S+)%\) Forward Only Surviving: (.*?) \((.*?)%\) Reverse Only Surviving: (.*?) \((\S+)%\) Dropped: (\S+) \((\S+)%\)")
    match = pattern.match(cc[3])
    ss = "reads总数量:%s\n被保留的reads数量:%s\t被保留的reads百分比:%s\n只有前一条read被保留的数量:%s\t只有前一条read被保留的百分比:%s\n只有后一条read被保留的数量:%s\t只有后一条read被保留的百分比:%s\n被过滤掉的reads数量:%s\t被过滤掉的reads百分比:%s\n" % (match.group(1),match.group(2),match.group(3),match.group(4),match.group(5),match.group(6),match.group(7),match.group(8),match.group(9))
    #sss = "总数量"
    print >> message,ss
    #g = ss1.encode('gbk') 
    #str=g.decode('gbk').encode('utf-8')
    #print str
    #print ss1.decode('gbk','ignore').encode('utf-8')
else:
    print "filter failed."

#p = os.popen('grep \'Completed successfully\' process.log')
#print p;
#time.sleep(10)
#logfile = open('process.log')
#ff = logfile.read()
#print ff
