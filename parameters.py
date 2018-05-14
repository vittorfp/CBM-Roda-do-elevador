import pypylon
import cv2
import numpy as np
import time

refPt = []
cropping = False
ok = False

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
	img = cv2.imread('img/img4.jpg')
	#exit(1)


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

def nothing(x):
	pass

def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping, ok
 
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True

	elif event == cv2.EVENT_LBUTTONUP:
		refPt.append((x, y))
		cropping = False
		ok = True

		#cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		#cv2.imshow("image", image)



def save(x):
	if(x == 1):
		ci_min = cv2.getTrackbarPos('Circulo Interno (raio minimo)','image')
		ci_max = cv2.getTrackbarPos('Circulo Interno (raio maximo)','image')
		ci_sens= cv2.getTrackbarPos('Circulo Interno (sensibilidade)','image')

		ce_min = cv2.getTrackbarPos('Circulo Externo (raio minimo)','image')
		ce_max = cv2.getTrackbarPos('Circulo Externo (raio maximo)','image')
		ce_sens= cv2.getTrackbarPos('Circulo Externo (sensibilidade)','image')
		inicio = crop[0]
		fim = crop[1]

		fh = open("parameters.txt", "r+") 
		fh.truncate(0)

		# Parametros de cropagem
		fh.write( str(inicio[0]) + '\n' )
		fh.write( str(inicio[1]) + '\n' )
		fh.write( str(fim[0]) + '\n' )
		fh.write( str(fim[1]) + '\n' )

		# Parametros do circulo interno
		fh.write( str(ci_min) + '\n' )
		fh.write( str(ci_max) + '\n' )
		fh.write( str(ci_sens) + '\n' )

		# Parametros do circulo externo
		fh.write( str(ce_min) + '\n' )
		fh.write( str(ce_max) + '\n' )
		fh.write( str(ce_sens) + '\n' )

		fh.close()


cv2.namedWindow('image')
cv2.setMouseCallback("image", click_and_crop)
while(not ok):
	cv2.imshow('image',img)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

	if(len(refPt) == 2):
		print(refPt)
		inicio = refPt[0]
		fim = refPt[1]
		img = img[inicio[1]:fim[1],inicio[0]:fim[0]]
		cv2.destroyAllWindows()
		crop = refPt
		refPt = []
	



cv2.namedWindow('image')
cv2.setMouseCallback("image", click_and_crop)
# create trackbars for color change
cv2.createTrackbar('Circulo Interno (raio minimo)','image',1,500,nothing)
cv2.createTrackbar('Circulo Interno (raio maximo)','image',1,500,nothing)
cv2.createTrackbar('Circulo Interno (sensibilidade)','image',1,20,nothing)

cv2.createTrackbar('Circulo Externo (raio minimo)','image',1,500,nothing)
cv2.createTrackbar('Circulo Externo (raio maximo)','image',1,500,nothing)
cv2.createTrackbar('Circulo Externo (sensibilidade)','image',1,20,nothing)

# create switch for ON/OFF functionality
switch = '0 : Ajustando \n1 : Salvar'
cv2.createTrackbar(switch, 'image', 0 , 1 , save)
#output = img.copy()
while(1):
	
	output = img.copy()
	#image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	image = img.copy()
	
	
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

	ci_min = cv2.getTrackbarPos('Circulo Interno (raio minimo)','image')
	ci_max = cv2.getTrackbarPos('Circulo Interno (raio maximo)','image')
	ci_sens= cv2.getTrackbarPos('Circulo Interno (sensibilidade)','image')

	ce_min = cv2.getTrackbarPos('Circulo Externo (raio minimo)','image')
	ce_max = cv2.getTrackbarPos('Circulo Externo (raio maximo)','image')
	ce_sens= cv2.getTrackbarPos('Circulo Externo (sensibilidade)','image')
	#print (ci_min,ci_max,ci_sens,ce_min,ce_max,ce_sens)
	image = cv2.GaussianBlur(image,(3,3),0)
	try:
		# detecta o circulo interno da roda
		circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, ci_sens ,800, maxRadius = ci_max, minRadius = ci_min)

		# detecta o circulo externo
		circles1 = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, ce_sens , 800, maxRadius = ce_max, minRadius = ce_min)
		
	except:
		print("Zero nao eh um valor permitido para esse parametro")

	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")
	 	
	 	for (x, y, r) in circles:
			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

	if circles1 is not None:
		circles1 = np.round(circles1[0, :]).astype("int")
	 	for (x, y, r) in circles1:
			cv2.circle(output, (x, y), r, (0, 0, 255), 4)
			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
	cv2.imshow('image',output)

cv2.destroyAllWindows()
print( getParams())