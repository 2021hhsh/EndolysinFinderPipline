import os
import argparse

def main(database, input_file, output_dir, threads):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 设置输出文件路径
    result_txt = os.path.join(output_dir, "result.txt")
    result_tbl = os.path.join(output_dir, "result.tbl")
    result_dom = os.path.join(output_dir, "result.dom")

    # 构建 hmmscan 命令
    cmd = (
        f"hmmscan --cpu {threads} -o {result_txt} "
        f"--tblout {result_tbl} --domtblout {result_dom} --noali -E 1e-5 {database} {input_file}"
    )

    # 打印并执行命令
    print(f"Running: {cmd}")
    os.system(cmd)
    print("hmmscan completed successfully.")

if __name__ == "__main__":
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="Run hmmscan with custom database, input, output, and thread options.")
    parser.add_argument('-d', '--database', type=str, default="~/miniconda3/envs/new_vibrant/share/vibrant-1.2.1/db/databases/Pfam-A_v32.HMM", help="Path to HMM database (default: Pfam-A_v32.HMM)")
    parser.add_argument('-i', '--input', type=str, default="out_seq.fa", help="Input file for hmmscan (default: out_seq.fa)")
    parser.add_argument('-o', '--output', type=str, default="result", help="Output directory (default: result)")
    parser.add_argument('-t', '--threads', type=int, default=10, help="Number of threads (default: 10)")

    args = parser.parse_args()

    # 调用主函数
    main(database=args.database, input_file=args.input, output_dir=args.output, threads=args.threads)
