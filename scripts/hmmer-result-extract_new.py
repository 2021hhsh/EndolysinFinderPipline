import os
import re

fout = open('hmmer-search-result','w')

for file in os.listdir('out'):

# 打开包含HMMER search结果的文件，这里用示例文本代替
    if file == '.history':
      continue
    with open(f'out/{file}', 'r') as f:
        text = f.read()
    mod_name = re.findall('Query:       (.*?)\n',text)[0].replace('  ','')
    # 通过正则表达式提取所需信息
    #content = re.findall('')
    pattern = r'^\s*([\d.e-]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.e-]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)\s+(\S+)\s+(.+)$'
    matches = re.findall(pattern, text, flags=re.MULTILINE)
    #print(matches)

    # 输出提取的信息
    for match in matches:
        evalue1, score1, bias1, evalue2, score2, bias2, hmm_from, target_from, target_id, d= match
        descript = target_id.split('|')[2]
        fout.write(f'{mod_name}\t{evalue1}\t{score1}\t{bias1}\t{evalue2}\t{score2}\t{bias2}\t{hmm_from}\t{target_from}\t{target_id}\t{descript}\n')
fout.close()
