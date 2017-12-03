#!/usr/local/bin/python2
#@Author Brandon Tarney
#@Since  11/30/2017

#Edge  masking: use edge deteciton and morphology to detect text

from masker import Masker
import cv2
import time

class EdgeMasker(Masker):
    def __init__(self, name):
        self.name = name

    def mask_img_annotations(self, img):
        start_time = time.time()
        masked_img = img.copy()
        edge_mask = self.get_edge_mask(masked_img)
        final_mask = cv2.bitwise_and(color_mask,
                edge_mask)
        final_img = self.apply_mask_to_img(final_mask, masked_img)
        end_time = time.time()
        Masker.performance = (end_time - start_time)
        return final_masked_img


    def get_edge_mask(self, img):
        #TODO: try other filters: cv2.filter(SOVEL) (just horizontal tho)
        masked_img = img.copy()

gray_img = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
# blur the image, find edges, and then find contours along
# the edged regions
blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
edged = cv2.Canny(blurred, 30, 150)
(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# loop over the contours
for (c, _) in cnts:
	# compute the bounding box for the rectangle
	(x, y, w, h) = cv2.boundingRect(c)

	# if the width is at least 7 pixels and the height
	# is at least 20 pixels, the contour is likely a digit
	if w >= 7 and h >= 20:
		# crop the ROI and then threshold the grayscale
		# ROI to reveal the digit
		roi = gray[y:y + h, x:x + w]
		thresh = roi.copy()
		T = mahotas.thresholding.otsu(roi)
		thresh[thresh > T] = 255
		thresh = cv2.bitwise_not(thresh)

		# deskew the image center its extent
		thresh = dataset.deskew(thresh, 20)
		thresh = dataset.center_extent(thresh, (20, 20))

		cv2.imshow("thresh", thresh)
        return masked_img


    def apply_mask_to_img(self, mask, img):
        #make a '1's BLACK in the final img
        return img

