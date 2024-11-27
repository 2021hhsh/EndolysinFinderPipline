import os
import re

with open('result/result.tbl','r') as f:
  lines = f.read().split('\n')

dic = {}

for line in lines:
  if '\n' in line:
    print('yes')
  if '#' in line:
    continue
  else:
    matchs = re.findall(r'^\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+([\d.e-]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.e-]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.+)$',line)
    #print(matchs[0][2]+'\t'+matchs[0][0]+'\t'+matchs[0][-1])
    try:
      if matchs[0][2] not in dic:
        dic[matchs[0][2]]=[]
        dic[matchs[0][2]].append(matchs[0][0]+'《'+matchs[0][1]+'|'+matchs[0][4]+'|'+matchs[0][-1]+'》')
      else:
        dic[matchs[0][2]].append(matchs[0][0]+'《'+matchs[0][1]+'|'+matchs[0][4]+'|'+matchs[0][-1]+'》')
    except:
      continue

with open('sorted.txt','r') as fd:
  inputs = fd.read().strip('\n').split('\n')

#for i,j in dic.items():
#  print(i+'\t'+','.join(j))

fout = open('merged-table.txt','w')
for input in inputs:
  name = input.split('\t')[-2]
  try:
    fout.write(input+'\t'+','.join(dic[name])+'\n')
  except KeyError:
    fout.write(input+'\t'+'none'+'\n')
fout.close()

