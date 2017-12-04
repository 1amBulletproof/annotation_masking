#!/usr/local/bin/python2
#@Author Brandon Tarney
#@Since  11/30/2017

#Edge  masking: use edge deteciton and morphology to detect text

from masker import Masker
import cv2
import numpy as np
import time

class EdgeMasker(Masker):
    def __init__(self, name="EdgeMasker"):
        self.name = name


    def mask_img_annotations(self, img):
        start_time = time.time()
        masked_img = img.copy()
        edge_mask = self.get_edge_mask(masked_img)
        end_time = time.time()
        Masker.performance = (end_time - start_time)
        return edge_mask


    # blur the image, find edges, and then find contours on the edged regions, filter for size 
    def get_edge_mask(self, img):
        masked_img = img.copy()
        gray_img = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(gray_img, (9, 9), 0)
        edged = cv2.Canny(blurred, 50, 100)
        (_, contours, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key = lambda x: x[1])

        # loop over the contours
        for (contour, _) in contours:
            # compute the bounding box for the rectangle
            (x, y, w, h) = cv2.boundingRect(contour)
            #Check to make sure this size makes sense
            if w >= 30 and w <= 85 and h >= 30 and h <= 85:
                masked_img[y:y+h, x:x+w] = (0,0,0)

        return masked_img




