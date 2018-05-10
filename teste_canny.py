# Teste com a roda nova

import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--save", help = "Image to save")
args = vars(ap.parse_args())

rachaduras = cv2.imread('img/borracha1.jpg')


# TO DO: Fazer canny line detection na parte da borracha.
edged = cv2.Canny(rachaduras, 30, 40)
cv2.imshow("output",  edged )
cv2.waitKey(0)