import cv2
import numpy as np
import json

def show_image(json_file, image_file):

    with open(json_file, 'r') as f:
        json_data_R = json.load(f)

    date_index = []
    res_array = json_data_R.get('images')

    for list in res_array:
        list_set = list.get('fields')

    for n in range(len(list_set)):
        if '주민등록증' in list_set[n].get('inferText'):
            name_index = n + 1
            # print(name_index)
        if '-' in list_set[n].get('inferText'):
            id_num_index = n
            # print(id_num_index)
        if '.' in list_set[n].get('inferText'):
            date_index.append(n)

    sort_bounding1 = list_set[name_index-1].get('boundingPoly').get('vertices')[0]
    sort_bounding2 = list_set[name_index-1].get('boundingPoly').get('vertices')[2]

    name_bounding1 = list_set[name_index].get('boundingPoly').get('vertices')[0]
    name_bounding2 = list_set[name_index + 1].get('boundingPoly').get('vertices')[2]

    id_num_bounding1 = list_set[id_num_index].get('boundingPoly').get('vertices')[0]
    id_num_bounding2 = list_set[id_num_index].get('boundingPoly').get('vertices')[2]

    address_bounding1 = list_set[id_num_index+1].get('boundingPoly').get('vertices')[0]
    address_bounding2 = list_set[date_index[0]-1].get('boundingPoly').get('vertices')[2]

    date_bounding1 = list_set[date_index[0]].get('boundingPoly').get('vertices')[0]
    date_bounding2 = list_set[date_index[2]].get('boundingPoly').get('vertices')[2]


    img = cv2.imread(image_file, cv2.IMREAD_COLOR)

    cv2.rectangle(img, (int(sort_bounding1.get('x')), int(sort_bounding1.get('y'))),
                    (int(sort_bounding2.get('x')), int(sort_bounding2.get('y'))), (255, 0, 0), 2)

    cv2.rectangle(img, (int(address_bounding1.get('x')), int(address_bounding1.get('y'))),
                    (int(address_bounding2.get('x'))+40, int(address_bounding2.get('y'))), (255, 0, 0), 2)

    # name
    cv2.rectangle(img, (int(name_bounding1.get('x')), int(name_bounding1.get('y'))),
                    (int(name_bounding2.get('x')), int(name_bounding2.get('y'))), (0, 0, 255), 2)
    # id_num
    cv2.rectangle(img, (int(id_num_bounding1.get('x')), int(id_num_bounding1.get('y'))),
                    (int(id_num_bounding2.get('x')), int(id_num_bounding2.get('y'))), (0, 0, 255), 2)
    # date
    cv2.rectangle(img, (int(date_bounding1.get('x')), int(date_bounding1.get('y'))),
                   (int(date_bounding2.get('x')), int(date_bounding2.get('y'))), (0, 0, 255), 2)

    cv2.namedWindow('Mobile_R', cv2.WINDOW_NORMAL)
    cv2.imshow('Mobile_R', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


json_file = input("json file : ")
  # D:/test/Mobile_R.json
image_file = input("image file : ")
  # D:/test/Mobile_R__sample.jpg
show_image(json_file, image_file)