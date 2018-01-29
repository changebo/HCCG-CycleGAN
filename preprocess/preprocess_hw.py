# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

import argparse
import sys
import numpy as np
import scipy.misc
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import json
import collections
import random
reload(sys)
sys.setdefaultencoding("utf-8")




#split_ratio = 0.3
#ratioA = 0.1
#ratioB = 0.1
#def draw_single_char(ch, font, canvas_size=256, x_offset=0, y_offset=0):
#    img = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
#    draw = ImageDraw.Draw(img)
#    draw.text((x_offset, y_offset), ch, (0, 0, 0), font=font)
#    return img


def draw_single_char(ch, font, canvas_size=128, x_offset=0, y_offset=0):
    img = Image.new("L", (canvas_size, canvas_size), 255)
    draw = ImageDraw.Draw(img)
    draw.text((x_offset, y_offset), ch, 0, font=font)
    return img




def resize_image(img):
    # pad to square
    pad_size = int(abs(img.shape[0]-img.shape[1]) / 2)
    if img.shape[0] < img.shape[1]:
        pad_dims = ((pad_size, pad_size), (0, 0))
    else:
        pad_dims = ((0, 0), (pad_size, pad_size))
    img = np.lib.pad(img, pad_dims, mode='constant', constant_values=255)
    # resize
    img = scipy.misc.imresize(img, (128, 128))
    assert img.shape == (128, 128)
    return img


def main(path, source_path, ratioA, ratioB):
    source_font = ImageFont.truetype(source_path, size=128)
    f = open(path, "rb")
    random.seed(20171201)
    charlist = []
    bitmaplist = []
    sourcelist = []
    filename = os.path.basename(path).split('.')[0]
    datafolder = os.path.join('DenseCycleGAN', 'datasets', filename + '-' + ratioA + '-' + ratioB)
    if not os.path.exists(datafolder):
        os.makedirs(datafolder)
    trainA_path = os.path.join(datafolder, 'trainA')
    trainB_path = os.path.join(datafolder, 'trainB')
    testA_path = os.path.join(datafolder, 'testA')
    testB_path = os.path.join(datafolder, 'testB')
    folders = [trainA_path,trainB_path, testA_path, testB_path]
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)
    while True:
        tmp = f.read(4)
        if len(tmp) is 0:
            break
        else:
            sample_size = np.fromstring(tmp, dtype=np.uint32).item()
            tag_code = np.fromstring(f.read(2), dtype=np.uint16).newbyteorder().item()
            width = np.fromstring(f.read(2), dtype=np.uint16).item()
            height = np.fromstring(f.read(2), dtype=np.uint16).item()
            bitmap = np.fromstring(f.read(width * height), dtype=np.uint8)
            bitmap = bitmap.reshape([height, width])
            bitmap = resize_image(bitmap)
            bitmaplist.append(bitmap)
            ch = bytearray.fromhex(str(hex(tag_code))[2:]).decode('gb2312')
            charlist.append(ch)
            source_img = draw_single_char(ch, font = source_font)
            sourcelist.append(source_img)
    arr = np.arange(len(charlist))
    np.random.shuffle(arr)
    ntrainA = np.floor(float(ratioA) * len(charlist))
    ntrainB = np.floor(float(ratioB) * len(charlist))
    for x in np.arange(len(arr)):
    	ch = charlist[arr[x]]
        bitmap = bitmaplist[arr[x]]
        source_img = sourcelist[arr[x]]
        if arr[x]<=ntrainA and arr[x]<=ntrainB:
            scipy.misc.imsave(os.path.join(trainA_path, str(ord(ch)) + '.png'), bitmap)
            scipy.misc.imsave(os.path.join(trainB_path, str(ord(ch)) + '.png'), source_img)
        elif arr[x]>ntrainA and arr[x]<=ntrainB:
            scipy.misc.imsave(os.path.join(testA_path, str(ord(ch)) + '.png'), bitmap)
            scipy.misc.imsave(os.path.join(trainB_path, str(ord(ch)) + '.png'), source_img)
        elif arr[x]<=ntrainA and arr[x]>ntrainB:
            scipy.misc.imsave(os.path.join(trainA_path, str(ord(ch)) + '.png'), bitmap)
            scipy.misc.imsave(os.path.join(testB_path, str(ord(ch)) + '.png'), source_img)
        else:
            scipy.misc.imsave(os.path.join(testA_path, str(ord(ch)) + '.png'), bitmap)
            scipy.misc.imsave(os.path.join(testB_path, str(ord(ch)) + '.png'), source_img)
    


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
