#!/usr/bin/env python3
"""Module containing the CanonicalAG class and the command line interface."""

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


class CanonicalAG(BiobbObject):
    """
    | biobb_dna CanonicalAG
    | Calculate Canonical Alpha/Gamma populations from alpha and gamma parameters.

    Args:
        input_alphaC_path (str): Path to .ser file for helical parameter 'alphaC'. File type: input. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/backbone/canal_output_alphaC.ser>`_. Accepted formats: ser (edam:format_2330).
        input_alphaW_path (str): Path to .ser file for helical parameter 'alphaW'. File type: input. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/backbone/canal_output_alphaW.ser>`_. Accepted formats: ser (edam:format_2330).
        input_gammaC_path (str): Path to .ser file for helical parameter 'gammaC'. File type: input. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/backbone/canal_output_gammaC.ser>`_. Accepted formats: ser (edam:format_2330).
        input_gammaW_path (str): Path to .ser file for helical parameter 'gammaW'. File type: input. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/backbone/canal_output_gammaW.ser>`_. Accepted formats: ser (edam:format_2330).
        output_csv_path (str): Path to .csv file where output is saved. File type: output. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/backbone/canonag_ref.csv>`_. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/backbone/canonag_ref.jpg>`_. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **sequence** (*str*) - (None) Nucleic acid sequence corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option).
            * **seqpos** (*list*) - (None) list of sequence positions (columns indices starting by 0) to analyze.  If not specified it will analyse the complete sequence.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.backbone.canonicalag import canonicalag

            prop = {
                'helpar_name': 'twist',
                'seqpos': [1,2],
                'sequence': 'GCAT',
            }
            canonicalag(
                input_alphaC_path='/path/to/alphaC.ser',
                input_alphaW_path='/path/to/alphaW.ser',
                input_gammaC_path='/path/to/gammaC.ser',
                input_gammaW_path='/path/to/gammaW.ser',
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

    def __init__(self, input_alphaC_path, input_alphaW_path,
                 input_gammaC_path, input_gammaW_path,
                 output_csv_path, output_jpg_path,
                 properties=None, **kwargs) -> None:
        properties = properties or {}
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_alphaC_path': input_alphaC_path,
                'input_alphaW_path': input_alphaW_path,
                'input_gammaC_path': input_gammaC_path,
                'input_gammaW_path': input_gammaW_path
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
        """Execute the :class:`CanonicalAG <backbone.canonicalag.CanonicalAG>` object."""

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
        shutil.copy(self.io_dict['in']['input_alphaC_path'], self.tmp_folder)
        shutil.copy(self.io_dict['in']['input_alphaW_path'], self.tmp_folder)
        shutil.copy(self.io_dict['in']['input_gammaC_path'], self.tmp_folder)
        shutil.copy(self.io_dict['in']['input_gammaW_path'], self.tmp_folder)

        # read input files
        alphaC = read_series(
            self.io_dict['in']['input_alphaC_path'], usecols=self.seqpos)
        alphaW = read_series(
            self.io_dict['in']['input_alphaW_path'], usecols=self.seqpos)
        gammaC = read_series(
            self.io_dict['in']['input_gammaC_path'], usecols=self.seqpos)
        gammaW = read_series(
            self.io_dict['in']['input_gammaW_path'], usecols=self.seqpos)

        # fix angle range so its not negative
        alphaC = self.fix_angles(alphaC)
        alphaW = self.fix_angles(alphaW)
        gammaC = self.fix_angles(gammaC)
        gammaW = self.fix_angles(gammaW)

        # calculate difference between epsil and zeta parameters
        xlabels = self.get_xlabels(
            self.sequence,
            inverse_complement(self.sequence))
        canonical_populations = self.check_alpha_gamma(
            alphaC,
            gammaC,
            alphaW,
            gammaW)

        # save table
        canonical_populations.name = "Canonical alpha/gamma"
        ag_populations_df = pd.DataFrame({
            "Nucleotide": xlabels,
            "Canonical alpha/gamma": canonical_populations})
        ag_populations_df.to_csv(
            self.io_dict['out']['output_csv_path'],
            index=False)

        # save plot
        fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
        axs.bar(
            range(len(xlabels)),
            canonical_populations,
            label="canonical alpha/gamma")
        axs.bar(
            range(len(xlabels)),
            100 - canonical_populations,
            bottom=canonical_populations,
            label=None)
        # empty bar to divide both sequences
        axs.bar(
            [len(alphaC.columns)],
            [100],
            color='white',
            label=None)
        axs.legend()
        axs.set_xticks(range(len(xlabels)))
        axs.set_xticklabels(xlabels, rotation=90)
        axs.set_xlabel("Nucleotide Sequence")
        axs.set_ylabel("Canonical Alpha-Gamma (%)")
        axs.set_title("Nucleotide parameter: Canonical Alpha-Gamma")
        fig.savefig(
            self.io_dict['out']['output_jpg_path'],
            format="jpg")
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

    def check_alpha_gamma(self, alphaC, gammaC, alphaW, gammaW):
        separator_df = pd.DataFrame({"-": np.nan}, index=range(len(gammaW)))
        gamma = pd.concat([
            gammaW,
            separator_df,
            gammaC[gammaC.columns[::-1]]],
            axis=1)
        alpha = pd.concat([
            alphaW,
            separator_df,
            alphaC[alphaC.columns[::-1]]],
            axis=1)

        alpha_filter = np.logical_and(alpha > 240, alpha < 360)
        gamma_filter = np.logical_and(gamma > 0, gamma < 120)
        canonical_alpha_gamma = np.logical_and(
            alpha_filter, gamma_filter).mean() * 100

        return canonical_alpha_gamma

    def fix_angles(self, dataset):
        values = np.where(dataset < 0, dataset + 360, dataset)
        values = np.where(values > 360, values - 360, values)
        dataset = pd.DataFrame(values)
        return dataset


def canonicalag(
        input_alphaC_path: str, input_alphaW_path: str,
        input_gammaC_path: str, input_gammaW_path: str,
        output_csv_path: str, output_jpg_path: str,
        properties: dict = None, **kwargs) -> int:
    """Create :class:`CanonicalAG <dna.backbone.canonicalag.CanonicalAG>` class and
    execute the: meth: `launch() <dna.backbone.canonicalag.CanonicalAG.launch>` method. """

    return CanonicalAG(
        input_alphaC_path=input_alphaC_path,
        input_alphaW_path=input_alphaW_path,
        input_gammaC_path=input_gammaC_path,
        input_gammaW_path=input_gammaW_path,
        output_csv_path=output_csv_path,
        output_jpg_path=output_jpg_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Calculate Canonical Alpha/Gamma distributions.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_alphaC_path', required=True,
                               help='Helical parameter <alphaC> input ser file path. Accepted formats: ser.')
    required_args.add_argument('--input_alphaW_path', required=True,
                               help='Helical parameter <alphaW> input ser file path. Accepted formats: ser.')
    required_args.add_argument('--input_gammaC_path', required=True,
                               help='Helical parameter <gammaC> input ser file path. Accepted formats: ser.')
    required_args.add_argument('--input_gammaW_path', required=True,
                               help='Helical parameter <gammaW> input ser file path. Accepted formats: ser.')
    required_args.add_argument('--output_csv_path', required=True,
                               help='Path to output csv file. Accepted formats: csv.')
    required_args.add_argument('--output_jpg_path', required=True,
                               help='Path to output jpg file. Accepted formats: jpg.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    canonicalag(
        input_alphaC_path=args.input_alphaC_path,
        input_alphaW_path=args.input_alphaW_path,
        input_gammaC_path=args.input_gammaC_path,
        input_gammaW_path=args.input_gammaW_path,
        output_csv_path=args.output_csv_path,
        output_jpg_path=args.output_jpg_path,
        properties=properties)


if __name__ == '__main__':
    main()
