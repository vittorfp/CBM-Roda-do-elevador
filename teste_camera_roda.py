import pypylon
import imutils
import time
import numpy as np
import cv2


def getParams():
	fh = open("parameters.txt", "r") 
	params = fh.readlines()
	fh.close()
	params = map(lambda s: int(s.strip()), params)

	#print(params)
	if(len(params) == 10):
		(inicio_x, inicio_y, fim_x, fim_y, ci_min,ci_max,ci_sens,ce_min,ce_max,ce_sens) = params
		return (inicio_x, inicio_y, fim_x, fim_y, ci_min,ci_max,ci_sens,ce_min,ce_max,ce_sens)
	else:
		return None


def template_match(img,template):
	found = None
	#print(template.shape)
	#print(img.shape)

	for scale in np.linspace(0.2, 1.0, 30)[::-1]:

		resized = imutils.resize(img, width = int(img.shape[1] * scale))
		r = img.shape[1] / float(resized.shape[1])
 		
		if resized.shape[0] < tH or resized.shape[1] < tW:
			break

		resized = cv2.GaussianBlur(resized,(3,3),0)
		#edged = cv2.Canny(resized, 30, 50)
	
		result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
 		
		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
 	
 	return found



def plot_circles(circles, output):
	if circles is not None:
		#print(circles[0])

		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")

		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)


def proc_image(image):

	global inicio_x, inicio_y, fim_x, fim_y, ci_min,ci_max,ci_sens,ce_min,ce_max,ce_sens, templatem, tH, tW

	#image = imutils.resize(image, width = int(image.shape[1] * 0.8))
	image = image[inicio_y:fim_y,inicio_x:fim_x]
	## To-DO template matching da roda
	# Retorna -1 se nao for roda
	a = template_match(image,template)
	#print(a)
	if(a is None):
		pass
	else:
		(maxVal, maxLoc, r) = a
	(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
	(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
	
	output = image.copy()
	#output = cv2.equalizeHist(image)
	# define o limiar de deteccao da roda
	print(maxVal)
	if( maxVal < 51553404*2 ):
		return output
	cv2.imwrite('img/rodas/Roda '+time.ctime()+'.jpg',image)
	print("Roda")


	#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image_c = cv2.GaussianBlur(image,(3,3),0)


	#image = edged


	# detecta o circulo externo
	circles1 = cv2.HoughCircles(image_c, cv2.HOUGH_GRADIENT, ci_sens , 700, maxRadius = ci_max, minRadius = ci_min)
	#circles1 = None

	# detecta a interface entre a borracha e o ferro
	circles2 = cv2.HoughCircles(image_c, cv2.HOUGH_GRADIENT, ce_sens , 700, maxRadius = ce_max, minRadius = ce_min)
	#circles2 = None

	plot_circles(circles1,output)
	plot_circles(circles2,output)

	#cv2.imshow("Circulos",  output )
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()



	# Isola a borracha na foto
	# poderia ser feito uma mascara de tamanho fixo, mas fiz essa baseada no tamanho
	# do circulo detectado pois estou fazendo testes em imagens de tamanhos diferentes
	total = 0
	if (circles1 is not None) and (circles2 is not None):

		borracha_ferro = circles1[0,0]
		externo = circles2[0,0]
		print(externo)
		print(borracha_ferro)
		rachaduras = image.copy()
		for x in range( image.shape[1] ):
			for y in range( image.shape[0] ):

				dist = np.sqrt( (x - externo[0])**2 + (y - externo[1])**2 )
				if not(( dist >= borracha_ferro[2] ) & ( dist <= externo[2] )):
					rachaduras[y,x] = 0
				else:
					total += 1

		cv2.imshow("Crop",  rachaduras )
		cv2.waitKey(1)
		#cv2.destroyAllWindows()

		# TO DO: Fazer canny line detection na parte da borracha.
		edged = cv2.Canny(rachaduras, 25, 30)

		cv2.imshow("Linhas",  edged )
		cv2.waitKey(1)
		#cv2.destroyAllWindows()


		brancos = (np.sum(edged)/255).astype(float)
		#total = edged.shape[0] * edged.shape[1]

		percentual = brancos/ (float(total)*0.75)
		print( str(percentual*100.0)+'%')
	return output


(inicio_x, inicio_y, fim_x, fim_y, ci_min,ci_max,ci_sens,ce_min,ce_max,ce_sens) = getParams()
de = None

try:
	print('Build against pylon library version:', pypylon.pylon_version.version)
	available_cameras = pypylon.factory.find_devices()
	print('Available cameras are', available_cameras)
	cam = pypylon.factory.create_device(available_cameras[-1])
	print('Camera info of camera object:', cam.device_info)
	cam.open()
	for img in cam.grab_images(1):
		print("Imagem capturada")
except:
	print("Falha na comunicacao com a camera")
	exit(1)
	de = cv2.imread('img/roda-real.bmp')

template = cv2.imread('img/template_roda.jpg')
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
(tH, tW) = template.shape[:2]


while True:
	for image in cam.grab_images(1):
		#print(image.shape)
		result = proc_image(image)
		try:
			cv2.imshow('frame',result)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		except:
			cv2.destroyAllWindows()
			break

cv2.destroyAllWindows()
