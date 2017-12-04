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
from color_masker import ColorMasker
from edge_masker import EdgeMasker
from morph_masker import MorphMasker
from combo_masker import ComboMasker
from template_masker import TemplateMasker


def main():
    #Handle input arguments
    arg_parser = argparse.ArgumentParser("find and mask annotations (small text and possibly images) in video")
    arg_parser._action_groups.pop()
    required = arg_parser.add_argument_group('required arguments')
    optional = arg_parser.add_argument_group('optional arguments')

    required.add_argument("-i", "--input",
            help="input video file path",required=True)
    required.add_argument("-t", "--type", required=True,
            help="type of masking: basic, color, edge, morphology, template, advanced, combo",
            default="basic")
    optional.add_argument("-o", "--output", required=False,
            help="output video file path (must be .avi)")
    
    args = arg_parser.parse_args()
    print("")
    print("input arguments: " + str(args))
    print("")

    #required arguments
    input_movie_file_path = args.input
    type_of_mask = args.type
    
    #optional arguments, see defaults above
    output_movie_file_path = args.output

    #Setup Video read/write
    vid_cap = cv2.VideoCapture(input_movie_file_path)

    if not (output_movie_file_path == None):
        vid_writer = setup_vid_writer(vid_cap, output_movie_file_path)

    if not vid_cap.isOpened():
        print("Could not open " + input_movie_file_path + " movie. Exiting")

    #Strategy Design Pattern: initialize the appropriate masker 
    maskers = { 
            'basic' : BasicMasker("Basic Masker"),
            'color' : ColorMasker("Color Masker", "green") ,
            'edge' : EdgeMasker("Edge & Threshold Masker"),
            'morph' : MorphMasker("Morphology Masker"),
            'combo' : ComboMasker("Combo Masker"),
            'template' : TemplateMasker("Template Masker") 
            }
    masker = maskers.get(type_of_mask)

    #read the video, frame by frame until the video is not opened or we can't read anymore
    mask_sizes = list()
    mask_times = list()
    while (vid_cap.isOpened() == True):
        ret, frame = vid_cap.read()
        if (ret == True):
            #Apply the mask
            masked_frame = masker.mask_img_annotations(frame)

            #Get masking metrics
            mask_sizes.append(masker.get_mask_size(masked_frame))
            mask_times.append(Masker.performance)

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

    #Display masking metrics
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


if __name__ == "__main__":
    main()



