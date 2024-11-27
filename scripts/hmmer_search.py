import os
import argparse

def main(input_dir, output_dir, threads):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 遍历输入目录中的所有文件
    count = 1
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.hmm'):  # 确保只处理 .hmm 文件
            print(f"Processing {file_name} ({count})")
            name = file_name.split('.hmm')[0]
            input_file = os.path.join(input_dir, file_name)
            output_file = os.path.join(output_dir, f"{name}.out")

            # 构建并执行 hmmsearch 命令
            cmd = f"hmmsearch --cpu {threads} -E 0.00001 {input_file} ../hmmer-input-uniq/hmmer_in_seq_uniq.faa > {output_file}"
            #print(f"Running: {cmd}")
            os.system(cmd)

            count += 1

if __name__ == "__main__":
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="Run hmmsearch for all .hmm files in a directory.")
    parser.add_argument('-d', '--database', type=str, default='../hmmer_mod', help="Input directory containing .hmm files (default: ../hmmer_mod)")
    parser.add_argument('-o', '--output', type=str, default='./out', help="Output directory for results (default: ./out)")
    parser.add_argument('-t', '--threads', type=int, default=10, help="Number of threads for hmmsearch (default: 10)")

    args = parser.parse_args()

    # 调用主函数
    main(input_dir=args.database, output_dir=args.output, threads=args.threads)
