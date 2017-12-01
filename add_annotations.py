#!/usr/bin/python2
#@author Brandon Tarney
#@since 11/22/2017

# Add Annotations (small text and possibly images) to video

import cv2
import sys
import argparse

def main():
    arg_parser = argparse.ArgumentParser("add annotations (small text and possibly images) to video")

    arg_parser.add_argument("-i", "--input", required=True,
            help="input video file path")
    arg_parser.add_argument("-o", "--output", required=True,
            help="output video file path (must be .avi)")
    arg_parser.add_argument("-a", "--annotation", required=True,
            help="annotation text to add to each frame of video")
    arg_parser.add_argument("-m", "--move", action='store_true', required=False,
            help="move the annotation throughout the video")
    arg_parser.add_argument("-s", "--size", default=2, required=False,
            help="size of the annotations (generally 1-4)")
    
    args = arg_parser.parse_args()

    #required arguments
    input_movie_file_path = args.input
    output_movie_file_path = args.output
    annotation_text = args.annotation

    #optional arguments, see defaults above
    isMoving = args.move
    text_size = int(args.size)
    
    videoCapture = cv2.VideoCapture(input_movie_file_path)
    videoWriter = cv2.VideoWriter()

    # VideoWriter settings (Codec help: https://gist.github.com/takuma7/44f9ecb028ff00e2132e)
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

    if not videoCapture.isOpened():
        print("Could not open " + input_movie_file_path + " movie. Exiting")

    #read the video, frame by frame until the video is not opened or we can't read anymore
    text_location = (100,100)
    while (videoCapture.isOpened() == True):
        ret, frame = videoCapture.read()
        if (ret == True):
            text_color = (255, 255, 255)
            text_location = getAnnotationLocation(text_location, isMoving)
            frame = cv2.putText(frame, annotation_text, text_location, 
                    cv2.FONT_HERSHEY_SIMPLEX, text_size, text_color)
            videoWriter.write(frame)
            cv2.imshow("frame", frame)
            cv2.waitKey(50)
        else:
            break

    #Release the video objects when everything is done
    videoWriter.release()
    videoCapture.release()

    #Close all frames
    cv2.destroyAllWindows()


def getAnnotationLocation(location, isMoving):
    if isMoving:
        if location[0] < 600:
            location = (location[0] + 15, location[1])
        else:
            location = (100,100)
    return location


if __name__ == "__main__":
    main()



