import os
import sys

checkv_dir = sys.argv[1]
faa_dir = sys.argv[2]
out_dir = sys.argv[3]
key_w = 'holin'
list_dir = os.listdir(checkv_dir)
if os.path.exists(out_dir) == False:
    os.mkdir(out_dir)

def get_pp(s):
    li = s.split('_')
    leng = len(li)
    return '_'.join(li[:leng-1])

def de_len(s):
    leng = len(s)
    return s[:leng-3]

def strip_(s):
    if '(-)' in s and s[-2] == '-':
        s = de_len(s)
        
    if '(+)' in s and s[-2] == '+':
        s = de_len(s)
        
    if '(-)' in s and s[-2] == '-':
        s = de_len(s)
        
    if '(+)' in s and s[-2] == '+':
        s = de_len(s)
    return s
    
    
for phage_dir in list_dir:
    phage_name = phage_dir.strip('_vbrant.fasta')
    list_tite = []
    list_none = []
    
    if os.path.exists(f'{checkv_dir}/{phage_dir}/proviruses.fna') == True:
        with open(f'{checkv_dir}/{phage_dir}/proviruses.fna', 'r') as f:
            for line in f:
                if line[0] == '>':
                    list_tite.append(line.strip('\n'))
    else:
        print(f'{checkv_dir}/{phage_dir}/proviruses.fna')
                    
    if os.path.exists(f'{checkv_dir}/{phage_dir}/quality_summary.tsv') == True:            
        with open(f'{checkv_dir}/{phage_dir}/quality_summary.tsv', 'r') as f:
            list_temp = f.read().strip('\n').split('\n')[1:]
            for i in list_temp:
                if i.split('\t')[7] =='Not-determined':
                    #len1 = len(i.split('\t')[0].split('[PP')[0].strip('>').split('_'))
                    list_none.append(i.split('\t')[0])
                    #print('_'.join(i.split('\t')[0].split('[PP')[0].strip('>').split('_')[:len1-2]).split('.')[0]+'_PP'+i.split('\t')[0].split('[PP')[-1].strip(']'))
    else:
        print(f'{checkv_dir}/{phage_dir}/quality_summary.tsv')
        print('没有这个前噬菌体')
        continue
    
    with open(f'{faa_dir}/{phage_name}.faa', 'r') as d:
        con_faa = d.read()
        seqs = con_faa.strip('\n').strip('>').split('\n>')
        out_seqs = []
        dic = {}
    if con_faa.strip('\n') == '':
        print('序列文件为空')
        continue

        for seq in seqs:
            head = seq.split('\n')[0]
            content = '\n'.join(seq.split('\n')[1:])
            contig_pp = head.split('|')[1]+'|'+head.split('|')[2]
            #print(contig_pp)
            if get_pp(contig_pp) in list_none:
                continue
            
            #try:
            #    contig = head.split('|')[1]
            #except:
            #    print(head)
            #    exit()
            contig = head.split('|')[1]
            
            sites = head.split('|')[4].strip('complement(').strip(')').replace('>', '').replace('<','')
            left = int(sites.split('..')[0])
            right = int(sites.split('..')[1])
            #pp = '[PP '+head.split('|')[1].split('_PP')[-1]+']'
            pp = get_pp(head.split('|')[2])
            
            k = 0
            if len(list_tite) == 0:
                k=1
            for de_title in list_tite:
                
                contig_de = de_title.split('|')[0].strip('>')
                pp_de = get_pp(de_title.split('|')[1].split(' ')[0])
                #pp_de = '[PP '+de_title.split('[PP')[-1].split(']')[0]+']'
                range_de = de_title.split(' ')[-1].split('/')[0]
                l_de = int(range_de.split('-')[0])
                r_de = int(range_de.split('-')[-1])
                #print(left,right,l_de,r_de)
                #print(contig,'|', pp,'|', contig_de,'|', pp_de)
                if pp == pp_de and contig_de == contig:
                    #print(left,right,l_de,r_de)
                    if left >= l_de and right <= r_de:
                        k = 1
                        break
                else:
                    k = 1

            if k == 1:
                dic[head] = content.strip('\n')
                #print(head)
                out_seqs.append(head)

        for ind in range(len(out_seqs)):
            if 'holin' in out_seqs[ind]:
                if ind-1 in range(len(out_seqs)) and 'holin' not in out_seqs[ind-1]:
                    out_seqs[ind-1] = out_seqs[ind-1]+'(+)'

                if ind+1 in range(len(out_seqs)) and 'holin' not in out_seqs[ind+1]:
                    out_seqs[ind+1] = out_seqs[ind+1]+'(-)'
            #else:
            #    if ind-1 in range(len(out_seqs)) and 'holin' in out_seqs[ind-1]:
            #        if ind+1 in range(len(out_seqs)) and 'holin' in out_seqs[ind+1]:
            #            out_seqs[ind] = out_seqs[ind]+'(+-)'
        
        
        f_out = open(f'{out_dir}/{phage_name}.faa' ,'w')
        
        for title in out_seqs:
            
            #print(title)
            f_out.write('>'+title+'\n')
            #print(title.strip('(-)').strip('(+)').strip('(+-)'))
            #if '-sequence_fragment_1_6|PF11195.8|2101..2346|Protein of unknown function (DUF2829' in title:
            #    print(title)
            #    print(strip_(title))
            try:
                f_out.write(dic[strip_(title)].strip('\n')+'\n')
                
            except:
                print(title)
                print()
                print(strip_(title))
                print('-----------------------------------')
            #f_out.write(dic[strip_(title)].strip('\n')+'\n')
            
            
        f_out.close()




