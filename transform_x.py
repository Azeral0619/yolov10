import glob
import os


original_labels = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "A",
    11: "B",
    12: "C",
    13: "D",
    14: "E",
    15: "G",
    16: "I",
    17: "J",
    18: "L",
    19: "M",
    20: "O",
    21: "Q",
    22: "X",
    23: "Y",
    24: "Z",
}

# 定义新数据集的标签
new_labels = {
    0: "1",
    1: "2",
    2: "3",
}


label_mapping = {value: key for key, value in new_labels.items()}


def convert_label(original_label_line):
    parts = original_label_line.split()
    original_label = int(parts[0])
    if str(original_label) in label_mapping.keys():
        new_label = label_mapping[original_labels[original_label]]
    else:
        new_label = 3
    print(original_label, new_label)
    parts[0] = str(new_label)
    return " ".join(parts)


def process_files(directory):
    # 找到目录下的所有.txt文件
    for filepath in glob.glob(os.path.join(directory, "*.txt")):
        with open(filepath, "r") as file:
            lines = file.readlines()

        # 转换每一行
        converted_lines = [convert_label(line) + "\n" for line in lines]

        # 将转换后的内容写回文件
        with open(filepath, "w") as file:
            file.writelines(converted_lines)


process_files("data/labels")
