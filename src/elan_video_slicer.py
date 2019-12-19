#!/usr/bin/python3
##############################################################################
# ELAN Video Slicer Util
#
# Main driver file for ELAN Video Slicer utility. Requires ffmpeg.
#
# Version: 0.1
# Author: Jameson Nguyen (JNRuan), University of Queensland
##############################################################################
# Libary Imports
from datetime import timedelta
from typing import List, Tuple
import argparse
import os
import re
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
        self.fps = args.fps
        # Make Output Folder, 'OutputFolder/fps_n'
        self.output_path = os.path.join(args.output_dir, f"fps_{self.fps}")
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def get_annotations(self) -> List[Tuple[int, int, str]]:
        """Get all annotations from user provided tier name or tier index.

        :returns: List of annotations with start and end times in milliseconds,
                    at selected tier. (start, end, annotation)
        """
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
        annotations = self.get_annotations()
        for start_time, end_time, annotation in annotations:
            t_start = str(timedelta(milliseconds=start_time))
            t_end = str(timedelta(milliseconds=end_time))
            label = annotation.lower()
            label = re.sub(r'[\\/*?:"<>|]', "-", label)
            outpath = os.path.join(self.output_path, label)
            if not os.path.exists(outpath):
                os.makedirs(outpath)
            inpath = os.path.dirname(self.elan_video.path)
            self._subprocess_call_ffmpeg(inpath, outpath,
                                         t_start, t_end,
                                         self.elan_video.name,
                                         label,
                                         self.fps)

    def _subprocess_call_ffmpeg(self, inpath: str, outpath: str,
                                start_time, end_time,
                                id: str, annotation: str,
                                fps: int):
        """Calls ffmpeg subroutine.

        Example:
            ffmpeg -i id.mp4 -ss hh:mm:ss.ms -to hh:mm:ss.ms -vf fps=10 outpath/annotation/id_annotation_10fps_%04d.jpg
        """
        vid_path = os.path.join(inpath, f"{id}.mp4")
        frame_name = f"{id}_{annotation}_{fps}fps_%04d.jpg"
        frame_path = os.path.join(outpath, frame_name)
        subprocess.call([
            'ffmpeg',
            '-i', vid_path,
            '-ss', start_time,
            '-to', end_time,
            '-vf', f'fps={fps}',
            frame_path
        ], shell=True)

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

    # Run App
    elan_vid_slicer = ElanVideoSlicer(args)
    if elan_vid_slicer.elan_video.eaf:
        elan_vid_slicer.run()
    else:
        print("Failed to load or find an ELAN file and video to use. Please check directory and usage.")
        print("Run script with optional argument -h for help: e.g. python3 elan_video_slicer.py -h")


if __name__ == '__main__':
    main()
