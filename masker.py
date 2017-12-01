#!/usr/local/bin/python2
#@Author Brandon Tarney
#@Since  11/30/2017

#Masker abstract super class

class Masker():
    def __init__(self, name):
        self.name = name

    def maskImageAnnotations(self, image):
        raise NotImplementedError("Abstract method called")
    def calculateMaskedArea(self, masked_image):
        raise NotImplementedError("Abstract method called")
