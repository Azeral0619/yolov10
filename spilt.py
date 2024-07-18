import os
import random


ratio = 0.2
label_dir = "data/labels"  # 生成的yolo格式的数据存放路径
image_dir = "data/images"

# 获取所有标签文件名
files = os.listdir(label_dir)
random.seed(0)
# 打乱文件顺序
random.shuffle(files)

# 计算验证集的大小
val_size = int(len(files) * ratio)

# 分割文件名为训练集和验证集
val_files = files[:val_size]
train_files = files[val_size:]


# 定义写入文件路径的函数
def write_file(file_list, filename, image_dir):
    with open(filename, "w") as f:
        for file in file_list:
            # 替换标签文件扩展名为图像文件扩展名
            image_file = file.replace(".txt", ".jpg")
            f.write(os.path.join(image_dir, image_file) + "\n")


# 写入train.txt, val.txt, all.txt
write_file(train_files, "data/train.txt", image_dir)
write_file(val_files, "data/val.txt", image_dir)
write_file(files, "data/all.txt", image_dir)
