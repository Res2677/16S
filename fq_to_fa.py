from sys import argv
def main(inputf,outputf):
  r_count = len(open (inputf).readlines())
  for i in range(r_count):
    if (i-1) % 4 == 0:
      fst_line=linecache.getline(inputf,i)
      sec_line1=linecache.getline(process + inputf,i+1)
    out_fa = open(outputf,'w')
    print >> out_fa,'>' + fst_line + sec_line1.strip()

if __name__ == '__main__':
  main()
