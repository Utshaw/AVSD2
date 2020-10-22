#!/usr/bin/env python3
# Video generation: https://stackoverflow.com/questions/44947505/how-to-make-a-movie-out-of-images-in-python
# Check requirements.txt
# to use cv2 module: pip install opencv-python
# to use moviepy: pip install moviepy
# pip install Pillow==2.2.2
# pip3 install --upgrade pillow

from PIL import Image
import os
import sys
# import cv2
import moviepy.video.io.ImageSequenceClip
from shutil import copyfile
import extract_Audio as ea
import logging
logging.basicConfig(filename='avsd-info.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(filename='avsd-error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

IMAGE_LOCATION = "filtered_faces"
VIDEO_OUTPUT_DIR = "videos"
AUDIO_OUTPUT_DIR = "audios"
MY_MAX_INT = 99999999
MY_MIN_INT = -1
FPS = 1


def getMaxImageSize(imageList):
    """
    Get the maximum image size from a list of images

    Args:
        imageList (list): list of images 
    Returns:
        return the highest width, height of the images
    """
    maxWidth = MY_MIN_INT
    maxHeight = MY_MIN_INT
    for image in imageList:
        im = Image.open(os.path.join(IMAGE_LOCATION, image)) 
        width, height = im.size
        if width > maxWidth:
            maxWidth = width
        if height > maxHeight:
            maxHeight = height
    return maxWidth, maxHeight

def getMinImageSize(imageList):
    """
    Get the minimum image size from a list of images

    Args:
        imageList (list): list of images 
    Returns:
        return the lowest width, height of the images
    """
    minWidth = MY_MAX_INT
    minHeight = MY_MAX_INT
    for image in imageList:
        im = Image.open(os.path.join(IMAGE_LOCATION, image))
        width, height = im.size
        if width < minWidth:
            minWidth = width
        if height < minHeight:
            minHeight = height
    return minWidth, minHeight

    



def resizeImage(targetWidth, targetHeight, imageName):
    """
    Resizes given image in place to given width & height

    Args:
        targetWidth (int): The target width of the image 
        targetHeight (int): Target height of the image
        imageName (string): image name, the image must be in IMAGE_LOCATION directory
    """    
    try:

        im = Image.open(os.path.join(IMAGE_LOCATION, imageName))
    except FileNotFoundError:
        print(imageName + ' file is not found inside ' + os.getcwd() +  IMAGE_LOCATION + " directory")
    else:
        f, e = os.path.splitext(imageName)
        imResize = im.resize((targetWidth,targetHeight), Image.ANTIALIAS)
        imResize.save(os.path.join(IMAGE_LOCATION, imageName), 'PNG', quality=90)


def resizeAllImages(targetWidth, targetHeight, imageList):
    """
    Resize all images in IMAGE_LOCATION

    Args:
        targetWidth (int): The target width of the image 
        targetHeight (int): Target height of the image
        imageList (list): list of images
    """
    for image in imageList:
        resizeImage(targetWidth, targetHeight, image)


def generateImage(imageDirectory, firstImage, numberOfImages):
    """
    Genenrates images from given sample image

    Args:
        imageDirectory (string): The parent directory inside which all images wll be generated 
        firstImage (string): The sample image which will be replicated (should be inside the imageDirectory)
        numberOfImages (int): Total number of images that will be generated (including the given one)
    """    

    fileBaseName = 2
    for i in range(numberOfImages-1):
        copyfile(imageDirectory + "/" + firstImage, imageDirectory + "/" + str(fileBaseName) + ".png")
        fileBaseName+=1

# generateImage("images", "1.png", 100)

def getImageList(chunkSize):

    """
    Generator gives list of ( list of image names of chunk size )
    Args:
        chunkSize (int) : number of images in a single chunk
    Yields:
        [list]: list of images name
    """    
    imageList = os.listdir(IMAGE_LOCATION)
    imageList = sorted(imageList, key=lambda x : int(os.path.splitext(x)[0]))
    
    firstImageNo = int(os.path.splitext(imageList[0])[0])
    

    chunkList = [imageList[0]]
    totalImageInCurrentPass = 1
    expectedImageNo = firstImageNo + 1

    for image in imageList[1:]:
        currentImageInt = int(os.path.splitext(image)[0])
        if (currentImageInt == expectedImageNo) and (totalImageInCurrentPass != chunkSize) :
            chunkList.append(image)
            totalImageInCurrentPass += 1
            expectedImageNo+=1
        else:
            yield chunkList
            chunkList = [image]
            totalImageInCurrentPass = 1
            expectedImageNo = currentImageInt + 1
        
    yield chunkList




def createVideo(inputVideoName="sample1", fps_=25):
    global FPS
    FPS=fps_
    chunkedImageList = getImageList(350) # change 9 to 350
    masterImageList = []
    videoDict = {}

    for imageList in chunkedImageList:
        if len(imageList) < 100:
            print('Ignoring this imageList because of small size (less than 100) | Size: ' + str(len(imageList)))
        else:
            masterImageList.append(imageList)

    for imageList in masterImageList:
        targetWidth, targetHeight = getMinImageSize(imageList)
        # print(str(targetWidth) + ", " + str(targetWidth) + " target size for " + str(imageList) )
        resizeAllImages(targetWidth, targetHeight, imageList)
        videoDict[os.path.splitext(imageList[0])[0] + '_' + os.path.splitext(imageList[-1])[0]]     = imageList

    video_name = ""
    image_files = []
    image_folder = IMAGE_LOCATION


    passNum = 1
    for name, value in videoDict.items(): # 1_193 -> [1.png, ... , 193.png]
        videoFileBaseName =  inputVideoName + "_" + str(passNum) + "_" + name + ".mp4"
        audioFileBaseName =  inputVideoName + "_" + str(passNum) + "_" + name + ".mp3"

        video_name = os.path.join(VIDEO_OUTPUT_DIR, videoFileBaseName) 
        image_files = [IMAGE_LOCATION + os.path.sep + "" + single_image for single_image in value]    
        # print("Generating " + video_name)
        # print('----'*50)
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=FPS)
        clip.write_videofile(video_name)
        frame_start, frame_end = int(name.split('_')[0]), int(name.split('_')[1])
        timestamp_ =  frame_start / FPS
        duration = (frame_end / FPS) - timestamp_
        ea.main(str(int(timestamp_)), str(int(duration)), os.path.join(AUDIO_OUTPUT_DIR, audioFileBaseName))
        passNum += 1
        logging.info('Video-> (%s)  || Audio-> (%s)' % (videoFileBaseName, audioFileBaseName))




if __name__ == "__main__":
    createVideo()