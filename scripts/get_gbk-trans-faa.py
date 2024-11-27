import os
import re

def change(s):
    li = s.split(' ')
    leng = len(li)
    return li[0]+'|'+'-'.join(li[1:])

dir2 = 'vibrant-output'
#test/CFYS01.1/VIBRANT_CFYS01.1/VIBRANT_phages_CFYS01.1/CFYS01.1.phages_combined.gbk
pat = f'{dir2}/GCA-tag/VIBRANT_GCA-tag/VIBRANT_phages_GCA-tag/GCA-tag.phages_combined.gbk'
dir1 = 'gbk-faa-out'

if os.path.exists(dir1) == False:
    os.mkdir(dir1)
#dir2 = 'test'
for f1 in os.listdir(dir2):
    f_name = pat.replace('GCA-tag', f1)
    if os.path.exists(f'{dir1}/{f1}.faa') or os.path.exists(f_name) == False:
        continue

    f_o = open(f'{dir1}/{f1}.faa', 'w')
    with open(f_name, 'r') as f:
        txt = f.read()
    list_txt1 = (txt.split('//'))
    
    for txt1 in list_txt1:
        list_txt2 = txt1.split('	 CDS	')

        for txt2 in list_txt2:
            if '/translation' not in txt2:
                continue
            locus_tag = change(re.findall('/locus_tag=\"(.*?)\"', txt2)[0])
            protein_id = re.findall('/protein_id=\"(.*?)\"', txt2)[0]
            product = re.findall('/product=\"(.*?)\"', txt2)[0].replace(' ', '-')
            try:
                translation = re.findall('/translation=\"(.*?)\"', txt2,re.S)[0].replace('\t','').replace(' ','').replace('\n','')
            except IndexError:
                print(txt2)
            site = txt2.split('\n')[0].strip(' ').strip('\t').strip('\n').strip(' ')


    
            f_o.write(f'>{f1}|{locus_tag}|{protein_id}|{site}|{product}\n{translation}\n')
    
    f_o.close()
    #exit()


#with open()
