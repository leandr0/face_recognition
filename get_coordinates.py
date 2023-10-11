import numpy as np
import cv2

image = cv2.imread('CNH.jpeg')
y=195
x=165
h=250
w=220
foto = image[y:y+h, x:x+w]
cv2.imshow('Image', foto)


y=165
x=180
h=20
w=480
nome = image[y:y+h, x:x+w]
cv2.imshow('Image', nome)

cv2.waitKey(0)