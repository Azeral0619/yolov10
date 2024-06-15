import os
import shutil


def move_unannotated_images(image_dir, xml_dir, target_dir):
    xml_files = set(f[:-4] for f in os.listdir(xml_dir) if f.endswith(".xml"))
    for image_file in os.listdir(image_dir):
        if image_file.endswith(".jpg") and image_file[:-4] not in xml_files:
            shutil.move(os.path.join(image_dir, image_file), os.path.join(target_dir, image_file))


image_dir = "data/keyframes"
xml_dir = "data/annotations_xml"
target_dir = "data/background"
if not os.path.isdir(target_dir):
    os.mkdir(target_dir)
move_unannotated_images(image_dir, xml_dir, target_dir)
