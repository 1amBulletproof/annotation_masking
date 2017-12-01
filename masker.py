#!/usr/local/bin/python2
#@Author Brandon Tarney
#@Since  11/30/2017

#Masker abstract super class
import numpy as np
import cv2

class Masker():

    mask_color = (0,0,0)

    def __init__(self, name):
        self.name = name
        self.performance = 0

    def mask_img_annotations(self, img):
        raise NotImplementedError("Abstract method called")

    def get_performance(self):
        color_min = np.array([0,0,0], np.uint8)
        color_max = np.array([0,0,0], np.uint8)
        result =  cv2.inRange(mask, color_min, color_max)
        return cv2.countNonZero(result)

    def get_mask_size(self, mask):
        color_min = np.array([0,0,0], np.uint8)
        color_max = np.array([0,0,0], np.uint8)
        result =  cv2.inRange(mask, color_min, color_max)
        return cv2.countNonZero(result)
