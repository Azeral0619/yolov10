import xml.etree.ElementTree as ET
import os
import random

classes = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "G",
    "I",
    "J",
    "L",
    "M",
    "O",
    "Q",
    "X",
    "Y",
    "Z",
]


def clear_hidden_files(path):
    dir_list = os.listdir(path)
    for i in dir_list:
        abspath = os.path.join(os.path.abspath(path), i)
        if os.path.isfile(abspath):
            if i.startswith("._"):
                os.remove(abspath)
        else:
            clear_hidden_files(abspath)


def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(image_id, voc_labels, yolo_labels):
    in_file = open(os.path.join(voc_labels + "%s.xml") % image_id)
    out_file = open(os.path.join(yolo_labels + "%s.txt") % image_id, "w")
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)

    for obj in root.iter("object"):
        difficult = obj.find("difficult").text
        cls = obj.find("name").text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xml_box = obj.find("bndbox")
        b = (
            float(xml_box.find("xmin").text),
            float(xml_box.find("xmax").text),
            float(xml_box.find("ymin").text),
            float(xml_box.find("ymax").text),
        )
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + "\n")
    in_file.close()
    out_file.close()


if __name__ == "__main__":
    # 获取当前路径
    wd = os.getcwd()
    # 创建相应VOC模式文件夹
    voc_path = os.path.join(wd, "data")
    if not os.path.isdir(voc_path):
        os.mkdir(voc_path)

    annotation_dir = os.path.join(voc_path, "annotations_xml/")
    if not os.path.isdir(annotation_dir):
        os.mkdir(annotation_dir)
    clear_hidden_files(annotation_dir)

    image_dir = os.path.join(voc_path, "keyframes/")
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    clear_hidden_files(image_dir)

    voc_file_dir = os.path.join(voc_path, "ImageSets/")
    if not os.path.isdir(voc_file_dir):
        os.mkdir(voc_file_dir)

    voc_file_dir = os.path.join(voc_file_dir, "Main/")
    if not os.path.isdir(voc_file_dir):
        os.mkdir(voc_file_dir)

    VOC_train_file = open(os.path.join(voc_path, "train.txt"), "w")
    VOC_test_file = open(os.path.join(voc_path, "test.txt"), "w")
    VOC_train_file.close()
    VOC_test_file.close()

    if not os.path.exists(os.path.join(voc_path, "Labels/")):
        os.makedirs(os.path.join(voc_path, "Labels"))

    train_file = open(os.path.join(voc_path, "2007_train.txt"), "a")
    test_file = open(os.path.join(voc_path, "2007_test.txt"), "a")
    VOC_train_file = open(os.path.join(voc_path, "train.txt"), "a")
    VOC_test_file = open(os.path.join(voc_path, "test.txt"), "a")

    image_list = os.listdir(image_dir)  # list image files
    probo = random.randint(1, 100)
    print("Probobility: %d" % probo)
    for i in range(0, len(image_list)):
        path = os.path.join(image_dir, image_list[i])
        if os.path.isfile(path):
            image_path = image_dir + image_list[i]
            image_name = image_list[i]
            (name_without_extent, extent) = os.path.splitext(os.path.basename(image_path))
            voc_name_without_extent, voc_extent = os.path.splitext(os.path.basename(image_name))
            annotation_name = name_without_extent + ".xml"
            annotation_path = os.path.join(annotation_dir, annotation_name)
        probo = random.randint(1, 100)
        print("Probobility: %d" % probo)
        if probo < 90:
            if os.path.exists(annotation_path):
                train_file.write(image_path + "\n")
                VOC_train_file.write(voc_name_without_extent + "\n")
                yolo_labels_dir = os.path.join(voc_path, "Labels/")
                convert_annotation(name_without_extent, annotation_dir, yolo_labels_dir)
        else:
            if os.path.exists(annotation_path):
                test_file.write(image_path + "\n")
                VOC_test_file.write(voc_name_without_extent + "\n")
                yolo_labels_dir = os.path.join(voc_path, "Labels/")
                convert_annotation(name_without_extent, annotation_dir, yolo_labels_dir)

    train_file.close()
    test_file.close()
    VOC_train_file.close()
    VOC_test_file.close()
