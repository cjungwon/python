import cv2
import numpy as np
import json


def show_image(json_file, image_file):

  with open(json_file, 'r') as f:
    json_data = json.load(f)

  bar_index = []
  dot_index = []
  res_array = json_data.get('images')

  for list in res_array:
    list_set = list.get('fields')
    
    for n in range(len(list_set)):
      if '-' in list_set[n].get('inferText'):
        bar_index.append(n)

      if '.' in list_set[n].get('inferText'):
        dot_index.append(n)


  lecense_num_bounding1 = list_set[bar_index[0]].get('boundingPoly').get('vertices')[0]
  lecense_num_bounding2 = list_set[bar_index[0]].get('boundingPoly').get('vertices')[2]

  name_bounding1 = list_set[bar_index[0] + 1].get('boundingPoly').get('vertices')[0]
  name_bounding2 = list_set[bar_index[0] + 1].get('boundingPoly').get('vertices')[2]

  id_num_bounding1 = list_set[bar_index[1]].get('boundingPoly').get('vertices')[0]
  id_num_bounding2 = list_set[bar_index[1] + 1].get('boundingPoly').get('vertices')[2]

  date_bounding1 = list_set[dot_index[len(dot_index) - 2]].get('boundingPoly').get('vertices')[0]
  date_bounding2 = list_set[dot_index[len(dot_index) - 1]].get('boundingPoly').get('vertices')[2]



  img = cv2.imread(image_file, cv2.IMREAD_COLOR)

  # license_num
  cv2.rectangle(img, (int(lecense_num_bounding1.get('x')), int(lecense_num_bounding1.get('y'))),
                    (int(lecense_num_bounding2.get('x')), int(lecense_num_bounding2.get('y'))), (0, 0, 255), 2)
  # name
  cv2.rectangle(img, (int(name_bounding1.get('x')), int(name_bounding1.get('y'))),
                   (int(name_bounding2.get('x')), int(name_bounding2.get('y'))), (0, 0, 255), 2)
  # id_num
  cv2.rectangle(img, (int(id_num_bounding1.get('x')), int(id_num_bounding1.get('y'))),
                   (int(id_num_bounding2.get('x')), int(id_num_bounding2.get('y'))), (0, 0, 255), 2)
  # date
  cv2.rectangle(img, (int(date_bounding1.get('x')), int(date_bounding1.get('y'))),
                   (int(date_bounding2.get('x')), int(date_bounding2.get('y'))), (0, 0, 255), 2)

  cv2.namedWindow('Mobile_D', cv2.WINDOW_NORMAL)
  cv2.imshow('Mobile_D', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  

json_file = input("json file : ")
  # D:/test/Mobile_D.json
image_file = input("image file : ")
  # D:/test/Mobile_D__sample.jpg
show_image(json_file, image_file)