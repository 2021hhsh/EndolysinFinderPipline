import os
import argparse
from multiprocessing import Pool
import subprocess

# 运行函数
def run(file_name):
    len_i = len(file_name.split('.'))
    name = '.'.join(file_name.split('.')[:len_i - 1])

    # 创建输出目录
    os.makedirs(f'vibrant-output/{name}', exist_ok=True)

    # 检查是否已运行完成
    if os.path.exists(f'vibrant-output/{name}/run_ok'):
        print(f"Skipping {file_name}: already completed.")
        return

    # 移动文件到目标目录
    print(f"Processing {file_name}...")
    #os.system(f'mv {input_dir}/{file_name} vibrant-output/{name}')

    # 执行 VIBRANT_run.py
    cmd = f'cd vibrant-output/{name}&& ln -s {input_dir}/{file_name} && VIBRANT_run.py -i {file_name} -t {threads} && mkdir -p run_ok'
    print(f"Running command: {cmd}")
    result = os.system(cmd)

    # 检查执行结果
    if result != 0:
        print(f"Error processing {file_name}: VIBRANT_run.py failed.")
    else:
        print(f"Successfully processed {file_name}.")

# 主函数
if __name__ == '__main__':
    # 参数解析
    parser = argparse.ArgumentParser(description="Run VIBRANT pipeline in parallel.")
    parser.add_argument('-i', '--input', type=str, default='./input', help="Input directory (default: ./input)")
    parser.add_argument('-t', '--threads', type=int, default=10, help="Number of threads per process (default: 10)")
    parser.add_argument('-n', '--processes', type=int, default=1, help="Number of parallel processes (default: 3)")

    args = parser.parse_args()
    input_dir = args.input
    threads = args.threads
    processes = args.processes

    # 检查输入目录是否存在
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        exit(1)

    # 获取输入文件列表
    list_files = os.listdir(input_dir)
    if not list_files:
        print(f"Error: No files found in directory '{input_dir}'.")
        exit(1)

    print(f"Starting VIBRANT pipeline with {processes} processes and {threads} threads per process.")
    print(f"Input directory: {input_dir}")
    print(f"Files to process: {len(list_files)}")

    # 使用多进程池处理
    pool = Pool(processes)
    pool.map(run, list_files)
    pool.close()
    pool.join()

    print("All tasks completed.")
