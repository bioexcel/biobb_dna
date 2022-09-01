#!/usr/bin/env python3
"""Module containing the Puckering class and the command line interface."""

import shutil
import argparse

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from biobb_dna.utils.loader import read_series
from biobb_dna.utils.transform import inverse_complement
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger
from biobb_common.tools import file_utils as fu
from biobb_common.configuration import settings


class Puckering(BiobbObject):
    """
    | biobb_dna Puckering
    | Calculate Puckering from phase parameters.

    Args:
        input_phaseC_path (str): Path to .ser file for helical parameter 'phaseC'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/backbone/canal_output_phaseC.ser>`_. Accepted formats: ser (edam:format_2330).
        input_phaseW_path (str): Path to .ser file for helical parameter 'phaseW'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/backbone/canal_output_phaseW.ser>`_. Accepted formats: ser (edam:format_2330).
        output_csv_path (str): Path to .csv file where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/backbone/puckering_ref.csv>`_. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/backbone/puckering_ref.jpg>`_. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **sequence** (*str*) - (None) Nucleic acid sequence corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option).
            * **helpar_name** (*str*) - (None) helical parameter name.
            * **stride** (*int*) - (1000) granularity of the number of snapshots for plotting time series.
            * **seqpos** (*list*) - (None) list of sequence positions (columns indices starting by 0) to analyze.  If not specified it will analyse the complete sequence.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.backbone.puckering import puckering

            prop = {
                'sequence': 'GCAT',
            }
            puckering(
                input_phaseC_path='/path/to/phaseC.ser',
                input_phaseW_path='/path/to/phaseW.ser',
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

    def __init__(self, input_phaseC_path, input_phaseW_path,
                 output_csv_path, output_jpg_path,
                 properties=None, **kwargs) -> None:
        properties = properties or {}
        super().__init__(properties)

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
        self.sequence = properties.get("sequence")
        self.stride = properties.get(
            "stride", 1000)
        self.seqpos = properties.get(
            "seqpos", None)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Puckering <backbone.puckering.Puckering>` object."""

        # Check the properties
        fu.check_properties(self, self.properties)

        # check sequence
        if self.sequence is None or len(self.sequence) < 2:
            raise ValueError("sequence is null or too short!")

        # check seqpos
        if self.seqpos is not None:
            if (max(self.seqpos) > len(self.sequence) - 2) or (min(self.seqpos) < 1):
                raise ValueError(
                    f"seqpos values must be between 1 and {len(self.sequence) - 2}")
            if not (isinstance(self.seqpos, list) and len(self.seqpos) > 1):
                raise ValueError(
                    "seqpos must be a list of at least two integers")

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir(prefix="backbone_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # Copy input_file_path1 to temporary folder
        shutil.copy(self.io_dict['in']['input_phaseC_path'], self.tmp_folder)
        shutil.copy(self.io_dict['in']['input_phaseW_path'], self.tmp_folder)

        # read input files
        phaseC = read_series(
            self.io_dict['in']['input_phaseC_path'],
            usecols=self.seqpos)
        phaseW = read_series(
            self.io_dict['in']['input_phaseW_path'],
            usecols=self.seqpos)

        # fix angle range so its not negative
        phaseC = self.fix_angles(phaseC)
        phaseW = self.fix_angles(phaseW)

        # calculate difference between epsil and zeta parameters
        xlabels = self.get_xlabels(
            self.sequence,
            inverse_complement(self.sequence))
        Npop, Epop, Wpop, Spop = self.check_puckering(phaseC, phaseW)

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
            [len(phaseC.columns)],
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
            self.tmp_files.append(self.tmp_folder)
            self.remove_tmp_files()

        return 0

    def get_xlabels(self, strand1, strand2):
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

        if self.seqpos is not None:
            labelsC = [labelsC[i] for i in self.seqpos]
            labelsW = [labelsW[i] for i in self.seqpos]
        xlabels = labelsW + ['-'] + labelsC
        return xlabels

    def check_puckering(self, phaseC, phaseW):
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
        return Npop, Epop, Wpop, Spop

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
