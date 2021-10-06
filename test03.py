import cv2
import numpy as np


def showimage():
  imgfile = 'Mobile_D__sample.jpg'
  img = cv2.imread(imgfile, cv2.IMREAD_COLOR)

  cv2.rectangle(img, (547, 295), (983, 349), (0, 0, 255), 2)
  cv2.rectangle(img, (545, 363), (666, 408), (0, 0, 255), 2)
  cv2.rectangle(img, (545, 409), (858, 444), (0, 0, 255), 2)
  cv2.rectangle(img, (551, 701), (705, 725), (0, 0, 255), 2)

  cv2.namedWindow('Mobile_D', cv2.WINDOW_NORMAL)
  cv2.imshow('Mobile_D', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  
showimage()


