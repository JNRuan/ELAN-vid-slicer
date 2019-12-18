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
import argparse
import os
import subprocess

# Module Imports
from elan_video import ElanVideo

##############################################################################
class ElanVideoSlicer:
    """Slices videos into frames based on annotations from ELAN files."""
    def __init__(self, args):
        self.elan_video = ElanVideo(args.input_dir, args.elan_file, args.tier_name, args.tier_index)


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
                        default='../output',
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
    elan_video_slicer = ElanVideoSlicer(args)
    if elan_video_slicer.elan_video.eaf:
        print(type(elan_video_slicer.elan_video.eaf))
        print(elan_video_slicer.elan_video.eaf.get_tier_names())
        print(elan_video_slicer.elan_video.eaf.get_annotation_data_for_tier('RH-IDgloss'))
        print("EAF LOADED.")
    else:
        print("EAF LOAD FAILED.")


if __name__ == '__main__':
    main()
