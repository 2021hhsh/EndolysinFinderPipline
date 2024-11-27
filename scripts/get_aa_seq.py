import os

with open('out_seq.fa', 'r') as f:
  list_aa = f.read().split('>')

dic = {}
for i in list_aa:
  if i.strip('\n') == '':
    continue
  key = i.split('\n')[0].split(' ')[0]
  value = '\n'.join(i.split('\n')[1:])
  dic[key] = value
  
with open('merged-table.txt','r') as d:
  lines = d.read().split('\n')

fout = open('extracted-seq.txt','w')
for line in lines:
  list_line = line.split('\t')
  try:
    name = list_line[-3].strip(' ')
  except:
    print(line)
    continue
  if name == '':
    continue
  seq = dic[name].strip('\n')
  fout.write('\t'.join(list_line[:9])+'\t'+name+'\t'+seq+'\t'+str(len(seq))+'\t'+list_line[-2]+'\t'+list_line[-1]+'\n')
  
fout.close()

