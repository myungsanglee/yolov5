import os
import sys
import cv2
from tqdm import tqdm
import numpy as np

# txt_path = '/home/fssv2/fssv2_dataset/Crowd/1. VSCrowd/VSCrowd_Aug1/val.txt'
# with open(txt_path, 'r') as f:
#     jpg_list = f.read().splitlines()

# print(jpg_list[:6])

# for jpg_path in tqdm(jpg_list):
#     txt_path = jpg_path.replace('.jpg', '.txt')
    
#     with open(txt_path, 'r') as f:
#         labels = f.read().splitlines()
        
#     for label in labels:
#         label = label.split(' ')
#         class_idx = label[0]
#         cx = float(label[1])
#         cy = float(label[2])
#         w = float(label[3])
#         h = float(label[4])

#         if not class_idx == '0':
#             print(txt_path)
#             break
#         if cx == 0.0 or cx == 1.0 or cx < 0.0:
#             print(txt_path)
#             break
#         if cy == 0.0 or cy == 1.0 or cy < 0.0:
#             print(txt_path)
#             break
#         if w == 0.0 or w < 0.0:
#             print(txt_path)
#             break
#         if h == 0.0 or h < 0.0:
#             print(txt_path)
#             break



a = '/home/fssv2/fssv2_dataset/Crowd/3. FDST/test_data/10/051.jpg'
b = a.split(os.sep)
print(b[-2])