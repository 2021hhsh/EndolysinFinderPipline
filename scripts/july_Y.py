def july(list1):
  j = 'NO'
  for i in list1:
    if '(+)' in i or '(-)' in i:
      j = 'YES'
      break
    
  return j

with open('all_extracted-seq.txt', 'r') as f:
  for line in f:
    lines = line.strip('\n').split('\t')
    gcas = lines[15:]
    new_list = lines[:10]
    new_list.append(july(gcas))
    new_list.extend(lines[10:])
    print('\t'.join(new_list))
