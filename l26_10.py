#!.venv/bin python
from math import ceil, floor
import numpy as np
import matplotlib.pyplot as plt
import cv2
import random

i1 = cv2.imread('Data/kostka.jpg')
#plt.figure()
#plt.title("Kostka")
#plt.imshow(i1)

#print(i1.shape)

i1gray = cv2.cvtColor(i1, cv2.COLOR_RGB2GRAY)
#plt.figure()
#plt.title("GrayScale")
#plt.imshow(i1gray, cmap="gray")

k = 5

#laplacian = cv2.Laplacian(i1gray, cv2.CV_64F)
#sobelx = cv2.Sobel(i1gray,cv2.CV_64F, 1,0,ksize=k)
#sobely = cv2.Sobel(i1gray,cv2.CV_64F, 0,1,ksize=k)

#plt.figure()
#plt.title('Laplacian')
#plt.imshow(laplacian,cmap='gray')

#plt.figure()
#plt.title('Sobelx')
#plt.imshow(sobelx,cmap='gray')

#plt.figure()
#plt.title('Sobely')
#plt.imshow(sobely,cmap='gray')

i2 = cv2.imread('Data/20211026_105058.jpg')
i2_gray = cv2.cvtColor(i2, cv2.COLOR_BGR2GRAY)
plt.figure()
plt.title("Scena")
plt.imshow(i2_gray,cmap="gray")

#plt.figure()
#plt.title("gray diff")
#plt.imshow(i2gdiff,cmap="gray")

ibg = cv2.imread('Data/20211026_105101.jpg')
ibg_gray = cv2.cvtColor(ibg, cv2.COLOR_BGR2GRAY)
plt.figure()
plt.title("BG")
plt.imshow(ibg_gray,cmap="gray")

diff = cv2.subtract(ibg_gray,i2_gray)
plt.figure()
plt.title("Diff")
plt.imshow(diff,cmap="gray")

_, tdiff = cv2.threshold(diff,120,255,cv2.THRESH_BINARY)
plt.figure()
plt.title("Thresholded")
plt.imshow(tdiff, cmap="gray")

kernel = np.ones((5,5),np.uint8)
tediff = cv2.erode(tdiff,kernel, iterations=2)

plt.figure()
plt.title("Eroded")
plt.imshow(tediff,cmap="gray")

teddiff = cv2.dilate(tediff,kernel,iterations=8)

plt.figure()
plt.title("Dilatated")
plt.imshow(teddiff,cmap="gray")

contours, _ = cv2.findContours(teddiff, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

thcontours = []
for c in contours:
    if cv2.contourArea(c)>600:
        thcontours.append(c)

print(len(thcontours))

cv2.drawContours(i2,thcontours,-1, (0,255,0),3)
plt.figure()
plt.title("Contour")
plt.imshow(i2)

circles = cv2.HoughCircles(i1gray,cv2.HOUGH_GRADIENT,1,5,param1=50,param2=20,minRadius=20,maxRadius=50)
circles = np.uint16(np.around(circles))
for c in circles[0,:]:
    cv2.circle(i1,(c[0],c[1]),c[2],(0,255,0),8)

print(len(circles[0,:]))
print(circles)
plt.figure()
plt.imshow(i1)



#ksize = 5
#kernel = np.ones((ksize,ksize))
#isx = 150
#isy = 150
#image = np.random.rand(isx,isy)*200

image = ibg_gray
isx,isy = image.shape

ksize = 3
kernel = np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]])

out = np.zeros((isx-ksize+1,isy-ksize+1))
for x in range(isx-ksize):
    for y in range(isy-ksize):
        out[x,y] = (kernel*image[x:x+ksize,y:y+ksize]).sum()
plt.figure()
plt.imshow(out,cmap="gray")

plt.show()