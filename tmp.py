import os
import sys
import cv2
from tqdm import tqdm
import numpy as np
from glob import glob
import random
import shutil

# txt_path = "/home/fssv2/fssv2_dataset/Crowd/1. VSCrowd/VSCrowd_Aug1/val.txt"
# with open(txt_path, "r") as f:
#     jpg_list = f.read().splitlines()

# print(jpg_list[:6])

# for jpg_path in tqdm(jpg_list):
#     txt_path = jpg_path.replace(".jpg", ".txt")

#     with open(txt_path, "r") as f:
#         labels = f.read().splitlines()

#     for label in labels:
#         label = label.split(" ")
#         class_idx = label[0]
#         cx = float(label[1])
#         cy = float(label[2])
#         w = float(label[3])
#         h = float(label[4])

#         if not class_idx == "0":
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


# data_dir = '/home/fssv2/fssv2_dataset/Crowd/1. VSCrowd/VSCrowd_Aug2'
# with open(os.path.join(data_dir, 'train.txt'), 'r') as f:
#     img_list = f.read().splitlines()

# img_list = random.sample(img_list, 100)
# print(len(img_list))

# num = 0
# for img_path in img_list:
#     num += 1
#     new_img_path = os.path.join(data_dir, 'tmp', f'{num:03d}.jpg')

#     shutil.copyfile(img_path, new_img_path)


# detections = np.array([
#     [0, 0.95461, 19, 14, 38, 43],
#     [1, 0.94512, 38, 16, 57, 46],
#     [10, 0.90392, 57, 20, 77, 49],
#     [12, 0.4, 57, 20, 77, 49],
#     [20, 0.7, 57, 20, 77, 49],
#     [1, 0.96204, 92, 25, 111, 54],
#     [1, 0.93653, 112, 27, 131, 57],
#     [3, 0.93458, 132, 30, 152, 59],
#     [3, 0.6458, 132, 30, 152, 59],
#     [4, 0.93637, 153, 32, 174, 61],
#     [0, 0.4138, 174, 30, 190, 59]
#  ])

# str_idx_list = np.where((10<=detections[..., 0]) & (detections[..., 0]<=48))[0]

# if len(str_idx_list):
#     if len(str_idx_list) > 1:
#         arg_idx = np.argsort(-detections[str_idx_list][..., 1])
#         delete_idx = str_idx_list[arg_idx[1:]]
#         detections = np.delete(detections, delete_idx, axis=0)
#         str_idx = str_idx_list[arg_idx[0]]
#     else:
#         str_idx = str_idx_list[0]

#     if len(detections[str_idx+1:]) > 4:
#         delete_idx = np.argsort(-detections[str_idx+1:, 1])[4:] + (str_idx + 1)
#         detections = np.delete(detections, delete_idx, axis=0)

# print(detections)


# txt_path = '/home/fssv2/myungsang/datasets/lpr/test_2.txt'
# with open(txt_path, 'r') as f:
#     jpg_list = f.read().splitlines()


# tmp = 0
# for jpg_path in tqdm(jpg_list):
#     txt_path = jpg_path.replace('.jpg', '.txt')

#     with open(txt_path, 'r') as f:
#         labels = f.read().splitlines()

#     label = labels[0].split(' ')
#     class_idx, cx, cy, w, h = label
#     if class_idx != '0':
#         tmp += 1

#         label = f'0 {cx} {cy} {w} {h}\n'

#         with open(txt_path, 'w') as f:
#             f.write(label)

# print(tmp)


print(np.mod(33, 32))