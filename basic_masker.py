#!/usr/local/bin/python2
#@Author Brandon Tarney
#@Since  11/30/2017

#Basic masking: just mask all the places annotations MIGHT be
#This is effectively what is done currently at work and the baseline for comparison

from masker import Masker
import cv2

class BasicMasker(Masker):
    def __init__(self, name):
        self.name = name

    def maskImageAnnotations(self, img):
        masked_img = img.copy()
        self.img_x_dim = masked_img.shape[1]
        self.img_y_dim = masked_img.shape[0]
        self.setTopRectangle(masked_img)
        self.setLeftRectangle(masked_img)
        self.setRightRectangle(masked_img)
        self.setBottomRectangle(masked_img)
        return masked_img

    def setTopRectangle(self, img):
        upper_left = (0,0)
        lower_right = ( self.img_x_dim, self.img_y_dim/5 )
        self.setRectangle(img, upper_left, lower_right)

    def setLeftRectangle(self, img):
        upper_left = (0,0)
        lower_right = ( self.img_x_dim/5, self.img_y_dim )
        self.setRectangle(img, upper_left, lower_right)

    def setRightRectangle(self, img):
        upper_left = (self.img_x_dim - self.img_x_dim/5, 0)
        lower_right = ( self.img_x_dim, self.img_y_dim )
        self.setRectangle(img, upper_left, lower_right)

    def setBottomRectangle(self, img):
        upper_left = (0, self.img_y_dim - self.img_y_dim/5)
        lower_right = ( self.img_x_dim, self.img_y_dim )
        self.setRectangle(img, upper_left, lower_right)

    def setRectangle(self, img, pt1, pt2):
        rect_color = (0,0,0) # black
        rect_thickness = -1 # filled
        img_with_rect = cv2.rectangle(img, pt1, pt2, rect_color, rect_thickness)
        return img_with_rect
