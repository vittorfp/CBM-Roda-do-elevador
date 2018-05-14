import pypylon
import imutils
import numpy as np
import cv2

print('\n\nBuild against pylon library version:', pypylon.pylon_version.version)

available_cameras = pypylon.factory.find_devices()
print('Available cameras are', available_cameras)

# Grep the first one and create a camera for it
cam = pypylon.factory.create_device(available_cameras[-1])

# We can still get information of the camera back
print('Camera info :', cam.device_info)

# Open camera and grep some images
cam.open()

def getParams():
	fh = open("parameters.txt", "r") 
	params = fh.readlines()
	fh.close()
	params = map(lambda s: int(s.strip()), params)

	print(params)
	if(len(params) == 10):
		(inicio_x, inicio_y, fim_x, fim_y, ci_min,ci_max,ci_sens,ce_min,ce_max,ce_sens) = params
		return (inicio_x, inicio_y, fim_x, fim_y, ci_min,ci_max,ci_sens,ce_min,ce_max,ce_sens)
	else:
		return None

(inicio_x, inicio_y, fim_x, fim_y, ci_min,ci_max,ci_sens,ce_min,ce_max,ce_sens) = getParams()

def proc_image(image):

	global inicio_x, inicio_y, fim_x, fim_y, ci_min,ci_max,ci_sens,ce_min,ce_max,ce_sens

	#image = imutils.resize(image, width = int(image.shape[1] * 0.8))
	image = image[inicio_y:fim_y,inicio_x:fim_x]
	output = image.copy()


	#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image_c = cv2.GaussianBlur(image,(3,3),0)


	#image = edged

	# detecta o circulo interno da roda
	#circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1 ,400, maxRadius = 320)
	circles = None

	# detecta o circulo externo
	circles1 = cv2.HoughCircles(image_c, cv2.HOUGH_GRADIENT, ci_sens , 700, maxRadius = ci_max, minRadius = ci_min)
	#circles1 = None

	# detecta a interface entre a borracha e o ferro
	circles2 = cv2.HoughCircles(image_c, cv2.HOUGH_GRADIENT, ce_sens , 700, maxRadius = ce_max, minRadius = ce_min)
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

	cv2.imshow("Circulos",  output )
	cv2.waitKey(0)
	cv2.destroyAllWindows()



	# Isola a borracha na foto
	# poderia ser feito uma mascara de tamanho fixo, mas fiz essa baseada no tamanho
	# do circulo detectado pois estou fazendo testes em imagens de tamanhos diferentes
	total = 0
	if circles1 is not None:
		borracha_ferro = circles1[0]
		externo = circles2[0]

		rachaduras = image.copy()
		for x in range( image.shape[1] ):
			for y in range( image.shape[0] ):

				dist = np.sqrt( (x - externo[0])**2 + (y - externo[1])**2 )
				if not(( dist >= borracha_ferro[2] ) & ( dist <= externo[2] )):
					rachaduras[y,x] = 0
				else:
					total += 1

		cv2.imshow("Crop",  rachaduras )
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		# TO DO: Fazer canny line detection na parte da borracha.
		edged = cv2.Canny(rachaduras, 25, 30)

		cv2.imshow("Linhas",  edged )
		cv2.waitKey(0)
		cv2.destroyAllWindows()


		brancos = (np.sum(edged)/255).astype(float)
		#total = edged.shape[0] * edged.shape[1]

		percentual = brancos/ (float(total)*0.75)
		print( str(percentual*100.0)+'%')
	return output


while True:
	for image in cam.grab_images(1):
		#print(image.shape)
		result = proc_image(image)
		cv2.imshow('frame',result)
		
	if cv2.waitKey(0) & 0xFF == ord('q'):
		break
	cv2.destroyAllWindows()

cv2.destroyAllWindows()
