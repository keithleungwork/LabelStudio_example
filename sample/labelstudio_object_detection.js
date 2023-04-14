/*
The whole json for project in label studio
*/

sample = [
  // One object for one image
  {
    "data": {
      // This key "image" has to match the data source in the project layout config (object tag)
      "image": "\/data\/local-files\/?d=images\/xxxxxx.png"
    },
    "annotations": [
      {
          "result": [
              {
                  // These shouldmatch the variable name configured in the project layout
                  "from_name": "label",
                  "to_name": "image",
                  // for bbox
                  "type": "rectanglelabels",
                  "readonly": false,
                  "hidden": false,
                  // bbox value
                  "value": {
                      /*
                        Convert the coord to LabelStudio format : 
                        https://labelstud.io/guide/export.html#Units-of-image-annotations
                      */
                      "x": 1.98353434543354,
                      "y": 1.182699319824755,
                      "width": 1.744857771491816,
                      "height": 1.990079355543569,
                      // Not mentioned in the document but it is required. Otherwise cannot export in UI.
                      "original_width": 1234,
                      "original_height": 1234,
                      "rotation": 0,
                      "rectanglelabels": ["some_label_xxxx"]
                  }
              }
              // Other bbox annotation in the same images....
          ]
      }
    ],
  }
]