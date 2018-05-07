import cv2

image = cv2.imread('/img/img3.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

output = image.copy()


circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 1.4,140, maxRadius = 100)

if circles is not None:
	print(circles[0])

	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
 	
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
 
	cv2.imshow("output",  output )
	if args['save'] != None:
		cv2.imwrite(args['save'], np.hstack([image, output]) )
	cv2.waitKey(0)

