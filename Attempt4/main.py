import cv2
import numpy as np

img = cv2.imread('fist center.jpg', cv2.IMREAD_GRAYSCALE)                                      #replace "fist cener" with whatever file you please         
_, threshold = cv2.threshold(img, 158, 255, cv2.THRESH_BINARY)                                 #uses threshold to bring colors above/below 158 to white/black respectively
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)              #extracts contours for each of the binary shapes given to us by thresholding

output = [ ]                                                                                   #prepare array to hold each shape the contour function will spit out
skip = False                                                                                   #used later to keep null images from being locationally classified

for cnt in contours:                                                                           #CONTOUR CREATOR
    approx = cv2.approxPolyDP(cnt, 0.00001*cv2.arcLength(cnt, True), True)
    cv2.drawContours(img, [approx], 0, (0), 5)
    output.append(len(approx))                                                                 #for every shape found, append its contour quantity to the array called "output"

# in solid shapes like FIST and SPLAY, only one shape is recognized by contours, 
# which means the output array will only contain one value. In PALMS, the smidge of light
# between the fingers creates another shape, which means the output array for PALMS will
# have more than one value. This phenomena is what I'm referencing in the if-condition
# below.

if len(output) < 2:                                                                            #TYPE CLASSIFIER
    vert = output[0]                                                                           #variable "vert" = no. of vertices in the first/only shape in the output list
    if (100 <= vert <= 450):                                                                   #fists = commonly between 100 and 450 vertices
         print("fist")
    elif (451 <= vert <= 850):                                                                 #splay = commonly between 451 and 850 vertices
         print("splay")              
    elif vert < 100:                                                                           #null always has at least 4 vertices because of the corners of the photos
         print("null")
         skip = True                                                                           #"skip" boolean comes into play, here
else:
     print ("palm")                                                                            #if there's more than one entry in the output array, must be a palm


# as seen below, since some palms/splays in the bottom half of the screen would extend past
# the true middle of the screen, becoming present in more than one quadrant,
# I had to make the divider between the top and bottom 
# be a hard-coded number that's closer to the top of the screen than it is from the 
# bottom. Thus, 200 pixels was chosen, as it falls right above the finegrtips of 
# bottom-positioned palms/splays. 

(h, w) = threshold.shape[:2]
belt = 200                                                                                     #value for pixel height for the "belt" dividing top and bottom halves of screen

topLeft = threshold[0:belt, 0:360]                                                             #the bounds for each quadrant of the frame
topRight = threshold[0:belt, 360:w]
bottomLeft = threshold[belt:h, 0:360]
bottomRight = threshold[belt:h, 360:w]
                                                                                                           
tl = np.sum(topLeft == 0)                                                                      # COUNT THE NUMBER OF BLACK PIXELS
tr = np.sum(topRight == 0)                                                                     #whatever quadrant had black pixels contained the hand.
bl = np.sum(bottomLeft == 0)
br = np.sum(bottomRight == 0)
                                                                                               #DETERMINE LOCATION 
if (not skip):                                                                                 #skip used to eliminate "null" pics from continuing to this part. 

     if (tl and br):                                                                           #if in two diagonal blocks, it had to be in the center.
          print ("center")
     elif (bl and tl):                                                                         #whatever quadrant had black pixels contained the hand.
          print("top left")
     elif (bl and not tl):
          print("bottom left")
     elif (br and tr):
          print("top right")
     elif (br and not tr):
          print("bottom right")

cv2.imshow('Threshold', threshold)
# cv2.imshow('Contours', img)                                                                  #feel free to run this line if you want to see the OG image + contour outline
cv2.waitKey(0)
cv2.destroyAllWindows()
