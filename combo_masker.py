#!/usr/local/bin/python2
#@Author Brandon Tarney
#@Since  11/30/2017

#Combo masking: combine color masking and edge detection masks

from masker import Masker
import cv2
import time

class ComboMasker(Masker):
    def __init__(self, name):
        self.name = name


    def mask_img_annotations(self, img):
        start_time = time.time()
        masked_img = img.copy()
        color_mask = self.get_color_mask(masked_img)
        edge_mask = self.get_edge_mask(masked_img)
        final_mask = cv2.bitwise_and(color_mask,
                edge_mask)
        final_img = self.apply_mask_to_img(final_mask, masked_img)
        end_time = time.time()
        Masker.performance = (end_time - start_time)
        return final_masked_img


    def get_color_mask(self, img):
        masked_img = img.copy()
        #cv2.threshold(value) or cv2.inRange(color1, color2)
        return masked_img


    def get_edge_mask(self, img):
        masked_img = img.copy()
        #cv2.filter(SOVEL) (just horizontal tho)
        #cv2.filter(CANNY) (compare this to the above?)
        return masked_img


    def apply_mask_to_img(self, mask, img):
        #make a '1's BLACK in the final img
        return img

