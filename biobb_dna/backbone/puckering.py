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


"""Module containing the Puckering class and the command line interface."""


class Puckering():
    """
    | biobb_dna Puckering
    | Calculate Puckering from phase parameters.

    Args:
        input_phaseC_path (str): Path to .ser file for helical parameter 'phaseC'. File type: input. Accepted formats: ser
        input_phaseW_path (str): Path to .ser file for helical parameter 'phaseW'. File type: input. Accepted formats: ser
        output_csv_path (str): Path to .csv file where output is saved. File type: output. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **strand1** (*str*) - Nucleic acid sequence for the first strand corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *usecols* option).
            * **strand2** (*str*) - Nucleic acid sequence for the second strand corresponding to the input .ser file.
            * **helpar_name** (*str*) - (Optional) helical parameter name.
            * **stride** (*int*) - (1000) granularity of the number of snapshots for plotting time series.
            * **usecols** (*list*) - (None) list of column indices to use.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.backbone.puckering import Puckering

            prop = {
                'strand1': 'GCAT',
                'strand2': 'ATGC'
            }
            Puckering(
                input_phaseC_path='/path/to/phaseC.ser',
                input_phaseW_path='/path/to/phaseW.ser',
                output_csv_path='/path/to/table/output.csv',
                output_jpg_path='/path/to/table/output.jpg',
                properties=prop)

        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_phaseC_path, input_phaseW_path,
                 output_csv_path, output_jpg_path,
                 properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_phaseC_path': input_phaseC_path,
                'input_phaseW_path': input_phaseW_path
            },
            'out': {
                'output_csv_path': output_csv_path,
                'output_jpg_path': output_jpg_path
            }
        }

        self.properties = properties
        self.strand1 = properties.get("strand1")
        self.strand2 = properties.get("strand2")
        self.stride = properties.get(
            "stride", 1000)
        self.usecols = properties.get(
            "usecols", None)

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
        """Execute the :class:`Puckering <backbone.puckering.Puckering>` object."""

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

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir(prefix="backbone_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # Copy input_file_path1 to temporary folder
        shutil.copy(self.io_dict['in']['input_phaseC_path'], self.tmp_folder)
        shutil.copy(self.io_dict['in']['input_phaseW_path'], self.tmp_folder)

        # read input files
        phaseC = read_series(self.io_dict['in']['input_phaseC_path'])
        phaseW = read_series(self.io_dict['in']['input_phaseW_path'])

        # fix angle range so its not negative
        phaseC = self.fix_angles(phaseC)
        phaseW = self.fix_angles(phaseW)

        # calculate difference between epsil and zeta parameters
        Npop, Epop, Wpop, Spop, xlabels = self.check_puckering(
            self.strand1, self.strand2, phaseC, phaseW)

        # save plot
        fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
        axs.bar(
            range(len(xlabels)),
            Npop,
            label="North")
        axs.bar(
            range(len(xlabels)),
            Epop,
            bottom=Npop,
            label="East")
        axs.bar(
            range(len(xlabels)),
            Spop,
            bottom=Npop+Epop,
            label="South")
        axs.bar(
            range(len(xlabels)),
            Wpop,
            bottom=Npop+Epop+Spop,
            label="West")
        # empty bar to divide both sequences
        axs.bar(
            [len(self.strand1)],
            [100],
            color='white',
            label=None)
        axs.legend()
        axs.set_xticks(range(len(xlabels)))
        axs.set_xticklabels(xlabels, rotation=90)
        axs.set_xlabel("Nucleotide Sequence")
        axs.set_ylabel("Puckering (%)")
        axs.set_title("Nucleotide parameter: Puckering")
        fig.savefig(
            self.io_dict['out']['output_jpg_path'],
            format="jpg")

        # save table
        populations = pd.DataFrame({
            "Nucleotide": xlabels,
            "North": Npop,
            "East": Epop,
            "West": Wpop,
            "South": Spop})
        populations.to_csv(
            self.io_dict['out']['output_csv_path'],
            index=False)

        plt.close()

        # Remove temporary file(s)
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)

        return 0

    def check_puckering(self, strand1, strand2, phaseC, phaseW):
        # get list of tetramers, except first and last two bases
        labelsW = list(strand1)
        labelsW[0] = f"{labelsW[0]}5\'"
        labelsW[-1] = f"{labelsW[-1]}3\'"
        labelsW = [
            f"{i}-{j}" for i, j in zip(labelsW, range(1, len(labelsW)+1))]
        labelsC = list(strand2)[::-1]
        labelsC[0] = f"{labelsC[0]}5\'"
        labelsC[-1] = f"{labelsC[-1]}3\'"
        labelsC = [
            f"{i}-{j}" for i, j in zip(labelsC, range(len(labelsC), 0, -1))]
        xlabels = labelsW + ['-'] + labelsC

        separator_df = pd.DataFrame({"-": np.nan}, index=range(1, len(phaseC)))
        phase = pd.concat([
            phaseW,
            separator_df,
            phaseC[phaseC.columns[::-1]]],
            axis=1)
        # phase.columns = columns

        Npop = np.logical_or(phase > 315, phase < 45).mean() * 100
        Epop = np.logical_and(phase > 45, phase < 135).mean() * 100
        Wpop = np.logical_and(phase > 225, phase < 315).mean() * 100
        Spop = np.logical_and(phase > 135, phase < 225).mean() * 100
        return Npop, Epop, Wpop, Spop, xlabels

    def fix_angles(self, dataset):
        values = np.where(dataset < 0, dataset + 360, dataset)
        # values = np.where(values > 360, values - 360, values)
        dataset = pd.DataFrame(values)
        return dataset


def puckering(
        input_phaseC_path: str, input_phaseW_path: str,
        output_csv_path: str, output_jpg_path: str,
        properties: dict = None, **kwargs) -> int:
    """Create :class:`Puckering <dna.backbone.puckering.Puckering>` class and
    execute the: meth: `launch() <dna.backbone.puckering.Puckering.launch>` method. """

    return Puckering(
        input_phaseC_path=input_phaseC_path,
        input_phaseW_path=input_phaseW_path,
        output_csv_path=output_csv_path,
        output_jpg_path=output_jpg_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Calculate North/East/West/South distribution of sugar puckering backbone torsions.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_phaseC_path', required=True,
                               help='Helical parameter <alphaC> input ser file path. Accepted formats: ser.')
    required_args.add_argument('--input_phaseW_path', required=True,
                               help='Helical parameter <alphaW> input ser file path. Accepted formats: ser.')
    required_args.add_argument('--output_csv_path', required=True,
                               help='Path to output csv file. Accepted formats: csv.')
    required_args.add_argument('--output_jpg_path', required=True,
                               help='Path to output jpg file. Accepted formats: jpg.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    puckering(
        input_phaseC_path=args.input_phaseC_path,
        input_phaseW_path=args.input_phaseW_path,
        output_csv_path=args.output_csv_path,
        output_jpg_path=args.output_jpg_path,
        properties=properties)


if __name__ == '__main__':
    main()