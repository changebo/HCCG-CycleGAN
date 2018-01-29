import numpy as np
import cv2
import os
import scipy.misc as misc
from PIL import Image
import cv2
import sys


np.set_printoptions(threshold=np.nan)

processed_foldername = 'processedWangxizhi'
if not os.path.exists(processed_foldername):
	os.makedirs(processed_foldername)

nfile = os.listdir('./wangxizhi_origin')

for file in nfile:
	img = cv2.imread(os.path.join('./wangxizhi_origin', file),0)
	img = cv2.medianBlur(img,7)
	cv2.fastNlMeansDenoisingMulti(img, 2, 5, None, 4, 7, 35)

	width = img.shape[0]
	height = img.shape[1]
	bound = 3

	img[img>80] = 255
	img[600:,500:] = 255
	img[0:bound,:] = 255
	img[:,0:bound] = 255
	img[-bound:,:] = 255
	img[:,-bound:] = 255


	crop = img[80:640,50:610].copy()
	misc.imsave(os.path.join('./processedWangxizhi', file), crop)
	
