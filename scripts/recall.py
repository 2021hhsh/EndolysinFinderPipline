import os

def get_gca_count(s):
  set1 = set()
  for i in s.split('\t'):
    gca = i.split('|')[0]
    set1.add(gca)
  
  return str(len(list(set1)))+'\t'+s
    
  
  
with open('extracted-seq.txt', 'r') as f:
  list_ = f.read().strip('\n').split('\n')

dic = {}

with open('../hmmer-input-uniq/hmmer_in_seq_uniq.sta', 'r') as f1:
  for line in f1.read().strip('\n').split('\n'):
    dic[line.split('\t')[0]] = line

fout = open('all_extracted-seq.txt', 'w')

for line1 in list_:
  fout.write(line1+'\t'+get_gca_count(dic[line1.split('\t')[9]])+'\n')


fout.close()
