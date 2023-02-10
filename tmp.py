import os
import sys
import cv2



x = '/home/fssv2/fssv2_dataset/Crowd/1. VSCrowd/VSCrowd_Aug1/train/train_497/000085.jpg'
img = cv2.imread(x)
cv2.imshow('img', img) 
cv2.waitKey(0)