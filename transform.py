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
    15: "F",
    16: "G",
    17: "H",
    18: "I",
    19: "J",
    20: "K",
    21: "L",
    22: "M",
    23: "N",
    24: "O",
    25: "P",
    26: "Q",
    27: "R",
    28: "S",
    29: "T",
    30: "U",
    31: "V",
    32: "W",
    33: "X",
    34: "Y",
    35: "Z",
}


label_mapping = {value: key for key, value in new_labels.items()}


def convert_label(original_label_line):
    parts = original_label_line.split()
    original_label = int(parts[0])
    new_label = label_mapping[original_labels[original_label]]
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
