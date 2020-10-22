# USAGE
# python unsupervised_clustering.py --encodings encodings.pickle

# import the necessary packages
from sklearn.cluster import DBSCAN
from imutils import build_montages
import os
import numpy as np
import argparse
import pickle
import cv2
import re

def main():
	current_path = os.getcwd()

	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-e", "--encodings", default='encodings.pickle',
		help="path to serialized db of facial encodings")
	ap.add_argument("-j", "--jobs", type=int, default=-1,
		help="# of parallel jobs to run (-1 will use all CPUs)")
	args = vars(ap.parse_args())

	# load the serialized face encodings + bounding box locations from
	# disk, then extract the set of encodings to so we can cluster on
	# them
	print("[INFO] loading encodings...")
	data = pickle.loads(open(args["encodings"], "rb").read())
	data = np.array(data)
	encodings = [d["encoding"] for d in data]

	# cluster the embeddings
	print("[INFO] clustering...")
	clt = DBSCAN(metric="euclidean", n_jobs=args["jobs"])
	clt.fit(encodings)

	# determine the total number of unique faces found in the dataset
	labelIDs = np.unique(clt.labels_)
	numUniqueFaces = len(np.where(labelIDs > -1)[0])
	print("[INFO] # unique faces: {}".format(numUniqueFaces))

	sp_id = 0
	max = 0
	f_no = 0
	# loop over the unique face integers
	for labelID in labelIDs:
		# find all indexes into the `data` array that belong to the
		# current label ID, then randomly sample a maximum of 25 indexes
		# from the set
		print("[INFO] faces for face ID: {}".format(labelID))
		idxs = np.where(clt.labels_ == labelID)[0]
		if len(idxs)>max:
			sp_id = labelID
			max = len(idxs)
			
	idxs = np.where(clt.labels_ == sp_id)[0]

	for i in idxs:
		# load the input image and extract the face ROI
		image = cv2.imread(data[i]["imagePath"])
		prev_path = str(data[i]["imagePath"])
		bool = re.search('dataset(.+?).png', prev_path)
		
		extract_num = ""
		if bool:
			extract_num = bool.group(1)
		
		n = extract_num[1:]
		#print(n)
		
		(top, right, bottom, left) = data[i]["loc"]
		face = image[top:bottom, left:right]
		cv2.imwrite(current_path + "/filtered_faces/" +n+".png",face)
		#f_no+=1

	print("The speaker is Face :{}" .format(sp_id))



if __name__ == "__main__":
	main()