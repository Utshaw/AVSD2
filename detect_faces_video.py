# USAGE
# python detect_faces_video.py --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel

# import the necessary packages
#from imutils.video import VideoStream
import numpy as np
import os
import argparse
import imutils
import time
import cv2


def detectFace(videoName=os.path.join("input_videos", "sample4.mp4")):
	vd = videoName
	print('Video name: ' + str(vd))

	current_path = os.getcwd()
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--prototxt", default='deploy.prototxt.txt',
		help="path to Caffe 'deploy' prototxt file")
	ap.add_argument("-m", "--model", default='res10_300x300_ssd_iter_140000.caffemodel',
		help="path to Caffe pre-trained model")
	ap.add_argument("-c", "--confidence", type=float, default=0.5,
		help="minimum probability to filter weak detections")

	args = vars(ap.parse_args())

	# load our serialized model from disk
	print("[INFO] loading model...")

	print('-'*10)
	print(type(args["prototxt"]))
	print('-'*10)
	net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

	# initialize the video stream and allow the cammera sensor to warmup
	print("[INFO] starting video stream...")
	#vs = VideoStream(src=0).start()
	vs = cv2.VideoCapture(vd)
	time.sleep(1.0)

	f_no = 0
	# loop over the frames from the video stream
	while True:
			# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 400 pixels
		ret, frame = vs.read()
		f_no += 1
		frame = imutils.resize(frame, width=400)
	
		# grab the frame dimensions and convert it to a blob
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
			(300, 300), (104.0, 177.0, 123.0))
	
		# pass the blob through the network and obtain the detections and
		# predictions
		net.setInput(blob)
		detections = net.forward()

		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with the
			# prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections by ensuring the `confidence` is
			# greater than the minimum confidence
			if confidence < args["confidence"]:
				continue

			# compute the (x, y)-coordinates of the bounding box for the
			# object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
	
			# draw the bounding box of the face along with the associated
			# probability
			#text = "{:.2f}%".format(confidence * 100)
			y = startY - 10 if startY - 10 > 10 else startY + 10
			cv2.rectangle(frame, (startX-2, startY-2), (endX+2, endY+2), (0, 0, 255), 2)
			crop_img=frame[startY:endY, startX:endX]
			
			if np.shape(frame) == ():
				continue
			else:
				try:
					cv2.imwrite(current_path + "/dataset/" +str(f_no)+".png",crop_img)
				except Exception as e:
					print('-'*20)
					print(e)
					print('-' * 20)
			#cv2.putText(frame, text, (startX, y),
			#	cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
		# show the output frame
		# cv2.imshow("Frame", frame)
		# key = cv2.waitKey(1) & 0xFF

		# # if the `q` key was pressed, break from the loop
		# if key == ord("q"):
			# break

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

if __name__ == "__main__":
	detectFace()