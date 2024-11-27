import os

def change(s):
    li = s.split(' ')
    leng = len(li)
    return li[0]+'|'+'-'.join(li[1:])


if os.path.exists('fnas') == False:
    os.mkdir('fnas')

dir1 = 'vibrant-output'
mod = 'GCA_test/VIBRANT_GCA_test/VIBRANT_phages_GCA_test/GCA_test.phages_combined.fna'

for gca in os.listdir(dir1):
    fil = dir1+'/'+mod.replace('GCA_test', gca)
    if os.path.exists(fil) == False:
        print(fil)
        continue
    
    if os.path.exists(f'fnas/{gca}_vbrant.fasta'):
        continue

    f_out = open(f'fnas/{gca}_vbrant.fasta', 'w')
    with open(fil, 'r') as f:
        for line in f:
            if line[0] == '>':
                f_out.write(change(line))
            else:
                f_out.write(line)
    f_out.close()

