#!/usr/bin/env python3
"""Module containing the AverageStiffness class and the command line interface."""

import shutil
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from biobb_dna.utils import constants
from biobb_dna.utils.loader import read_series
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger
from biobb_common.tools import file_utils as fu
from biobb_common.configuration import settings


class AverageStiffness(BiobbObject):
    """
    | biobb_dna AverageStiffness
    | Calculate average stiffness constants for each base pair of a trajectory's series.

    Args:        
        input_ser_path (str): Path to .ser file for helical parameter. File is expected to be a table, with the first column being an index and the rest the helical parameter values for each base/basepair. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/canal_output_roll.ser>`_. Accepted formats: ser (edam:format_2330).
        output_csv_path (str): Path to .csv file where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/stiffness/stiffavg_roll.csv>`_. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/stiffness/stiffavg_roll.jpg>`_. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **KT** (*float*) - (0.592186827) Value of Boltzmann temperature factor.
            * **sequence** (*str*) - (None) Nucleic acid sequence corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *usecols* option).
            * **helpar_name** (*str*) - (None) helical parameter name.
            * **seqpos** (*list*) - (None) list of sequence positions (columns indices starting by 0) to analyze.  If not specified it will analyse the complete sequence.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.stiffness.average_stiffness import average_stiffness

            prop = { 
                'helpar_name': 'twist',
                'sequence': 'GCAT',
            }
            average_stiffness(
                input_ser_path='/path/to/twist.ser',
                output_csv_path='/path/to/table/output.csv',
                output_jpg_path='/path/to/table/output.jpg',
                properties=prop)
    Info:
        * wrapped_software:
            * name: In house
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_ser_path, output_csv_path, output_jpg_path,
                 properties=None, **kwargs) -> None:
        properties = properties or {}
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_ser_path': input_ser_path,
            },
            'out': {
                'output_csv_path': output_csv_path,
                'output_jpg_path': output_jpg_path
            }
        }

        self.properties = properties
        self.sequence = properties.get("sequence")
        self.KT = properties.get(
            "KT", 0.592186827)
        self.seqpos = properties.get("seqpos", None)
        self.helpar_name = properties.get("helpar_name", None)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`AverageStiffness <stiffness.average_stiffness.AverageStiffness>` object."""

        # Check the properties
        fu.check_properties(self, self.properties)

        # check sequence
        if self.sequence is None or len(self.sequence) < 2:
            raise ValueError("sequence is null or too short!")

        # get helical parameter from filename if not specified
        if self.helpar_name is None:
            for hp in constants.helical_parameters:
                if hp.lower() in Path(
                        self.io_dict['in']['input_ser_path']).name.lower():
                    self.helpar_name = hp
            if self.helpar_name is None:
                raise ValueError(
                    "Helical parameter name can't be inferred from file, "
                    "so it must be specified!")
        else:
            if self.helpar_name not in constants.helical_parameters:
                raise ValueError(
                    "Helical parameter name is invalid! "
                    f"Options: {constants.helical_parameters}")

        # get base length and unit from helical parameter name
        if self.helpar_name.lower() in ["roll", "tilt", "twist"]:
            self.hp_unit = "kcal/(mol*degree²)"
            scale = 1
        else:
            self.hp_unit = "kcal/(mol*Å²)"
            scale = 10.6

        # check seqpos
        if self.seqpos is not None:
            if (max(self.seqpos) > len(self.sequence) - 2) or (min(self.seqpos) < 1):
                raise ValueError(
                    f"seqpos values must be between 1 and {len(self.sequence) - 2}")
            if not (isinstance(self.seqpos, list) and len(self.seqpos) > 1):
                raise ValueError(
                    "seqpos must be a list of at least two integers")

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir(prefix="avgstiffness_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # Copy input_file_path1 to temporary folder
        shutil.copy(self.io_dict['in']['input_ser_path'], self.tmp_folder)

        # read input .ser file
        ser_data = read_series(
            self.io_dict['in']['input_ser_path'],
            usecols=self.seqpos)
        if self.seqpos is None:
            ser_data = ser_data[ser_data.columns[1:-1]]
            # discard first and last base(pairs) from sequence
            sequence = self.sequence[1:]
            xlabels = [
                f"{sequence[i:i+2]}"
                for i in range(len(ser_data.columns))]
        else:
            sequence = self.sequence
            xlabels = [
                f"{sequence[i:i+2]}"
                for i in self.seqpos]

        # calculate average stiffness
        cov = ser_data.cov()
        stiff = np.linalg.inv(cov) * self.KT
        avg_stiffness = np.diag(stiff) * scale

        # save plot
        fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
        axs.plot(
            range(len(xlabels)),
            avg_stiffness,
            "-o")
        axs.set_xticks(range(len(xlabels)))
        axs.set_xticklabels(xlabels)
        axs.set_xlabel("Sequence Base Pair")
        axs.set_ylabel(f"{self.helpar_name.capitalize()} ({self.hp_unit})")
        axs.set_title(
            "Base Pair Helical Parameter Stiffness: "
            f"{self.helpar_name.capitalize()}")
        fig.savefig(
            self.io_dict['out']['output_jpg_path'],
            format="jpg")

        # save table
        dataset = pd.DataFrame(
            data=avg_stiffness,
            index=xlabels,
            columns=[f"{self.helpar_name}_stiffness"])
        dataset.to_csv(self.io_dict['out']['output_csv_path'])

        plt.close()

        # Remove temporary file(s)
        if self.remove_tmp:
            self.tmp_files.append(self.tmp_folder)
            self.remove_tmp_files()

        return 0


def average_stiffness(
        input_ser_path: str, output_csv_path: str, output_jpg_path: str,
        properties: dict = None, **kwargs) -> int:
    """Create :class:`AverageStiffness <stiffness.average_stiffness.AverageStiffness>` class and
    execute the :meth:`launch() <stiffness.average_stiffness.AverageStiffness.launch>` method."""

    return AverageStiffness(
        input_ser_path=input_ser_path,
        output_csv_path=output_csv_path,
        output_jpg_path=output_jpg_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Calculate average stiffness constants for each base pair of a trajectory\'s series.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_ser_path', required=True,
                               help='Helical parameter input ser file path. Accepted formats: ser.')
    required_args.add_argument('--output_csv_path', required=True,
                               help='Path to output csv file. Accepted formats: csv.')
    required_args.add_argument('--output_jpg_path', required=True,
                               help='Path to output jpg file. Accepted formats: jpg.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    average_stiffness(
        input_ser_path=args.input_ser_path,
        output_csv_path=args.output_csv_path,
        output_jpg_path=args.output_jpg_path,
        properties=properties)


if __name__ == '__main__':
    main()
