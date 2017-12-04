#!/usr/local/bin/python2
#@Author Brandon Tarney
#@Since  11/30/2017

#Combo masking: combine color masking and morph detection masks

from masker import Masker
from color_masker import ColorMasker
from morph_masker import MorphMasker
import cv2
import time

class ComboMasker(Masker):
    def __init__(self, name="ComboMasker"):
        self.name = name


    #Use color_masker + morph_masker & combine images
    def mask_img_annotations(self, img):
        start_time = time.time()
        color_masked_img  = img.copy()
        color_masker = ColorMasker("Color Masker", "green")
        color_masked_img = color_masker.mask_img_annotations(img)
        morph_masked_img  = img.copy()
        morph_masker = MorphMasker()
        morph_masked_img = morph_masker.mask_img_annotations(img)

        combined_mask_img = cv2.bitwise_or( color_masked_img,
                morph_masked_img)
        end_time = time.time()
        Masker.performance = (end_time - start_time)
        return combined_mask_img



