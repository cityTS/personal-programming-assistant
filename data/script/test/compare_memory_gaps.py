import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


# 定义不同行数的数据生成函数
def generate_random_strings(num_rows, min_len=20, max_len=200):
    strings = []
    for _ in range(num_rows):
        length = np.random.randint(min_len, max_len + 1)
        string = ''.join(np.random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'], size=length))
        strings.append(string)
    return strings


# 定义数据行数
rows_counts = [10000, 50000, 100000]
feather_sizes = []
original_sizes = []

# 生成数据，转换为Feather格式，计算大小
for num_rows in rows_counts:
    # strings = generate_random_strings(num_rows)
    # df = pd.DataFrame({'strings': strings})
    txt_file = f'data_{num_rows}_rows.txt'
    # with open(txt_file, 'w', encoding='utf-8') as f:
    #     for string in strings:
    #         f.write(string)
    # # 保存为Feather格式
    feather_file = f'data_{num_rows}_rows.feather'
    # df.to_feather(feather_file)

    # 记录原始数据大小（字节）
    original_size = os.path.getsize(txt_file)  # 将字符串转换为字节
    original_sizes.append(original_size)

    # 记录Feather文件大小
    feather_size = os.path.getsize(feather_file)
    feather_sizes.append(feather_size)

print(original_sizes)
print(feather_sizes)

# 计算节省的内存
memory_saved = [original - feather for original, feather in zip(original_sizes, feather_sizes)]
print(memory_saved)
# 通过柱状图展示优化了多少内存
plt.figure(figsize=(12, 6))
plt.bar([str(x) for x in rows_counts], memory_saved, color='skyblue')
plt.xlabel('Number of Rows')
plt.ylabel('Memory Saved (bytes)')
plt.title('Memory Optimization by Feather Format for Random Strings Data')
for i in range(len(rows_counts)):
    plt.text(i, memory_saved[i], str(memory_saved[i]), ha='center', va='bottom')
plt.show()


baifenbi = [(original - feather) * 100 / original for original, feather in zip(original_sizes, feather_sizes)]

plt.figure(figsize=(12, 6))
plt.bar([str(x) for x in rows_counts], baifenbi, color='skyblue')
plt.xlabel('Number of Rows')
plt.ylabel('Memory Saved Percent(%)')
plt.title('Memory Optimization by Feather Format for Random Strings Data')
for i in range(len(rows_counts)):
    plt.text(i, baifenbi[i], str(baifenbi[i]), ha='center', va='bottom')
plt.show()