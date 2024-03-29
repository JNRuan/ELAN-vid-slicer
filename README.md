# ELAN Vid Slicer

**Author**: James Nguyen, University of Queensland

**Version**: 0.2

The ELAN Vid Slicer is a tool created to perform a data pre-processing task involving annotated Elan (.eaf) files and video recordings of Auslan signers. This tool allows you to extract frames from a recording based on important annotations detected at a transcription tier within Elan (.eaf) files. It was created to extract annotated sequences of frames from Auslan signing videos that are part of the ELAR Auslan dataset [1].

If you have mutiple elan files for different videos, use mode --multi 1 when running script. See usage and folder structure for details.

## Dependencies

* ffmpeg ([Download](https://www.ffmpeg.org/download.html))
* pympi ([Repo](https://github.com/dopefishh/pympi))
* tqdm ([Repo](https://github.com/tqdm/tqdm))

For ffmpeg, follow install instructions and ensure environment/path is set.

For pympi and tqdm, use `pip install library_name` in terminal/cmd, see repo links for instructions/package names.

## Installation

Clone this repository with `git clone https://github.com/JNRuan/ELAN-vid-slicer.git` or download and extract from [Releases](https://github.com/JNRuan/ELAN-vid-slicer/releases).

## Folder Structure

Expected folder structure. Ensure that the video file and elan file (.eaf) have the same filename. Ideally there should only be one .eaf file per folder.

```
Root_Input_Folder/
-- Folder1/
---- elan_file.eaf
---- elan_file.mp4
-- Folder2/
---- elan_file.eaf
---- elan_file.mp4
```

## Usage

**Note: Python 3 required**

Navigate to the folder containing `elan_video_slicer.py`.

For help: `python elan_video_slicer.py -h`

To run: `python elan_video_slicer path/to/folder/elan_file.eaf [optional args]`

Example: 
```
# Save annotated sequences to output_folder
# Use tier name 'RH-IDgloss'
# Run video slice on all folders with .eaf files (see folder structure)
python elan_video_slicer "path/to/Root_Input_Folder" -o "path/to/output_folder" -t "RH-IDgloss" -m 1
```

Optional args:

`[-o | --output_dir] : Specify path output should be saved in. Default = "../output"`

`[-f | --fps] : Specify fps, default fps = 10. E.g., --fps 20 sets frames per second to 20.`

`[-e | --elan_file] : Specify elan file name if required (eg., there is more than one). E.g., -e "myelanfile.eaf"`

`[-vt | --video_type] : Specify video file extension. Default = "mp4". E.g., -vt "mov"`

`[-t | --tier_name] : Specify exact tier name. e.g., -t "tier_name"`

`[-i | --tier_index] : Specify tier index. Default = 1. E.g., -i 2 for 2nd tier in elan file.`

`[-m | --multi] : Mode when input directory contains many folders with elan files. Default = 0 for single folder mode. Use -m 1 for multi folder mode.`


## Future

GUI for better user experience...

If you encounter any bugs or issues, please make a ticket under issues.

## References
[1] T. Johnston, “From archive to corpus: Transcription and annotation in the creation of signed language corpora,” IJCL, vol. 15, no. 1, pp. 106–131, Apr. 2010, doi: 10.1075/ijcl.15.1.05joh.

