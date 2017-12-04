#!/usr/local/bin/python2
#@Author Brandon Tarney
#@Since  11/30/2017

#morphology  masking: use morphology after thresholding to detect text

from masker import Masker
import cv2
import numpy as np
import time

class MorphMasker(Masker):
    def __init__(self, name="MorphMasker"):
        self.name = name


    def mask_img_annotations(self, img):
        start_time = time.time()
        masked_img = img.copy()
        masked_img = self.get_edge_mask(masked_img)
        end_time = time.time()
        Masker.performance = (end_time - start_time)
        return masked_img


    def get_edge_mask(self, img):
        masked_img = img.copy()
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #Blur the image to reduce the noise
        blurred_gray_img = cv2.blur(gray_img, (11, 11))

        #Adaptive threshold to control for different lighting but this will produce noise!
        threshold_mask = cv2.adaptiveThreshold(blurred_gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY_INV, 7, 1)
        '''
        cv2.imshow("thresh", threshold_mask)
        cv2.waitKey(0)
        '''

        #Remove the noise
        kernel = np.ones((3, 3), np.uint8)
        low_noise_mask = cv2.erode(threshold_mask, kernel, iterations=2)
        '''
        cv2.imshow("erode", low_noise_mask)
        cv2.waitKey(0)
        '''

        #Combine the text area into word-blobs so they are large
        mask = cv2.dilate(low_noise_mask, kernel, iterations=7)
        '''
        cv2.imshow("dilate", mask)
        cv2.waitKey(0)
        '''

        #Find the contours of the masked regions (this will get us word-blobs)
        contour_img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # compute the bounding box for the rectangle
            (x, y, w, h) = cv2.boundingRect(contour)
            #Check for "blobs of words" which should be of decent size (which eliminates most noise!)
            if w >= 50 and w <= 500 and h >= 40 and h <= 100: 
                # crop the ROI and then threshold the grayscale
                # ROI to reveal the digit
                masked_img[y:y+h, x:x+w] = (0,0,0)
        return masked_img


