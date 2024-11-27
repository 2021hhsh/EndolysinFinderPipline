import os

fout = open('out_seq.fa','w')
with open('../hmmer-input-uniq/hmmer_in_seq_uniq.faa','r') as f:
  lists = f.read().strip('\n').split('>')


diction = {}
for item in lists:
  if '\n' not in item:
    continue
  key = item.strip('\n').split('\n')[0].split(' ')[0]
  value = '>'+item.strip('\n')
  diction[key] = value

with open('sorted.txt','r') as d:
  list_titles = d.read().strip('\n').split('\n')

for line in list_titles:
  id = line.split('\t')[-2]
  fout.write(diction[id]+'\n')
fout.close()
