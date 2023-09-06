import json
import os
import xml.etree.ElementTree as ET
import datetime


def get_cat2id(cat_path: str):
    with open(cat_path, 'r') as f:
        labels_str = f.read().split()
    return {l: i + 1 for i, l in enumerate(labels_str)}


def parse_pascal_voc_annotation(xml_path: str, cat2id: dict, img_id: int, ann_id: int):
    """
    Parse an annotation in Pascal VOC format and return the annotations & images with COCO-style keys.

    Args:
        xml_path (str): Path to the annotation file in Pascal VOC format.
        cat2id (dict): The dict with key equal to category name and value is the id
        img_id (int): the image id
        ann_id (int): the annotation starting id

    Returns:
        dict: dict with COCO-style keys for the parsed annotation.
        dict: dict for images
    """

    tree = ET.parse(xml_path)
    root = tree.getroot()

    filename = root.find('filename').text
    size_elem = root.find('size')
    width = int(size_elem.find('width').text)
    height = int(size_elem.find('height').text)

    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    coco_image_obj = {
        "id": img_id,
        "width": width,
        "height": height,
        "file_name": filename,
        "date_captured": formatted_date
    }

    # Prepare annotation list

    bbox_l = []
    for obj in root.findall('object'):
        xml_bbox = obj.find('bndbox')
        xmin = int(xml_bbox.find('xmin').text)
        ymin = int(xml_bbox.find('ymin').text)
        xmax = int(xml_bbox.find('xmax').text)
        ymax = int(xml_bbox.find('ymax').text)
        cid = cat2id[obj.find('name').text]

        bbox = {
            "id": ann_id,
            "image_id": img_id,
            'category_id': cid,
            'bbox': [xmin, ymin, xmax - xmin, ymax - ymin],
            'iscrowd': 0
        }
        bbox_l.append(bbox)
        # increment the bbox id
        ann_id += 1

    return bbox_l, coco_image_obj


def convert_pascal_voc_to_coco(ann_dir, output_path, cat_path):
    """
    Convert a directory of annotations in Pascal VOC format to a COCO-style JSON file.

    Args:
        ann_dir (str): Path to the directory containing the annotations in Pascal VOC format.
        output_path (str): Path to the output JSON file.
    """
    cat2id = get_cat2id(cat_path)

    # modify with your category names and IDs
    categories = [{"id": v, "name": k} for k, v in cat2id.items()]
    coco_data = {
        "images": [],
        "annotations": [],
        "categories": categories
    }

    img_id, bbox_id = 1, 1
    for xml_file in os.listdir(ann_dir):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(ann_dir, xml_file)
            # Convert pascal into COCO object
            bbox_list, image_obj = parse_pascal_voc_annotation(
                xml_path,
                cat2id,
                img_id,
                bbox_id
            )
            coco_data["images"].append(image_obj)
            coco_data["annotations"].extend(bbox_list)
            img_id += 1
            bbox_id += len(bbox_list)

    with open(output_path, 'w') as f:
        json.dump(coco_data, f, ensure_ascii=False, indent=4)

    print(f'Annotations saved to {output_path}')


# Example usage
ann_dir = 'tmp/test/xml/'
output_path = 'tmp/test/coco_annotations.json'
cat_path = 'tmp/labels.txt'
convert_pascal_voc_to_coco(ann_dir, output_path, cat_path)
