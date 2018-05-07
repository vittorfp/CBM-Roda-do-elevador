import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--save", help = "Image to save")
args = vars(ap.parse_args())

image = cv2.imread('img/img3.jpg')[300:1100,:,:]

image = imutils.resize(image, width = int(image.shape[1] * 0.8))
output = image.copy()


image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.GaussianBlur(image,(3,3),0)


#image = edged

# detecta o circulo interno da roda
circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1 ,400, maxRadius = 320)

# detecta o circulo externo
circles1 = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.4 , 400, maxRadius = 320, minRadius = 305)
#circles1 = None

# detecta a interface entre a borracha e o ferro
circles2 = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.4 , 700, maxRadius = 310, minRadius = 270)
#circles2 = None

if circles is not None:
	print(circles[0])

	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
 	
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

if circles1 is not None:
	print(circles1[0])

	# convert the (x, y) coordinates and radius of the circles to integers
	circles1 = np.round(circles1[0, :]).astype("int")
 	
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles1:
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

if circles2 is not None:
	print(circles2[0])

	# convert the (x, y) coordinates and radius of the circles to integers
	circles2 = np.round(circles2[0, :]).astype("int")
 	
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles2:
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

cv2.imshow("output",  output )
if args['save'] != None:
	cv2.imwrite(args['save'], np.hstack([image, output]) )
cv2.waitKey(0)


# Isola a borracha na foto
# poderia ser feito uma mascara de tamanho fixo, mas fiz essa baseada no tamanho
# do circulo detectado pois estou fazendo testes em imagens de tamanhos diferentes

externo = circles1[0]
borracha_ferro = circles2[0]

rachaduras = image.copy()
for x in range( image.shape[1] ):
	for y in range( image.shape[0] ):

		dist = np.sqrt( (x - externo[0])**2 + (y - externo[1])**2 )
		if not(( dist >= borracha_ferro[2] ) & ( dist <= externo[2] )):
			rachaduras[y,x] = 0

cv2.imshow("output",  rachaduras )
cv2.waitKey(0)

# TO DO: Fazer canny line detection na parte da borracha.


edged = cv2.Canny(rachaduras, 25, 30)
cv2.imshow("output",  edged )
cv2.waitKey(0)