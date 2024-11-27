import os
import sys


try :
    item = sys.argv[1]
except IndexError:
    print('请输入文件名：unique_seq.py xxx.fna')
if item == '':
    print('请输入文件名：unique_seq.py xxx.fna')
with open(item,'r') as f:
    list_seq = f.read().strip('\n').strip('>').split('\n>')
print(len(list_seq))

dic = {}
for seq in list_seq:
    if seq == '':
        continue
    else:
        key = ''.join(seq.split('\n')[1:]).strip('\n')
        value = seq.split('\n')[0]
        if key not in dic:
            dic[key] = []
        dic[key].append(value)

print(len(dic))

f_sta = open(item.strip('.faa')+'_uniq.sta','w')
with open(item.strip('.faa')+'_uniq.faa','w') as d:
    for i, j in dic.items():
        d.write('>'+j[0]+'\n'+i+'\n')
        f_sta.write('\t'.join(j)+'\n')
f_sta.close()

