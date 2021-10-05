#!/usr/bin/python3
##############################################################################
# ELAN Video Slicer Util
#
# Main driver file for ELAN Video Slicer utility. Requires ffmpeg.
#
# Version: 0.2
# Author: Jameson Nguyen (JNRuan), University of Queensland
##############################################################################
# Libary Imports
from datetime import timedelta
from typing import List, Tuple
from tqdm import tqdm
import argparse
import os
import re
import subprocess

# Module Imports
from elan_video import ElanVideo

##############################################################################
_VERSION = '0.2'
_PROMPT_DIVIDER = '=' * 80

class ElanVideoSlicer:
    """Slices videos into frames based on annotations from ELAN files."""
    def __init__(self, args, elan_folder: str):
        self.elan_video = ElanVideo(elan_folder, args.elan_file)
        self.vid_ext = args.video_type
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
            print(f"Tier name: {tier_name}")
            return self.elan_video.get_annotations_from_tier(tier_name)

    def run(self):
        """Runs Elan Video Slicer: Calls ffmpeg on the cmd line so user will
        need to have ffmpeg installed.
        """
        annotations = self.get_annotations()
        if len(annotations) == 0:
            print(f"Could not retrieve annotations, please check parameters.")
            return
        print(f"Found: {len(annotations)} annotations.")
        print("Slicing by annotations, please wait...")
        for i in tqdm(range(len(annotations))):
            start_time, end_time, annotation = annotations[i]
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
                                         self.fps,
                                         self.vid_ext)

    def _subprocess_call_ffmpeg(self, inpath: str, outpath: str,
                                start_time, end_time,
                                id: str, annotation: str,
                                fps: int, vid_ext: str):
        """Calls ffmpeg subroutine.

        Example:
            ffmpeg -i id.mp4 -ss hh:mm:ss.ms -to hh:mm:ss.ms -vf fps=10 outpath/annotation/id_annotation_10fps_%04d.jpg
        """
        vid_path = os.path.join(inpath, f"{id}.{vid_ext}")
        # frame_name = f"{id}_{annotation}_{fps}fps_%04d.jpg"
        frame_name = f"{id}_%04d.jpg"
        frame_path = os.path.join(outpath, frame_name)
        subprocess.call([
            'ffmpeg',
            '-i', vid_path,
            '-ss', start_time,
            '-to', end_time,
            '-vf', f'fps={fps}',
            '-qscale:v', '2',
            '-loglevel', '0',
            frame_path
        ], shell=True)


def run_multi_slice(args):
    print(f"Compiling your ELAN Folders from: {args.input_dir}")
    folder_list = [folder[0] for folder in os.walk(args.input_dir)]
    print(f"Found {len(folder_list)} folders.")
    print(_PROMPT_DIVIDER)
    for elan_folder in folder_list[1:]:
        run_single_slice(args, elan_folder)


def run_single_slice(args, elan_folder: str):
    # Run App
    print(f"Slicing from {elan_folder}")
    elan_vid_slicer = ElanVideoSlicer(args, elan_folder)
    if elan_vid_slicer.elan_video.eaf:
        elan_vid_slicer.run()
        print(_PROMPT_DIVIDER)
    else:
        print(f"Failed to load or find an ELAN file and video to use. Please check {elan_folder}")
        print("Run script with optional argument -h for help: e.g. python3 elan_video_slicer.py -h")

def main():
    # Setup Parser
    parser_desc = '''Elan Video Slicer: Create video frames for annotations from ELAN.'''
    parser = argparse.ArgumentParser(description=parser_desc,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Positional Args (Required)
    parser.add_argument('input_dir',
                        type=str,
                        help='''Input directory containing ELAN (.eaf) and
                                coresponding video file. If mutiple folders use arg --multi 1''')
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
    parser.add_argument('-vt', '--video_type',
                        type=str,
                        default='mp4',
                        help="Specify the video file extension, eg., 'mp4', 'mov'.")
    parser.add_argument('-t', '--tier_name',
                        type=str,
                        help='Tier to extract annotations. Input should be a tier name (string).')
    parser.add_argument('-i', '--tier_index',
                        type=int,
                        default=1,
                        help='''Tier index to extract annotations from.
                                Input should be a number (integer). Top tier index = 1.''')
    parser.add_argument('-m', '--multi',
                        type=int,
                        default=0,
                        help='''If --multi 1, runs in multi folder mode and
                                attempts to slice all folders inside provided
                                input_dir. If --multi 0, then will use
                                input dir to find Elan (.eaf) and video.''')

    args = parser.parse_args()

    print(f"Welcome to ELAN Vid Slicer v{_VERSION}")
    print(_PROMPT_DIVIDER)
    print("Parameters:")
    print(f"Input Dir: {args.input_dir}")
    print(f"Output Dir: {args.output_dir}")
    print(f"Elan File (Optional): {args.elan_file} | Tier Index: {args.tier_index} | Tier Name (Optional): {args.tier_name}")
    print(f"Video Type/Ext: {args.video_type}")
    print(f"Mode: FPS = {args.fps} | Multi = {args.multi}")
    print(_PROMPT_DIVIDER)

    if args.multi == 0:
        run_single_slice(args, args.input_dir)
    else:
        run_multi_slice(args)

    print("Shutting down Elan Vid Slicer...")

if __name__ == '__main__':
    main()
