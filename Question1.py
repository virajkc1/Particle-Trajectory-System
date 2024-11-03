import numpy as np
import cv2  
import matplotlib.pyplot as plt
import csv

#49 frames are in the video, calculated from trial and error in the for loop
video = cv2.VideoCapture("RedBall.mp4")  # this will store the video in a variable
xcoord =[]  # x and y co-ordinates are stored here to plot the graph
ycoord = []

plt.set_cmap("Greys")  #the colourmap is set to grayscale
for i in range(49):  # this will loop through each frame in the video
    ret, frame = video.read()
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY,) # converts the rgb image into grayscale
    img_cropped = grayImage[0:-400,0:1800]  #image cropped to remove irrelevant areas
    blurred = cv2.GaussianBlur(img_cropped, (7, 7), 0)  #image is blurred so easier to process 
    _,thresh = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY) #Thresholding conducted so if any pixel colour is less than 80 it will be converted to black
    kernel = np.ones((7, 7), dtype = np.uint8) # kernal size is the size at which dilation and erosion occur
    erosion = cv2.erode(thresh, kernel) # dilation removes floating white pixels in the image
    kernel2 = np.ones((7, 7), dtype = np.uint8)
    dilation = cv2.dilate(erosion, kernel2) # erosion expands the image as adjacent white pixels would have been converted into black from erosion hence dilation reverses this process

    circles = cv2.HoughCircles(  # this code is used to track the object for each frame
        dilation, # this is the image that it works on
        cv2.HOUGH_GRADIENT, 1, 
        minDist = 100, #the minimum distance between adjacent circles is high because only one circle should be present
        param1 = 100, param2 = 8, 
        minRadius = 0, maxRadius=0, # this will find any circle present in the frame, circle size varied between frames 
    )

    fig, ax = plt.subplots()

    ax.imshow(erosion)
    
    
    for circ in circles[0]: 
        x, y, r = circ
        ax.add_artist(plt.Circle((x, y), r, fill = False, color = "red")) # a red outline is produced per image
        x, y = circles[0][:, 0], circles[0][:, 1]
        xcoord.append(x[0])
        ycoord.append(y[0])
    # its 1520 horizontal and 1080 vertical

video.release()

with open('test.csv','w', newline= '') as f:  # code will save the x and y co-ordinates into a csv file to be read for question 2
  thewriter = csv.writer(f)
  thewriter.writerow(xcoord)
  thewriter.writerow(ycoord)

 # look through the y coordinates by using print(ycoord) to see where the peak of the second point is, change the value of ycoord[14] to its the peak in the specific video
# note you are looking for the number which is smallest once the ball has touched the surface
# this number should be subtracted by 1800 which is the vertical length of the scale but becasue the graph is flipped the scale starts from 1800 and reaches 0


# Calculate Restitution Coefficient
dropHeight = 1800 - ycoord[0] #get the drop height from graph
actualDropHeight = 0.041  #(m)
scalingFactor = actualDropHeight/dropHeight # Finds the scaling factor
bounceHeight = 1800 - ycoord[14] # gets the peak of the second bounce
actualbounceHeight = bounceHeight * scalingFactor # this is the actual bounce height (m)
resCoeff = math.sqrt(actualbounceHeight/actualDropHeight)

print("The Restitution Coefficient is:" ,resCoeff)
