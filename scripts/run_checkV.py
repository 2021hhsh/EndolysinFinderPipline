import os
from multiprocessing import Pool
import subprocess
import argparse


# 核心函数
def run(name):
    # 创建输出目录
    output_path = os.path.join(output_dir, name)
    os.makedirs(output_path, exist_ok=True)

    # 执行 CheckV 分析
    cmd = [
        'checkv', 'end_to_end',
        f'{input_dir}/{name}', output_path,
        '-d', checkv_db, '-t', str(num_threads)
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    # 检查执行结果
    if result.returncode != 0:
        print(f"Error: CheckV failed for {name}")
    else:
        print(f"Completed: {name}")


# 主函数
if __name__ == '__main__':
    # 参数解析
    parser = argparse.ArgumentParser(description="Run CheckV pipeline with multiprocessing.")
    parser.add_argument('-i', '--input', type=str, required=True, help="Input directory containing files")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output directory for CheckV results")
    parser.add_argument('-d', '--database', type=str, default='../checkv_db/checkv-db-v1.5',
                        help="Path to CheckV database (default: ../checkv_db/checkv-db-v1.5)")
    parser.add_argument('-n', '--processes', type=int, default=1, help="Number of parallel processes (default: 1)")
    parser.add_argument('-t', '--threads', type=int, default=10, help="Number of threads per process (default: 10)")

    args = parser.parse_args()

    # 参数变量
    input_dir = args.input
    output_dir = args.output
    checkv_db = args.database
    num_processes = args.processes
    num_threads = args.threads

    # 检查输入目录
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        exit(1)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 获取文件列表
    file_list = [f for f in os.listdir(input_dir)]
    if not file_list:
        print(f"Error: No files found in input directory '{input_dir}'.")
        exit(1)

    print(f"Starting CheckV pipeline with {num_processes} processes and {num_threads} threads per process.")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"CheckV database: {checkv_db}")
    print(f"Files to process: {len(file_list)}")

    # 多进程处理
    pool = Pool(processes=num_processes)
    pool.map(run, file_list)
    pool.close()
    pool.join()

    print("All tasks completed.")
