import pypylon
import imutils
import threading
import time
import sys
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import interface


from PyQt4 import QtGui, uic, QtCore
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *

# Como gerar o .py de um .ui
#pyuic4 CBM-RodaGuia/mainwindow.ui > interface.py

class MyWindow(QtGui.QMainWindow, interface.Ui_MainWindow):

	def __init__(self):
		#Esseinicializa a classe mae
		super(MyWindow, self).__init__()
		
		self.setupUi(self)

		#self.show()	
		self.timer = QtCore.QTimer()
		#self.timer.setInterval(3000)
		self.timer.timeout.connect(shot)
		self.timer.start(1000)
		
		self.mqtt_ok = True

		self.scene_init = QtGui.QGraphicsScene(self.foto_inicial) 
		self.scene_atual = QtGui.QGraphicsScene(self.foto_atual) 
		self.scene_crop = QtGui.QGraphicsScene(self.crop_borr)
		self.scene_rach = QtGui.QGraphicsScene(self.rachaduras) 
			

	def display_image(self,image, container):
		#return 0
		
		image = imutils.resize(image, width = int(image.shape[1] * 0.8))
		height, width = image.shape	

		# O problema estava nessa caralha de linha
		img = QtGui.QImage(image.tobytes(), width, height,(width),QtGui.QImage.Format_Indexed8)
		pixmap = QtGui.QPixmap.fromImage(img)
		img = QtGui.QImage()

		#img.clear()
		del img
		if container == 0:
			self.scene_init.clear()
			self.scene_init.addPixmap(pixmap)
			self.foto_inicial.setScene(self.scene_init)
			self.foto_inicial.show()
			self.scene_init.update()

		elif container == 1:
			self.scene_atual.clear()
			self.scene_atual.addPixmap(pixmap)
			self.foto_atual.setScene(self.scene_atual)
			self.foto_atual.show()
			self.scene_atual.update()

		elif container == 2:
			self.scene_crop.clear()
			self.scene_crop.addPixmap(pixmap)
			self.crop_borr.setScene(self.scene_crop)
			self.crop_borr.show()
			self.scene_crop.update()

		elif container == 3:
			self.scene_rach.clear()
			self.scene_rach.addPixmap(pixmap)
			self.rachaduras.setScene(self.scene_rach)
			self.rachaduras.show()
			self.scene_rach.update()
		
		pixmap =  QtGui.QPixmap()
		#pixmap.clear()
		del pixmap
		return 
		
	def update_percent(self,percentual):
		self.progressBar.setProperty("value", percentual)
		return
	
	def recurring_timer(self):
		shot()

	def mqtt_fail(self):
		self.mqtt_ok = False
		self.label_3.setText("MQTT Desconectado")


def shot():
	global cam, imagem_exemplo
	if(imagem_exemplo is None):
		for image in cam.grab_images(1):
			proc_image(image)
			break
	else:
		proc_image(imagem_exemplo)
		return

def mqtt_publish(percentual):
	global window
	if window.mqtt_ok:
		mqttc.publish('esp8266-out/id_nods/TQ7/Camera-CBM/Roda-Guia/pdr', \
						payload='{ \"data\":'+str(time.time() - 10800)+', \"valor\":'+ str(percentual) +'}', \
						qos=0, \
						retain=False
			)



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

#@profile
def log_transform(img,param):
	img = img.astype(np.float) # Cast to float
	c = (img.max()) / (img.max()**(param))
	img = (c*img**(param)).astype(np.uint8)
	#for i in range(0,img.shape[0]-1):
	#	for j in range(0,img.shape[1]-1):
	#		img[i,j] = np.int(c*img[i,j]**(param))

	# Cast back to uint8 for display
	#img = img.astype(np.uint8)
	del c
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
	
	window.display_image(image,1)
	image = log_transform(image,0.5)
	#output = image.copy()
	
	# define o limiar de deteccao da roda
	print(maxVal)
	if ( maxVal < 51553404*2 ) | (a is None):
		print("Nao eh roda")
		#return output
		return
	else:
		print("Roda")

	image_c = cv2.GaussianBlur(image,(3,3),0)

	circles1 = cv2.HoughCircles(image_c, cv2.HOUGH_GRADIENT, ci_sens , 700, maxRadius = ci_max, minRadius = ci_min)
	circles2 = cv2.HoughCircles(image_c, cv2.HOUGH_GRADIENT, ce_sens , 700, maxRadius = ce_max, minRadius = ce_min)
	#image_c.clear()
	del image_c

	#plot_circles(circles1,output)
	#plot_circles(circles2,output)
	#output.clear()
	#del output

	total = 0
	if (circles1 is not None) and (circles2 is not None):

		borracha_ferro = circles1[0,0]
		externo = circles2[0,0]
		rachaduras = image.copy()
		dist = np.sqrt( ( d[:,:,1] - externo[0]) ** 2 + ( d[:,:,0] - externo[1]) ** 2 )
		zera = ( dist <= borracha_ferro[2] ) | ( dist >= externo[2] )
		rachaduras[zera] = 0
		window.display_image(rachaduras,2)


		edged = cv2.Canny(rachaduras, 25, 30)
		window.display_image(edged,3)
		
		brancos = (np.sum(edged)/255).astype(float)
		
		#edged.clear()
		del edged
		del rachaduras

		total = ( image.shape[0] * image.shape[1] ) - np.sum(zera)
		percentual = brancos*100.0/ (float(total)*0.75)
		print( str(percentual)+'%')
		
		del zera
		del dist
		del image
		mqtt_publish(int(percentual))
		window.update_percent(int(percentual))
	
	return
	#return output

def init_matrix():
	d = np.zeros( (fim_y - inicio_y,  fim_x - inicio_x  ,2) )
	for x in range( fim_y - inicio_y ):
		for y in range( fim_x - inicio_x ):
			d[x,y,:] = [x,y]

	return d


if __name__ == "__main__":
	
	# Inicializacao da interface grafica
	try:
		app = QtGui.QApplication(sys.argv)
		window = MyWindow()
		window.show()
		print("Interface grafica carregada com sucesso")
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
		img_inicial = img_inicial[inicio_y:fim_y,inicio_x:fim_x]
		img_inicial = cv2.cvtColor(img_inicial, cv2.COLOR_BGR2GRAY)

		window.display_image(img_inicial,0)
		print("Parametros carregados com sucesso")
	except:
		print('Falha ao carregar parametros')

	
	try:
		mqttc = mqtt.Client()
		mqttc.connect("54.167.157.103", 1883, 60)
		mqttc.loop_start()
		print('Conexao MQTT bem sucedida')
	except:
		window.mqtt_fail()
		print('Falha ao estabelecer conexao MQTT com o server')


	# Inicializacao da camera
	try:
		imagem_exemplo = None
		print('Pylon version:', pypylon.pylon_version.version)
		available_cameras = pypylon.factory.find_devices()
		print('Cameras encontradas: ', available_cameras)
		cam = pypylon.factory.create_device(available_cameras[-1])
		print('Camera selecionada: ', cam.device_info)
		cam.open()
		print('Comunicacao com a camera realizada com sucesso')
	except: 	
		print("Falha na comunicacao com a camera\nCarregando imagem de exemplo...")
		imagem_exemplo = cv2.imread('img/roda-real.bmp')
		imagem_exemplo = cv2.cvtColor(imagem_exemplo, cv2.COLOR_BGR2GRAY)

	# Loop principal	
	sys.exit( app.exec_() )



# TO-DO: Fazer botao que chama rotina de reparametrizacao de raios e sensibilidades da deteccao
# TO-DO: Rotina de reconexao MQTT em caso de iniciar desconectado ou cair enquanto esta ligado
# TO-DO: Cropar a area da estrutura do elevador
