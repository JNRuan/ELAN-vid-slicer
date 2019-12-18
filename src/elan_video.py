#!/usr/bin/python3
##############################################################################
# ELAN Video Object
#
# Makes extensive use of the Elan data structure provided by pympi library.
#
# Author: Jameson Nguyen (JNRuan), University of Queensland
#
##############################################################################
from pympi import Elan
import os
import sys

##############################################################################

class ElanVideo:
    """Represents an ELAN annotated video file.

    Data is extracted from ELAN (.eaf) files and their associated video file.
    """
    def __init__(self, input_dir: str, elan_fname: str=None, tier_name: str=None, tier_index: int=1):
        self._eaf = self.load_elan(input_dir, elan_fname)

    @property
    def eaf(self):
        return self._eaf

    def load_elan(self, input_dir: str, elan_fname: str=None):
        eaf = None
        elan_file = ''

        # Elan file provided, load directly.
        if elan_fname:
            if elan_fname.endswith('.eaf'):
                elan_file = os.path.join(input_dir, elan_fname)
            else:
                elan_file = os.path.join(input_dir, f'{elan_fname}.eaf')
        else:
            # No Elan file, load indirectly - inform user if not found or there is more than one.
            elan_file_list = [file for file in os.listdir(input_dir) if file.endswith('.eaf')]
            if len(elan_file_list) == 0:
                print(f"No Elan (.eaf) files found in {input_dir}.")
            elif len(elan_file_list) > 1:
                print(f"More than one Elan (.eaf) file found in {input_dir}",
                        " by default using the first file in folder."
                        " Please specify the file you want to use with the optional",
                        " argument -e or --elan_file on script execution")
                elan_file = os.path.join(input_dir, elan_file_list[0])
            else:
                elan_file = os.path.join(input_dir, elan_file_list[0])

        try:
            eaf = Elan.Eaf(elan_file)
        except Exception as e:
            print(f"Error on attempting to load Elan file from {input_dir}/{elan_file}")
            print(e)

        if eaf:
            print(f"Loaded elan file: {elan_file}")
        return eaf
