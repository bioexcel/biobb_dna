# !/usr/bin/env python3
import shutil
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from biobb_dna.dna import constants
from biobb_dna.dna.loader import read_series
from biobb_common.tools.file_utils import launchlogger
from biobb_common.tools import file_utils as fu
from biobb_common.configuration import settings


"""Module containing the AverageStiffness class and the command line interface."""


class AverageStiffness():
    """
    | biobb_dna AverageStiffness
    | Calculate average stiffness constants for each base pair of a trajectory's series.

    Args:        
        input_ser_path (str): Path to .ser file for helical parameter. File is expected to be a table, with the first column being an index and the rest the helical parameter values for each base/basepair. File type: input. Accepted formats: ser
        output_csv_path (str): Path to .csv file where output is saved. File type: output. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **KT** (*float*) - (0.592186827) Value of Boltzmann temperature factor.
            * **strand1** (*str*) - Nucleic acid sequence for the first strand corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *usecols* option).
            * **strand2** (*str*) - Nucleic acid sequence for the second strand corresponding to the input .ser file.
            * **helpar_name** (*str*) - (Optional) helical parameter name.
            * **seqpos** (*list[int]*) - (Optional) list of sequence positions to analyze. If not specified it will analyse the complete sequence.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.dna.average_stiffness import AverageStiffness

            prop = { 
                'helpar_name': 'twist',
                'strand1': 'GCAT',
                'strand2': 'ATGC'
            }
            averagestiffness(
                input_ser_path='/path/to/twist.ser',
                output_csv_path='/path/to/table/output.csv',
                output_jpg_path='/path/to/table/output.jpg',
                properties=prop)

        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_ser_path, output_csv_path, output_jpg_path,
                 properties=None, **kwargs) -> None:
        properties = properties or {}

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
        self.strand1 = properties.get("strand1")
        self.strand2 = properties.get("strand2")
        self.KT = properties.get(
            "KT", 0.592186827)
        self.seqpos = properties.get("seqpos", None)
        helpar_name = properties.get("helpar_name", None)

        self.helpar_name = helpar_name
        # get helical parameter from filename if not specified
        if self.helpar_name is None:
            for hp in constants.helical_parameters:
                if hp.lower() in Path(input_ser_path).name.lower():
                    self.helpar_name = hp
            if self.helpar_name is None:
                raise ValueError(
                    "Helical parameter name can't be inferred from file, "
                    "so it must be specified!")

            # get base length and unit from helical parameter name
            if self.helpar_name in ["roll", "tilt", "twist"]:
                self.hp_unit = "kcal/(mol*degree²)"
                self.scale = 1
            else:
                self.hp_unit = "kcal/(mol*Å²)"
                self.scale = 10.6

        # Properties common in all BB
        self.can_write_console_log = properties.get(
            'can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`AverageStiffness <dna.average_stiffness.AverageStiffness>` object."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Check the properties
        fu.check_properties(self, self.properties)

        # Restart
        if self.restart:
            output_file_list = [
                self.io_dict['out']['output_csv_path'],
                self.io_dict['out']['output_jpg_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' %
                       self.step, out_log, self.global_log)
                return 0

        # check seqpos property
        if (
                not isinstance(self.seqpos, list) or
                not all([isinstance(i, int) for i in self.seqpos])):
            raise ValueError("`seqpos` must be a list of integers!")

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir(prefix="avgstiffness_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # Copy input_file_path1 to temporary folder
        shutil.copy(self.io_dict['in']['input_ser_path'], self.tmp_folder)

        # read input .ser file
        ser_data = read_series(
            self.io_dict['in']['input_ser_path'],
            usecols=self.seqpos)
        if self.seqpos is None:
            ser_data = ser_data[ser_data.columns[1:-2]]
            # discard first and last base(pairs) from strands
            strand1 = self.strand1[1:]
            strand2 = self.strand2[::-1][1:]
            xlabels = [
                f"{strand1[i:i+2]}{strand2[i:i+2][::-1]}"
                for i in range(len(ser_data.columns))]
        else:
            strand1 = self.strand1
            strand2 = self.strand2[::-1]
            xlabels = [
                f"{strand1[i:i+2]}{strand2[i:i+2][::-1]}"
                for i in self.seqpos]

        # calculate average stiffness
        cov = ser_data.cov()
        stiff = np.linalg.inv(cov) * self.KT
        avg_stiffness = np.diag(stiff) * self.scale

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
            fu.rm(self.tmp_folder)
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)

        return 0


def averagestiffness(
        input_ser_path: str, output_csv_path: str, output_jpg_path: str,
        properties: dict = None, **kwargs) -> int:
    """Create :class:`AverageStiffness <dna.average_stiffness.AverageStiffness>` class and
    execute the :meth:`launch() <dna.average_stiffness.AverageStiffness.launch>` method."""

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

    averagestiffness(
        input_ser_path=args.input_ser_path,
        output_csv_path=args.output_csv_path,
        output_jpg_path=args.output_jpg_path,
        properties=properties)


if __name__ == '__main__':
    main()
