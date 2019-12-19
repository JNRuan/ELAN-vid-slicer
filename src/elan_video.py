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
        self._eaf = None
        self._path = None
        self._elan_fname = None
        self._name = None
        self._load_elan(input_dir, elan_fname)

    @property
    def eaf(self):
        return self._eaf

    def _load_elan(self, input_dir: str, elan_fname: str=None):
        # Elan file provided, load directly.
        if elan_fname:
            if elan_fname.endswith('.eaf'):
                self._path = os.path.join(input_dir, elan_fname)
            else:
                self._path = os.path.join(input_dir, f'{elan_fname}.eaf')
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
                self._path = os.path.join(input_dir, elan_file_list[0])
            else:
                self._path = os.path.join(input_dir, elan_file_list[0])

        try:
            self._eaf = Elan.Eaf(self._path)
        except Exception as e:
            print(f"Error on attempting to load Elan file from {self._path}")
            print(e)

        if self._eaf:
            self._elan_fname = os.path.basename(self._path)
            self._name = os.path.splitext(self._elan_fname)[0]
            print(f"Loaded elan file: {self._elan_fname}")

    def get_tier_names(self):
        """Retrieves a list of all available tier names in tier index order.

        :returns: List of tier names (str).
        """
        return list(self._eaf.get_tier_names())

    def get_tier_by_index(self, tier_index: int):
        """Returns tier name at tier index.

        Note this is zero-indexed, so tier index 1 should be passed as 0.

        :param int tier_index: Index of tier name.
        :returns: Tier name at tier index (str), else None.
        """
        tier_names = self.get_tier_names()
        if tier_index > len(tier_names):
            print(f"Tier index exceeds the number of tiers.")
            return None
        return self.get_tier_names()[tier_index]

    def get_annotations_from_tier(self, tier: str):
        """Retrieves all annotations from the provided tier.

        :param str tier: The tier name to retrieve from.
        :returns: List of annotations at tier.
        """
        try:
            annotations = self._eaf.get_annotation_data_for_tier(tier)
        except KeyError as e:
            print(f"Tier: {tier} not found, please check tier name or use tier index.")
        return annotations
