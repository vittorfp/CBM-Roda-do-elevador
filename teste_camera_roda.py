import pypylon
import imutils
import time
import sys
import cv2
import numpy as np
import interface
from PyQt4 import QtGui, uic

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Como gerar o .py de um .ui
#pyuic4 CBM-RodaGuia/mainwindow.ui > interface.py

class MyWindow(QtGui.QMainWindow, interface.Ui_MainWindow):

	def __init__(self):
		#Esseinicializa a classe mae
		super(MyWindow, self).__init__()
		
		self.setupUi(self)
		#self.show()


	def display_image(self,image, container):
		global inicio_x, inicio_y, fim_x, fim_y
		r = QRect.rect(inicio_x, inicio_y, fim_x, fim_y);
	
		height, width = image.shape	
		byteValue =  1 * width
		#img_inicial = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		scene = QtGui.QGraphicsScene() 
		image = QtGui.QImage(image, height, width,  QtGui.QImage.Format_RGB888)
		scene.addPixmap(QtGui.QPixmap.fromImage(image).copy(inicio_x, inicio_y, fim_x, fim_y) )

		self.foto_inicial.setScene(scene)
		#self.foto_inicial.show()
		if container == 0:
			pass
		scene.update()
		return


	def update_percent(self,percentual):
		self.progressBar.setProperty("value", percentual)
		

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

def log_transform(img,param):
	img = img.astype(np.float) # Cast to float
	c = (img.max()) / (img.max()**(param))
	for i in range(0,img.shape[0]-1):
		for j in range(0,img.shape[1]-1):
			img[i,j] = np.int(c*img[i,j]**(param))

	# Cast back to uint8 for display
	img = img.astype(np.uint8)
	return img

def proc_image(image):

	global d,inicio_x, inicio_y, fim_x, fim_y, ci_min,ci_max,ci_sens,ce_min,ce_max,ce_sens, templatem, tH, tW , window

	#image = imutils.resize(image, width = int(image.shape[1] * 0.8))
	image = image[inicio_y:fim_y,inicio_x:fim_x]
	
	a = template_match(image,template)
	if(a is None):
		pass
	else:
		(maxVal, maxLoc, r) = a

	image = log_transform(image,0.5)
	output = image.copy()
	
	# define o limiar de deteccao da roda
	print(maxVal)
	if( maxVal < 51553404*2 ):
		print("Nao roda")
		return output
	else:
		#cv2.imwrite('img/rodas/Roda '+time.ctime()+'.jpg',image)
		print("Roda")

	#output = cv2.equalizeHist(image)
	#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	print(image)
	image_c = cv2.GaussianBlur(image,(3,3),0)

	# detecta o circulo externo
	circles1 = cv2.HoughCircles(image_c, cv2.HOUGH_GRADIENT, ci_sens , 700, maxRadius = ci_max, minRadius = ci_min)
	
	# detecta a interface entre a borracha e o ferro
	circles2 = cv2.HoughCircles(image_c, cv2.HOUGH_GRADIENT, ce_sens , 700, maxRadius = ce_max, minRadius = ce_min)
	
	plot_circles(circles1,output)
	plot_circles(circles2,output)

	

	# Isola a borracha na foto
	# poderia ser feito uma mascara de tamanho fixo, mas fiz essa baseada no tamanho
	# do circulo detectado pois estou fazendo testes em imagens de tamanhos diferentes
	total = 0

	if (circles1 is not None) and (circles2 is not None):

		borracha_ferro = circles1[0,0]
		externo = circles2[0,0]
		#print(externo)
		#print(borracha_ferro)

		rachaduras = image.copy()
		dist = np.sqrt( ( d[:,:,1] - externo[0]) ** 2 + ( d[:,:,0] - externo[1]) ** 2 )
		zera = ( dist <= borracha_ferro[2] ) | ( dist >= externo[2] )

		rachaduras[zera] = 0

		cv2.imshow("Crop",  rachaduras )
		cv2.waitKey(1)
		
		# TO DO: Fazer canny line detection na parte da borracha.
		edged = cv2.Canny(rachaduras, 25, 30)

		cv2.imshow("Linhas",  edged )
		cv2.waitKey(1)
		
		brancos = (np.sum(edged)/255).astype(float)
		total = ( image.shape[0] * image.shape[1] ) - np.sum(zera)

		percentual = brancos*100.0/ (float(total)*0.75)
		print( str(percentual)+'%')
		window.update_percent(int(percentual))
	return output

def init_matrix():
	d = np.zeros( (fim_y - inicio_y,  fim_x - inicio_x  ,2) )
	for x in range( fim_y - inicio_y ):
		for y in range( fim_x - inicio_x ):
			d[x,y,:] = [x,y]

	return d


# Inicializacao da interface grafica
try:
	app = QtGui.QApplication(sys.argv)
	window = MyWindow()
	window.show()
except:
	print("Falha ao carregar interface grafica")

# Carrega parametros e arquivos auxiliares
try:
	#Parametros
	(inicio_x, inicio_y, fim_x, fim_y, ci_min,ci_max,ci_sens,ce_min,ce_max,ce_sens) = getParams()
	
	# matriz auxiliar
	d = init_matrix()

	# Template
	template = cv2.imread('img/template_roda.jpg')
	template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
	(tH, tW) = template.shape[:2]

	# Imagem inicial
	img_inicial = cv2.imread('img/roda-real.bmp')
	#img_inicial = img_inicial[inicio_y:fim_y,inicio_x:fim_x]
	#img_inicial = cv2.cvtColor(img_inicial, cv2.COLOR_BGR2GRAY)
	window.display_image(img_inicial,0)

except:
	print('Falha ao carregar template')


# Inicializacao da camera
try:
	imagem_exemplo = None
	print('Build against pylon library version:', pypylon.pylon_version.version)
	available_cameras = pypylon.factory.find_devices()
	print('Available cameras are', available_cameras)
	cam = pypylon.factory.create_device(available_cameras[-1])
	print('Camera info of camera object:', cam.device_info)
	cam.open()
except:
	print("Falha na comunicacao com a camera\nCarregando imagem de exemplo...")
	imagem_exemplo = cv2.imread('img/roda-real.bmp')
	imagem_exemplo = cv2.cvtColor(imagem_exemplo, cv2.COLOR_BGR2GRAY)


# Loop principal
if(imagem_exemplo is None):
	while True:
		for image in cam.grab_images(1):
			result = proc_image(image)
			try:
				cv2.imshow('frame',result)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
			except:
				cv2.destroyAllWindows()
				break
else:

	result = proc_image(imagem_exemplo)
	try:
		cv2.imshow('frame',result)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	except:
		cv2.destroyAllWindows()


sys.exit(app.exec_())
window.display_image(img_inicial,0)
