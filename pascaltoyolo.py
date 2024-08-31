import os
import xml.etree.ElementTree as ET
import argparse

def convert_voc_to_yolo(voc_dir, yolo_dir, classes_file):
    if not os.path.exists(yolo_dir):
        os.makedirs(yolo_dir)

    with open(classes_file, 'r') as f:
        classes = f.read().strip().split()

    for voc_file in os.listdir(voc_dir):
        if voc_file.endswith(".xml"):
            voc_path = os.path.join(voc_dir, voc_file)
            yolo_path = os.path.join(yolo_dir, voc_file.replace(".xml", ".txt"))
            tree = ET.parse(voc_path)
            root = tree.getroot()
            size = root.find('size')
            w = int(size.find('width').text)
            h = int(size.find('height').text)

            with open(yolo_path, 'w') as yolo_file:
                for obj in root.findall('object'):
                    cls = obj.find('name').text
                    if cls not in classes:
                        continue
                    cls_id = classes.index(cls)
                    xmlbox = obj.find('bndbox')
                    b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                         float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                    bb = (b[0] + b[1]) / 2.0 / w, (b[2] + b[3]) / 2.0 / h, (b[1] - b[0]) / w, (b[3] - b[2]) / h
                    yolo_file.write(" ".join([str(cls_id)] + [str(a) for a in bb]) + '\n')

voc_dir = '/content/datasets/datasets/annotations'
yolo_dir = '/content/datasets/datasets/labels'
classes_file = '/content/datasets/datasets/classes.txt'

convert_voc_to_yolo(voc_dir, yolo_dir, classes_file)
