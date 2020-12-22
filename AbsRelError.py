#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np
from xml.etree import ElementTree
import cv2
from PIL import Image
import tensorflow as tf
import csv
import argparse
import os
import pandas as pd
import glob
import matplotlib.pyplot as plt
import pickle


#Raw images
save_path = '/home/ubuntu/Sayama/tmpdir/2020_08_04/video1top_png/image_02/data/'

#Mask images (These files may be used for the better evaluation in the future)
#mask_path= = '/home/ubuntu/Sayama/tmpdir/2020_08_04/video1top_png/image_03/data/'

#Depth maps (273486 = Before Fine Tuning, 279296 = After Fine Tuning)
#depth_map_dir='/home/ubuntu/Sayama/result_video1top_273486/'
depth_map_dir='/home/ubuntu/Sayama/result_video1top_279296/'

#Disparity map
ans_int_disp_map_dir="/home/ubuntu/Sayama/tmpdir/2020_08_04/video1middle_png/image_02/data"

#Abs Rel Error Calculation Settings
min_depth=5
max_depth=80

#Stereo Camera Parameters
bf=109.65
d_inf=2.67


#Making file list
#file_names = ["frame_000250"]
file_names = []
for file in os.listdir(save_path):
    if os.path.isfile(os.path.join(save_path, file)):
        file_name = file.rstrip('.png\n')
        file_names.append(file_name)


num_test=len(file_names)

rms     = np.zeros(num_test, np.float32)
log_rms = np.zeros(num_test, np.float32)
abs_rel = np.zeros(num_test, np.float32)
sq_rel  = np.zeros(num_test, np.float32)
d1_all  = np.zeros(num_test, np.float32)
a1      = np.zeros(num_test, np.float32)
a2      = np.zeros(num_test, np.float32)
a3      = np.zeros(num_test, np.float32)
scalors = np.zeros(num_test, np.float32)


def draw_images_ans_int(image_file):
    global ans_int_disp_map_dir    
    f_name=ans_int_disp_map_dir+"/"+image_file+".png"
    ans_int_disp_map=cv2.imread(f_name)
    ans_int_disp_map=cv2.cvtColor(ans_int_disp_map, cv2.COLOR_RGB2GRAY)
    return ans_int_disp_map


def abs_rel_error_single_image(i):
	pred_depth=np.load(depth_map_dir+file_names[i] +'.npy')
	pred_depth = cv2.resize(pred_depth, (416,128))

	ans_int_disp_map=draw_images_ans_int(file_names[i])

	gt_depth=bf/(ans_int_disp_map-d_inf)

	mask = np.logical_and(gt_depth>min_depth,gt_depth <max_depth)

	scalor = np.median(gt_depth[mask])/np.median(pred_depth[mask])
	scalors[i]=scalor

	pred_depth[mask] *= scalor


	pred_depth[pred_depth < min_depth] = min_depth
	pred_depth[pred_depth > max_depth] = max_depth

	abs_rel[i], sq_rel[i], rms[i], log_rms[i], a1[i], a2[i], a3[i] = compute_errors(gt_depth[mask], pred_depth[mask])
	
	print(str(i)+"/"+str(num_test))


def compute_errors(gt, pred):
    thresh = np.maximum((gt / pred), (pred / gt))
    a1 = (thresh < 1.25   ).mean()
    a2 = (thresh < 1.25 ** 2).mean()
    a3 = (thresh < 1.25 ** 3).mean()

    rmse = (gt - pred) ** 2
    rmse = np.sqrt(rmse.mean())

    rmse_log = (np.log(gt) - np.log(pred)) ** 2
    rmse_log = np.sqrt(rmse_log.mean())

    abs_rel = np.mean(np.abs(gt - pred) / gt)
    
    sq_rel = np.mean(((gt - pred)**2) / gt)

    return abs_rel, sq_rel, rmse, rmse_log, a1, a2, a3


for i in range(0,num_test):
	abs_rel_error_single_image(i)


print("{:>10}, {:>10}, {:>10}, {:>10}, {:>10}, {:>10}, {:>10}, {:>10}, {:>10} ".format('abs_rel', 'sq_rel', 'rms', 'log_rms', 'd1_all', 'a1', 'a2', 'a3', 'scalor'))
print("{:10.4f}, {:10.4f}, {:10.4f}, {:10.4f}, {:10.4f}, {:10.4f}, {:10.4f}, {:10.4f} ,{:10.4f} ".format(abs_rel.mean(), sq_rel.mean(), rms.mean(), log_rms.mean(), d1_all.mean(), a1.mean(), a2.mean(), a3.mean(),scalors.mean()))


