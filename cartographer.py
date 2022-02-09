#!/usr/bin/env python3
import os
import json

# Importing the OpenCV library
import cv2

def initialChecks(srcDir, destDir):

    if not os.path.exists(srcDir):
        
        raise Exception("Source directory does not exist. Please check config.json file and try again.")

    if not os.path.exists(destDir):
        
        raise Exception("Destination directory does not exist. Please check config.json file and try again.")


def getEdges(srcDir, fileName, destDir):
    # Reading the image using imread() function
    image = cv2.imread(srcDir + "/" + fileName)
    
    # # Extracting the height and width of an image
    # h, w = image.shape[:2]
    # # Displaying the height and width
    # print("Height = {},  Width = {}".format(h, w))

    # Display original image
    # cv2.imshow('Original', image)
    # cv2.waitKey(0)

    # Convert to graycsale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)

    # Display Gaussian Blur Image
    # cv2.imshow('Gaussian Blur', img_blur)
    # cv2.waitKey(0)
    
    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
    
    # Display Canny Edge Detection Image
    # cv2.imshow('Canny Edge Detection', edges)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # writing the image to a defined location
    # cv2.imwrite(destDir + "/" +  fileName, edges)
    inverseImage = cv2.bitwise_not(edges)
    cv2.imwrite(destDir + "/" +  fileName, inverseImage)

def main():

    config = None

    # Look for a configuration file
    if os.path.exists('./config.json'):
        f = open('./config.json', 'r')
        config = json.loads(f.read())
        f.close()

    print("\nStarting with Config - ", str(config))

    srcDir = config["srcDir"]
    destDir = config["destDir"]

    initialChecks(srcDir, destDir)

    fileList = os.listdir(srcDir)

    if fileList:
        
        for fileName in fileList:
    
            getEdges(srcDir, fileName, destDir)
    else:

        print("No files found in source directory. Please check config.json file and try again.")

if __name__ == "__main__":
    main()