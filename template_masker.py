#!/usr/local/bin/python2
#@Author Brandon Tarney
#@Since  11/30/2017

#Template  masking: use template matching to detect text

from masker import Masker
import cv2
import numpy as np
import time
import glob

class TemplateMasker(Masker):
    def __init__(self, name="TemplateMasker"):
        self.name = name
        self.gray_templates_edges = self.get_template_images()


    def mask_img_annotations(self, img):
        start_time = time.time()
        masked_img = img.copy()
        masked_img  = self.get_template_mask(masked_img)
        end_time = time.time()
        Masker.performance = (end_time - start_time)
        return masked_img


    # Template matching using edges
    def get_template_mask(self, img):
        masked_img = img.copy()
        gray_img = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
        gray_img_edges = cv2.Canny(gray_img, 50, 200)
        gray_template_img = cv2.imread("../images/letter_A.jpg", 0)

        #Search for best match of each letter
        for gray_template_edges in self.gray_templates_edges:

            #Get the shape of the template image for masking
            width, height = gray_template_edges.shape[::-1]

            result = cv2.matchTemplate(gray_img_edges, gray_template_edges, cv2.TM_CCOEFF)

            #Mask the best match for now for each letter
            threshold = 0.9
            loc = np.where(result >= threshold)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            thickness = -1 #fill
            color = (0,0,0) # black
            point = (maxLoc[0], maxLoc[1])
            point2 = (maxLoc[0] + width, maxLoc[1] + height)
            cv2.rectangle(masked_img, point, point2, color, thickness)


        return masked_img


    def get_template_images(self):
        gray_image_edges = list()
        for img_path in glob.glob("../images/characters/*"):
            tmp_gray_img = cv2.imread(img_path)
            tmp_gray_img = cv2.cvtColor(tmp_gray_img, cv2.COLOR_BGR2GRAY)
            tmp_gray_img = cv2.Canny(tmp_gray_img, 50, 200)
            gray_image_edges.append(tmp_gray_img)

        return gray_image_edges





