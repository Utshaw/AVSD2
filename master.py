#!/usr/bin/env python3
import shutil
import os
import detect_faces_video
import unsupervised_clustering
import videomaker
import encode_faces
import pandas as pd
import extract_Audio as ea
import cv2
import logging
logging.basicConfig(filename='avsd-info.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='avsd-error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')



DATASET_DIR = 'dataset'
FILTERED_FACES_DIR = 'filtered_faces'
INPUT_VIDEO_DIR = 'input_videos'

def getVideoList():
    """
    Gives list of images in IMAGE_LOCATION
    Args:
    
    Returns:
        [list]: list of image names
    """
    try:
        return os.listdir(INPUT_VIDEO_DIR)
    except FileNotFoundError:
        print('Given directory {} doesn\'t exist.'.format(IMAGE_LOCATION))
        sys.exit()


def cleanDir(dirName):
    shutil.rmtree("./" + dirName)
    os.makedirs(dirName)

def cleanDirs():
    cleanDir(DATASET_DIR)
    cleanDir(FILTERED_FACES_DIR)


def getFPS(inputVideoName):
    video = cv2.VideoCapture(os.path.join(INPUT_VIDEO_DIR, inputVideoName));
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver)  < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        fps = video.get(cv2.CAP_PROP_FPS)   
    return fps


def main():
    
    videoList = getVideoList()
    for video in videoList:
        try:

            ea.getAudio(os.path.join(INPUT_VIDEO_DIR, video))

            videoBaseName = os.path.splitext(video)[0]
            print(videoBaseName)
            
            print(os.path.join(INPUT_VIDEO_DIR, video))
            cleanDirs()
            try:
                detect_faces_video.detectFace(os.path.join(INPUT_VIDEO_DIR, video))
            except AttributeError as e:
                print(e)

            encode_faces.main()
            unsupervised_clustering.main()
            videomaker.createVideo(videoBaseName, fps_=getFPS(video))
        except:
            logging.error('Error processing (%s)' % (video))
            continue
        

if __name__ == "__main__":
    
    start = pd.Timestamp.now()
    main()
    print("TIME TAKEN: " + str(pd.Timestamp.now()-start))