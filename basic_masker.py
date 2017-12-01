#!/usr/local/bin/python2
#@Author Brandon Tarney
#@Since  11/30/2017

#Basic masking: just mask all the places annotations MIGHT be
#This is effectively what is done currently at work and the baseline for comparison

from masker import Masker
import cv2
import time

class BasicMasker(Masker):
    def __init__(self, name):
        self.name = name
        self.performance = 0

    def mask_img_annotations(self, img):
        start_time = time.time()
        masked_img = img.copy()
        self.img_x_dim = masked_img.shape[1]
        self.img_y_dim = masked_img.shape[0]
        self.set_top_rectangle(masked_img)
        self.set_left_rectangle(masked_img)
        self.set_right_rectangle(masked_img)
        self.set_bottom_rectangle(masked_img)
        end_time = time.time()
        self.performance = (end_time - start_time)
        return masked_img

    def set_top_rectangle(self, img):
        upper_left = (0,0)
        lower_right = ( self.img_x_dim, self.img_y_dim/5 )
        self.set_rectangle(img, upper_left, lower_right)

    def set_left_rectangle(self, img):
        upper_left = (0,0)
        lower_right = ( self.img_x_dim/5, self.img_y_dim )
        self.set_rectangle(img, upper_left, lower_right)

    def set_right_rectangle(self, img):
        upper_left = (self.img_x_dim - self.img_x_dim/5, 0)
        lower_right = ( self.img_x_dim, self.img_y_dim )
        self.set_rectangle(img, upper_left, lower_right)

    def set_bottom_rectangle(self, img):
        upper_left = (0, self.img_y_dim - self.img_y_dim/5)
        lower_right = ( self.img_x_dim, self.img_y_dim )
        self.set_rectangle(img, upper_left, lower_right)

    def set_rectangle(self, img, pt1, pt2):
        rect_thickness = -1 # filled
        img_with_rect = cv2.rectangle(img, pt1, pt2, Masker.mask_color, rect_thickness)
        return img_with_rect
