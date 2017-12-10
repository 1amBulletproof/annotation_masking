#!/usr/local/bin/python2
#@Author Brandon Tarney
#@Since  12/1/2017

#Color  masking: color masking for detection and masking annotations in images

from masker import Masker
import cv2
import numpy as np
import time

class ColorMasker(Masker):

    color_range = {
            'black': ((0,0,0),(0,0,20)),
            'white': ((0,0,200), (0,0,255)),
            'red' : ((175,50,50), (5,255,255)),
            'green' : ((55,50,50), (65,255,255)),
            'blue' : ((115,50,50), (125,255,255)) }


    def __init__(self, name, color):
        self.name = name
        self.color = color


    def mask_img_annotations(self, img):
        start_time = time.time()
        img_copy  = img.copy()
        color_mask = self.get_color_mask(img_copy)
        masked_img = self.apply_mask_to_img(color_mask, img_copy)
        end_time = time.time()
        Masker.performance = (end_time - start_time)
        return masked_img


    def get_color_mask(self, img):
        hsv_img  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        color_range = ColorMasker.color_range[self.color]
        mask =  cv2.inRange(hsv_img, color_range[0], color_range[1])
        Masker.mask = cv2.bitwise_not(mask)
        return mask


    def apply_mask_to_img(self, mask, img):
        inverted_mask = cv2.bitwise_not(mask)#black out the text
        masked_img = cv2.bitwise_and(img, img, mask=inverted_mask)
        return masked_img

