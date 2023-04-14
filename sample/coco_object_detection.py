"""
Here is the sample of REQUIRED fields
"""
sample = {
    "images": [
        {
            "id": 242287,
            "width": 426,
            "height": 640,
            "file_name": "xxxxxxxxx.jpg",
            "date_captured": "2013-11-15 02:41:42"
        }
    ],
    # There is an annotation object for each instance of an object on an image.
    "annotations": [
        {
            "id": 125686,
            "image_id": 242287,  # Corresponds to the image id in the images array.
            "category_id": 0,  # It maps to the id field of the categories array.
            "iscrowd": 0,  # Specifies if the image contains a crowd of objects.
            # [x,y,width,height] from top-left corner, in pixels, of a bbox around an object on the image.
            "bbox": [19.23, 383.18, 314.5, 244.46]
        }
    ],
    "categories": [
        {
            "id": 0,
            "name": "xxxxx"
        }
    ]
}
