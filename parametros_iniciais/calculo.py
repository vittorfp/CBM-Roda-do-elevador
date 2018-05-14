import numpy as np
import argparse
import imutils
import cv2



edged = cv2.imread('rachaduras.png')
cv2.imshow("output",  edged )
cv2.waitKey(0)

print(np.max(edged))
brancos = (np.sum(edged)/255).astype(float)
print(brancos)
#total = 70762.0 * 0.75
total = 60896.0
print(total)
percentual = brancos/total
print(percentual)
print( str(percentual*100.0)+'% degradada')