# 读取文件内容到一个列表中
with open("hmmer-search-result", "r") as f:
    lines = f.read().strip('\n').split('\n')

# 定义一个字典来存储每个Target ID的结果列表
results = {}

# 遍历每一行，将结果添加到对应的Target ID的列表中
for line in lines:
    fields = line.strip().split('\t')
    # print(line)
    target_id = fields[-2]
    result = tuple(fields)
    if target_id not in results:
        results[target_id] = []
    results[target_id].append(result)

# 对每个Target ID的结果列表按照Score和E-value进行排序，取第一个结果
for target_i, result_list in results.items():
    # items.sort(key=itemgetter("e_value"), reverse=True)
    # items.sort(key=itemgetter("score"))

    sorted_results = sorted(result_list, key=lambda x: float(x[2]), reverse=True)
    sorted_results = sorted(sorted_results, key=lambda x: float(x[1]))

    first_result = sorted_results[0]
    print("\t".join(first_result ))
