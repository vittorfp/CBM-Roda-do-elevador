import numpy as np
import argparse
import imutils
import cv2

def init_matrix(img):
	d = np.zeros( (img.shape[0] , img.shape[1], 2) )
	for x in range( img.shape[1] ):
		for y in range( img.shape[0] ):
			d[x,y,:] = [x,y]

	return d

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--save", help = "Image to save")
args = vars( ap.parse_args() )

image = cv2.imread('img/img5.jpg')[000:1100,:,:]

image = imutils.resize(image, width = int(image.shape[1] * 0.8))
output = image.copy()


image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.GaussianBlur(image,(3,3),0)


#image = edged

# detecta o circulo interno da roda
circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 3 ,700, maxRadius = 250, minRadius = 150)

# detecta o circulo externo
circles1 = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 3 , 600, maxRadius = 350, minRadius = 250)
#circles1 = None

# detecta a interface entre a borracha e o ferro
#circles2 = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.4 , 700, maxRadius = 310, minRadius = 270)
circles2 = None

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
borracha_ferro = circles[0]

#d = init_matrix(output)
#dist = np.sqrt( ( d[:,:,1] - externo[0]) ** 2 + ( d[:,:,0] - externo[1]) ** 2 )
#zera = ( dist <= borracha_ferro[2] ) | ( dist >= externo[2] )
#output[zera] = 0


'''
payload='{ \"data\":'+str(time.time() - 10800)+', \"valor\":[{ \"corrente\":'+ str(percentual) +',\"rachaduras\":4}] }', \
soma = 0
rachaduras = image.copy()
for x in range( image.shape[1] ):
	for y in range( image.shape[0] ):

		dist = np.sqrt( (x - externo[0])**2 + (y - externo[1])**2 )
		if not(( dist >= borracha_ferro[2] ) & ( dist <= externo[2] )):
			rachaduras[y,x] = 0
		else:
			soma += 1


print(soma)

cv2.imshow("output",  rachaduras )
cv2.waitKey(0)
'''
#cv2.imwrite('img/borracha1.jpg', rachaduras )

# TO DO: Fazer canny line detection na parte da borracha.
edged = cv2.Canny(output, 30, 40)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
edged = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
		
cv2.imshow("output",  edged )
cv2.waitKey(0)