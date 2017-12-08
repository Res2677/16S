import os
import linecache
#from sys import argv
option_dict = {}
def main():
  cfg = '16S-18S.cfg'
  ff = open(cfg).readlines()
  for line in ff:
    if line.strip():
      line_t = line.strip()
      if line_t[0] != '#':
        line_k = line_t.split('#')
        option = line_k [0].split('=')
        option_dict[option[0].strip()] = option[1].strip()
  return option_dict
if __name__ == '__main__':
  main()
