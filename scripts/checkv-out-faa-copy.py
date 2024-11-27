import os
import sys
import re  # Import the regular expression module

checkv_dir = sys.argv[1]
faa_dir = sys.argv[2]
out_dir = sys.argv[3]
key_w = 'holin'
list_dir = os.listdir(checkv_dir)

if not os.path.exists(out_dir):
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
    return s

# Regex for case-insensitive and isolated 'holin'
holin_pattern = re.compile(r'\bholin\b', re.IGNORECASE)

for phage_dir in list_dir:
    phage_name = phage_dir.strip('_vbrant.fasta')
    list_tite = []
    list_none = []

    if os.path.exists(f'{checkv_dir}/{phage_dir}/proviruses.fna'):
        with open(f'{checkv_dir}/{phage_dir}/proviruses.fna', 'r') as f:
            for line in f:
                if line.startswith('>'):
                    list_tite.append(line.strip('\n'))
    else:
        print(f'{checkv_dir}/{phage_dir}/proviruses.fna')

    if os.path.exists(f'{checkv_dir}/{phage_dir}/quality_summary.tsv'):
        with open(f'{checkv_dir}/{phage_dir}/quality_summary.tsv', 'r') as f:
            list_temp = f.read().strip('\n').split('\n')[1:]
            for i in list_temp:
                if i.split('\t')[7] == 'Not-determined':
                    list_none.append(i.split('\t')[0])
    else:
        print(f'{checkv_dir}/{phage_dir}/quality_summary.tsv')
        print('No provirus')
        continue

    with open(f'{faa_dir}/{phage_name}.faa', 'r') as d:
        con_faa = d.read()
        seqs = con_faa.strip('\n').strip('>').split('\n>')
        out_seqs = []
        dic = {}

    if not con_faa.strip('\n'):
        print('Sequence file is empty')
        continue

    for seq in seqs:
        head = seq.split('\n')[0]
        content = '\n'.join(seq.split('\n')[1:])
        contig_pp = head.split('|')[1] + '|' + head.split('|')[2]
        if get_pp(contig_pp) in list_none:
            continue

        contig = head.split('|')[1]
        sites = head.split('|')[4].strip('complement(').strip(')').replace('>', '').replace('<', '')
        left = int(sites.split('..')[0])
        right = int(sites.split('..')[1])
        pp = get_pp(head.split('|')[2])

        k = 0
        if not list_tite:
            k = 1

        for de_title in list_tite:
            contig_de = de_title.split('|')[0].strip('>')
            pp_de = get_pp(de_title.split('|')[1].split(' ')[0])
            range_de = de_title.split(' ')[-1].split('/')[0]
            l_de = int(range_de.split('-')[0])
            r_de = int(range_de.split('-')[-1])

            if pp == pp_de and contig_de == contig:
                if left >= l_de and right <= r_de:
                    k = 1
                    break
            else:
                k = 1

        if k == 1:
            dic[head] = content.strip('\n')
            out_seqs.append(head)

    for ind in range(len(out_seqs)):
        if re.search(holin_pattern, out_seqs[ind]):  # Case-insensitive and exact match
            if ind - 1 in range(len(out_seqs)) and not re.search(holin_pattern, out_seqs[ind - 1]):
                out_seqs[ind - 1] = out_seqs[ind - 1] + '(+)'

            if ind + 1 in range(len(out_seqs)) and not re.search(holin_pattern, out_seqs[ind + 1]):
                out_seqs[ind + 1] = out_seqs[ind + 1] + '(-)'

    with open(f'{out_dir}/{phage_name}.faa', 'w') as f_out:
        for title in out_seqs:
            f_out.write('>' + title + '\n')
            try:
                f_out.write(dic[strip_(title)].strip('\n') + '\n')
            except KeyError:
                print(title)
                print(strip_(title))
                print('-----------------------------------')

