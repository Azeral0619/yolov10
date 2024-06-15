import os
import xml.etree.ElementTree as ET


def get_all_classes(xml_dir) -> set:
    classes = set()
    for xml_file in os.listdir(xml_dir):
        if xml_file.endswith(".xml"):
            tree = ET.parse(os.path.join(xml_dir, xml_file))
            root = tree.getroot()
            for member in root.findall("object"):
                classes.add(member.find("name").text)
    return classes


xml_dir = "data/annotations"
all_classes = sorted(list(get_all_classes(xml_dir)))
print(all_classes)
