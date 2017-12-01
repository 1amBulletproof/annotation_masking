#!/usr/bin/python2
#@author Brandon Tarney
#@since 11/29/2017

# Find and Mask Annotations (small text and possibly images) in video

import cv2
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

    #required arguments
    input_movie_file_path = args.input
    type_of_mask = args.type
    
    #optional arguments, see defaults above
    output_movie_file_path = args.output

    if not (output_movie_file_path == None):
        videoWriter = setupVideoWriter(videoCapture, output_movie_file_path)

    videoCapture = cv2.VideoCapture(input_movie_file_path)
    if not videoCapture.isOpened():
        print("Could not open " + input_movie_file_path + " movie. Exiting")

    #Strategy Design Patter; initialize the appropriate masker 
    masker = getMasker(type_of_mask)

    #read the video, frame by frame until the video is not opened or we can't read anymore
    while (videoCapture.isOpened() == True):
        ret, frame = videoCapture.read()
        if (ret == True):
            masked_frame = masker.maskImageAnnotations(frame)

            if not (output_movie_file_path == None):
                videoWriter.write(frame)

            cv2.imshow("Original", frame)
            cv2.imshow("Mask", masked_frame)
            cv2.waitKey(50)
        else:
            break

    #Release the video objects when everything is done
    videoCapture.release()
    if not (output_movie_file_path == None):
        videoWriter.release()

    #Close all frames
    cv2.destroyAllWindows()


def setupVideoWriter(videoCapture, output_movie_file_path):
    # VideoWriter settings (Codec help: https://gist.github.com/takuma7/44f9ecb028ff00e2132e)
    videoWriter = cv2.VideoWriter()
    videoCodec = cv2.VideoWriter_fourcc('M','J','P','G')
    fps = 20
    frame_width = int(videoCapture.get(3))
    frame_height = int(videoCapture.get(4))
    frame_shape = (frame_width, frame_height)
    videoWriter.open(
            output_movie_file_path, 
            videoCodec,
            fps, 
            frame_shape)


def getMasker(type_of_mask):
    #Get the appropriate masker: no very memory efficient but easy to read
    '''
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



