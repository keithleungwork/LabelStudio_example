import json
import os
import xml.etree.ElementTree as ET


# Name of the tag used to label the region. See control tags.
LS_RESULT_FROM_NAME = "label"
# Name of the object tag that provided the region to be labeled. See object tags.
LS_RESULT_TO_NAME = "image"
# Type of tag used to annotate the task.
LS_RESULT_TYPE = "rectanglelabels"
LS_RESULT_READONLY = False
LS_RESULT_HIDDEN = False


# convert from pixels to LS percent units
def convert_to_ls(x, y, width, height, original_width, original_height):
    return x / original_width * 100.0, y / original_height * 100.0, width / original_width * 100.0, height / original_height * 100


def parse_pascal_voc_annotation(xml_path: str, ls_img_path: str):
    """
    Parse an annotation in Pascal VOC format and return the annotations & images for LabelStudio.

    Args:
        xml_path (str): Path to the annotation file in Pascal VOC format.
        ls_img_path (str): Path to the image file within the LabelStudio container. Relative to LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT

    Returns:
        dict: dict for Labelstudio format
    """

    tree = ET.parse(xml_path)
    root = tree.getroot()

    filename = root.find('filename').text
    size_elem = root.find('size')
    width = int(size_elem.find('width').text)
    height = int(size_elem.find('height').text)

    # an template object each images
    ls_output = {
        "data": {
            "image": "/data/local-files/?d=" + os.path.join(ls_img_path, filename)
        },
        "annotations": [],
    }

    # Prepare annotation list
    bbox_l = []
    for obj in root.findall('object'):
        xml_bbox = obj.find('bndbox')
        xmin = int(xml_bbox.find('xmin').text)
        ymin = int(xml_bbox.find('ymin').text)
        xmax = int(xml_bbox.find('xmax').text)
        ymax = int(xml_bbox.find('ymax').text)
        label = obj.find('name').text

        # Convert the coord to LabelStudio format : https://labelstud.io/guide/export.html#Units-of-image-annotations
        ls_x, ls_y, ls_w, ls_h = convert_to_ls(
            xmin,
            ymin,
            xmax - xmin,
            ymax - ymin,
            width,
            height
        )

        bbox = {
            # modify according to label studio config
            "from_name": LS_RESULT_FROM_NAME,
            "to_name": LS_RESULT_TO_NAME,
            "type": LS_RESULT_TYPE,
            "readonly": LS_RESULT_READONLY,
            "hidden": LS_RESULT_HIDDEN,
            "value": {
                "x": ls_x,
                "y": ls_y,
                "width": ls_w,
                "height": ls_h,
                # These 2 fields are required although original doc didn't say
                "original_width": width,
                "original_height": height,
                "rotation": 0,
                "rectanglelabels": [label]
            }
        }
        bbox_l.append(bbox)

    ls_output["annotations"] = [{"result": bbox_l}]
    return ls_output


def convert_pascal_voc_to_ls(ann_dir: str, output_path: str, ls_img_base_path: str):
    """
    Convert a directory of annotations in Pascal VOC format to the acceptable JSON file for LabelStudio.

    Args:
        ann_dir (str): Path to the directory containing the annotations in Pascal VOC format.
        output_path (str): Path to the output JSON file.
    """

    # The final json array for all images
    final_json = []

    for xml_file in os.listdir(ann_dir):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(ann_dir, xml_file)
            # Convert pascal into LS object
            ls_obj = parse_pascal_voc_annotation(xml_path, ls_img_base_path)
            final_json.append(ls_obj)

    with open(output_path, 'w') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)

    print(f'Annotations saved to {output_path}')


# Example usage
ann_dir = 'tmp/v2/xml/'
output_path = 'tmp/v2/ls_annotations.json'
ls_img_p = "v2/images"
convert_pascal_voc_to_ls(ann_dir, output_path, ls_img_p)
