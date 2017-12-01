#!/usr/bin/python2
#@author Brandon Tarney
#@since 11/29/2017

# Find and Mask Annotations (small text and possibly images) in video

import cv2
import numpy as np
import sys
import argparse
from masker import Masker
from basic_masker import BasicMasker

def main():
    arg_parser = argparse.ArgumentParser("find and mask annotations (small text and possibly images) in video")

    arg_parser.add_argument("-i", "--input", required=True,
            help="input video file path")
    arg_parser.add_argument("-t", "--type", required=True,
            help="type of masking: basic, color, morphology, template, feature, advanced, combo",
            default="basic")
    arg_parser.add_argument("-o", "--output", required=False,
            help="output video file path (must be .avi)")
    
    args = arg_parser.parse_args()
    print("")
    print("arguments: " + str(args))
    print("")

    #required arguments
    input_movie_file_path = args.input
    type_of_mask = args.type
    
    #optional arguments, see defaults above
    output_movie_file_path = args.output

    vid_cap = cv2.VideoCapture(input_movie_file_path)

    if not (output_movie_file_path == None):
        vid_writer = setup_vid_writer(vid_cap, output_movie_file_path)

    if not vid_cap.isOpened():
        print("Could not open " + input_movie_file_path + " movie. Exiting")

    #Strategy Design Patter; initialize the appropriate masker 
    masker = getMasker(type_of_mask)

    #read the video, frame by frame until the video is not opened or we can't read anymore
    mask_sizes = list()
    mask_times = list()
    while (vid_cap.isOpened() == True):
        ret, frame = vid_cap.read()
        if (ret == True):
            masked_frame = masker.mask_img_annotations(frame)

            mask_sizes.append(masker.get_mask_size(masked_frame))
            mask_times.append(masker.performance)

            if not (output_movie_file_path == None):
                vid_writer.write(masked_frame)

            cv2.imshow("Original", frame)
            cv2.imshow("Mask", masked_frame)
            cv2.waitKey(50)
        else:
            break

    #Release the video objects when everything is done
    vid_cap.release()
    if not (output_movie_file_path == None):
        vid_writer.release()

    #Close all frames
    cv2.destroyAllWindows()

    print("Avg mask size: " + str(np.average(mask_sizes)) + " pixels")
    print("Avg mask time: " + str(np.average(mask_times)) + " seconds")


def setup_vid_writer(videoCapture, output_movie_file_path):
    # VideoWriter settings (Codec help: https://gist.github.com/takuma7/44f9ecb028ff00e2132e)
    vid_writer = cv2.VideoWriter()
    videoCodec = cv2.VideoWriter_fourcc('M','J','P','G')
    fps = 20
    frame_width = int(videoCapture.get(3))
    frame_height = int(videoCapture.get(4))
    frame_shape = (frame_width, frame_height)
    vid_writer.open(
            output_movie_file_path, 
            videoCodec,
            fps, 
            frame_shape)
    return vid_writer


def getMasker(type_of_mask):
    #Get the appropriate masker: no very memory efficient but easy to read
    '''
    #PRIORITIZE: stuff we haven't done much-of: template matching, feature matching, advanced (i.e. the book's solution) & combo color + morphology
    maskers = {'basic' : BasicMasker(),
            'color' : ColorMasker(),
            'morphology' : MorphMasker(),
            'template' : TemplateMasker(),
            'feature' : FeatureMasker(),
            'advanced' : AdvancedMasker(),
            'combo' : ComboMasker() }
    return maskers.get(type_of_mask)
            '''
    maskers = { 'basic' : BasicMasker("Basic Masker") }
    return maskers.get(type_of_mask)


if __name__ == "__main__":
    main()



