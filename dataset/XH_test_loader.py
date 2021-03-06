# -*- coding:utf-8 -*-
#psenet-PyTorch-dataloader-for-batch-test
import numpy as np
from PIL import Image
from torch.utils import data
import util
import cv2
import random
import torchvision.transforms as transforms
import torch

'''
data_root_dirX = '数据文件夹所在根目录'
test_data_dirX = data_root_dirX + 'img所在文件夹名'
test_gt_dirX = data_root_dirX + 'label所在文件夹名' 如果没有真值可以不用
'''
#支持多个符合ICDAR2015标准的文件夹同时训练，无需整合到一个数据目录下

data_root_dir0 = './testdata/'
test_data_dir0 = data_root_dir0 + ''


random.seed(123456)

def get_img(img_path):
    try:
        img = cv2.imread(img_path)
        img = img[:, :, [2, 1, 0]]
    except Exception as e:
        print img_path
        raise
    return img

def scale(img, long_size=2240):
    h, w = img.shape[0:2]
    scale = long_size * 1.0 / max(h, w)
    img = cv2.resize(img, dsize=None, fx=scale, fy=scale)
    return img

class XHTestLoader(data.Dataset):
    def __init__(self, part_id=0, part_num=1, long_size=2240):
        data_dirs = [data_root_dir0]
        
        self.img_paths = []
        
        for data_dir in data_dirs:
            img_names = util.io.ls(data_dir, '.jpg')
            img_names.extend(util.io.ls(data_dir, '.png'))

            img_paths = []
            for idx, img_name in enumerate(img_names):
                img_path = data_dir + img_name
                img_paths.append(img_path)
            
            self.img_paths.extend(img_paths)

        part_size = len(self.img_paths) / part_num
        l = part_id * part_size
        r = (part_id + 1) * part_size
        self.img_paths = self.img_paths[l:r]
        self.long_size = long_size

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, index):
        img_path = self.img_paths[index]

        img = get_img(img_path)

        #resize
        scaled_img = scale(img, self.long_size)
        scaled_img = Image.fromarray(scaled_img)

        #no resize
        #scaled_img = Image.fromarray(img)
        scaled_img = scaled_img.convert('RGB')
        scaled_img = transforms.ToTensor()(scaled_img)
        scaled_img = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])(scaled_img)
        #print(scaled_img.size())
        
        return img[:, :, [2, 1, 0]], scaled_img