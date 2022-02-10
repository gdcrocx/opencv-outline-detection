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

def writeSVG(contours, height, width, destDir, fileName):

    fileName = os.path.splitext(fileName)[0]

    # c = max(contours, key=cv2.contourArea) # max contour

    # f = open(destDir + "/" + fileName + '.svg' , 'w+')
    # f.write('<svg width="'+str(width)+'" height="'+str(height)+'" xmlns="http://www.w3.org/2000/svg">')
    # f.write('<path d="M')

    # for i in range(len(c)):
    #     # print(c[i][0])
    #     x, y = c[i][0]
    #     # print(x)
    #     f.write(str(x)+  ' ' + str(y)+' ')

    # f.write('"/>')
    # f.write('</svg>')
    # f.close()

    with open(destDir + "/" + fileName + ".svg", "w+") as f:
        f.write(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')

        for c in contours:
            f.write('<path d="M')
            for i in range(len(c)):
                x, y = c[i][0]
                f.write(f"{x} {y} ")
            f.write('" style="stroke:black"/>')
        f.write("</svg>")

def getEdges(image, fileName, destDir):
    
    # # Extracting the height and width of an image
    imgHeight, imgWidth = image.shape[:2]
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

    # Inverse B&W Image
    # inverseImage = cv2.bitwise_not(edges)

    # Display Inverse Image 
    # cv2.imshow("Inverse Image", inverseImage)
    # cv2.waitKey(0)

    # contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_TC89_L1)

    # writing the image to a defined location
    # cv2.imwrite(destDir + "/" +  fileName, inverseImage)

    writeSVG(contours, imgHeight, imgWidth, destDir, fileName)

    # cv2.destroyAllWindows()

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
    
            # Reading the image using imread() function
            image = cv2.imread(srcDir + "/" + fileName)            

            getEdges(image, fileName, destDir)
    else:

        print("\nNo files found in source directory. Please check config.json file and try again.")

if __name__ == "__main__":
    main()
    print()