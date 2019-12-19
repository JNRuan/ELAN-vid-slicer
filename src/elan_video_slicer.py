#!/usr/bin/python3
##############################################################################
# ELAN Video Slicer Util
#
# Main driver file for ELAN Video Slicer utility.
#
# Version: 0.1
# Author: Jameson Nguyen (JNRuan), University of Queensland
##############################################################################
# Libary Imports
from datetime import timedelta
import argparse
import os
import subprocess

# Module Imports
from elan_video import ElanVideo

##############################################################################
class ElanVideoSlicer:
    """Slices videos into frames based on annotations from ELAN files."""
    def __init__(self, args):
        self.elan_video = ElanVideo(args.input_dir, args.elan_file)
        self.tier_name = args.tier_name
        self.tier_index = args.tier_index
        self.output_dir = args.output_dir
        self.fps = args.fps

    def get_annotations(self):
        if self.tier_name:
            print(f"Retrieving annotations from tier name {self.tier_name}")
            return self.elan_video.get_annotations_from_tier(self.tier_name)
        else:
            print(f"Retrieving annotations from tier index {self.tier_index}")
            tier_name = self.elan_video.get_tier_by_index(self.tier_index - 1)
            return self.elan_video.get_annotations_from_tier(tier_name)

    def run(self):
        """Runs Elan Video Slicer: Calls ffmpeg on the cmd line so user will
        need to have ffmpeg installed.
        """


def main():
    # Setup Parser
    parser_desc = '''Elan Video Slicer: Create video frames for annotations from ELAN.'''
    parser = argparse.ArgumentParser(description=parser_desc,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Positional Args (Required)
    parser.add_argument('input_dir',
                        type=str,
                        help='''Input directory containing ELAN (.eaf) and
                                coresponding video file.''')
    # Optional Args
    parser.add_argument('-o', '--output_dir',
                        type=str,
                        default='./output',
                        help='''Output directory for parsed annotations with
                                video frames. Each annotation will contain its own folder.''')
    parser.add_argument('-f', '--fps',
                        type=int,
                        default=10,
                        help='Frames per second (fps) to slice videos. Input a number (integer).')
    parser.add_argument('-e', '--elan_file',
                        type=str,
                        help='Elan file name. Specify if is more than one elan file in the input directory.')
    parser.add_argument('-t', '--tier_name',
                        type=str,
                        help='Tier to extract annotations. Input should be a tier name (string).')
    parser.add_argument('-i', '--tier_index',
                        type=int,
                        default=1,
                        help='''Tier index to extract annotations from.
                                Input should be a number (integer). Top tier index = 1.''')

    args = parser.parse_args()

    # Check Output
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Run App
    elan_vid_slicer = ElanVideoSlicer(args)
    if elan_vid_slicer.elan_video.eaf:
        # TESTING
        # annotations = elan_vid_slicer.get_annotations()
        # print(annotations)
        #
        # # TIME TESTER
        # start, end, annotation = annotations[0]
        # start = str(timedelta(milliseconds=start))
        # end = str(timedelta(milliseconds=end))
        # print(f"{start} - {end}: {annotation}")
        #
        # fname = elan_vid_slicer.elan_video._elan_fname
        # fname = os.path.splitext(fname)[0]
        # vid_name = os.path.join(args.input_dir, f'{fname}.mp4')
        # print(vid_name)
        # fps = args.fps
        # out = os.path.join(args.output_dir, annotation, f'{fname}_{annotation}_{fps}fps_%04d.jpg')
        #
        # subprocess.call(['ffmpeg',
        #                 '-i', vid_name,
        #                 '-ss', start,
        #                 '-to', end,
        #                 '-vf',
        #                 f'fps={fps}',
        #                 f'{fname}_{fps}fps_%04d.jpg'
        #                 ], shell=True)

        print("EAF LOADED.")
    else:
        print("Failed to load or find an ELAN file and video to use. Please check directory and usage.")
        print("Run script with optional argument -h for help: e.g. python3 elan_video_slicer.py -h")


if __name__ == '__main__':
    main()
