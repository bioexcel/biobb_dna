#!/usr/bin/env python3

"""Module containing the IntraSequenceCorrelation class and the command line interface."""
import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_dna.utils.loader import read_series
from biobb_dna.utils import constants


class IntraSequenceCorrelation():
    """
    | biobb_dna IntraSequenceCorrelation
    | Calculate correlation between all intra-base pairs of a single sequence and for a single helical parameter.

    Args:
        input_ser_path (str): Path to .ser file with data for single helical parameter. File type: input. Accepted formats: ser (edam:format_2330).
        output_csv_path (str): Path to directory where output is saved. File type: output. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **sequence** (*str*) - (None) Nucleic acid sequence for the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option).
            * **helpar_name** (*str*) - (None) helical parameter name to add to plot title.
            * **seqpos** (*list*) - (None) list of sequence positions (columns indices starting by 0) to analyze.  If not specified it will analyse the complete sequence.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.intrabp_correlations.intraseqcorr import intrasequencecorrelation

            intrasequencecorrelation(
                input_ser_path='path/to/input/file.ser',
                output_csv_path='path/to/output/file.csv',
                output_jpg_path='path/to/output/plot.jpg',
                properties=prop)
    Info:
        * wrapped_software:
            * name: In house
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(
            self, input_ser_path, output_csv_path,
            output_jpg_path, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_ser_path': input_ser_path
            },
            'out': {
                'output_csv_path': output_csv_path,
                'output_jpg_path': output_jpg_path
            }
        }

        self.properties = properties
        self.sequence = properties.get("sequence", None)
        self.seqpos = properties.get("seqpos", None)
        self.helpar_name = properties.get("helpar_name", None)

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
        """Execute the :class:`HelParCorrelation <intrabp_correlations.intraseqcorr.IntraSequenceCorrelation>` object."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

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
        if self.helpar_name in constants.hp_angular:
            self.method = "pearson"
        else:
            self.method = self.circular

        # check seqpos
        if self.seqpos is not None:
            if not (isinstance(self.seqpos, list) and len(self.seqpos) > 1):
                raise ValueError(
                    "seqpos must be a list of at least two integers")

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
        self.tmp_folder = fu.create_unique_dir(prefix="bpcorrelation_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # read input .ser file
        ser_data = read_series(
            self.io_dict['in']['input_ser_path'],
            usecols=self.seqpos)
        if self.seqpos is None:
            ser_data = ser_data[ser_data.columns[1:-1]]
            # discard first and last base(pairs) from strands
            sequence = self.sequence[1:]
            labels = [
                f"{sequence[i:i+1]}" for i in range(len(ser_data.columns))]
        else:
            labels = [f"{self.sequence[i:i+1]}" for i in self.seqpos]
        ser_data.columns = labels

        # rename duplicated subunits
        while any(ser_data.columns.duplicated()):
            ser_data.columns = [
                name if not duplicated else name + "_dup"
                for duplicated, name
                in zip(ser_data.columns.duplicated(), ser_data.columns)]

        # make matrix
        corr_data = ser_data.corr(method=self.method)

        # save csv data
        corr_data.to_csv(self.io_dict["out"]["output_csv_path"])

        # create heatmap
        fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
        axs.pcolor(corr_data)
        # Loop over data dimensions and create text annotations.
        for i in range(len(corr_data)):
            for j in range(len(corr_data)):
                axs.text(
                    j+.5,
                    i+.5,
                    f"{corr_data[corr_data.columns[j]].iloc[i]:.2f}",
                    ha="center",
                    va="center",
                    color="w")
        axs.set_xticks([i + 0.5 for i in range(len(corr_data))])
        axs.set_xticklabels(labels, rotation=90)
        axs.set_yticks([i + 0.5 for i in range(len(corr_data))])
        axs.set_yticklabels(labels)
        axs.set_title(
            "Base Pair Correlation "
            f"for Helical Parameter \'{self.helpar_name}\'")
        fig.tight_layout()
        fig.savefig(
            self.io_dict['out']['output_jpg_path'],
            format="jpg")
        plt.close()

        # Remove temporary file(s)
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)

        return 0

    @staticmethod
    def circular(x1, x2):
        x1 = x1 * np.pi / 180
        x2 = x2 * np.pi / 180
        diff_1 = np.sin(x1 - x1.mean())
        diff_2 = np.sin(x2 - x2.mean())
        num = (diff_1 * diff_2).sum()
        den = np.sqrt((diff_1 ** 2).sum() * (diff_2 ** 2).sum())
        return num / den


def intrasequencecorrelation(
        input_ser_path: str,
        output_csv_path: str, output_jpg_path: str,
        properties: dict = None, **kwargs) -> int:
    """Create :class:`HelParCorrelation <intrabp_correlations.intraseqcorr.IntraSequenceCorrelation>` class and
    execute the :meth:`launch() <intrabp_correlations.intraseqcorr.IntraSequenceCorrelation.launch>` method."""

    return IntraSequenceCorrelation(
        input_ser_path=input_ser_path,
        output_csv_path=output_csv_path,
        output_jpg_path=output_jpg_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Load .ser file from Canal output and calculate correlation between base pairs of the corresponding sequence.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_ser_path', required=True,
                               help='Path to ser file with inputs. Accepted formats: ser.')
    required_args.add_argument('--output_csv_path', required=True,
                               help='Path to output file. Accepted formats: csv.')
    required_args.add_argument('--output_jpg_path', required=True,
                               help='Path to output plot. Accepted formats: jpg.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    intrasequencecorrelation(
        input_ser_path=args.input_ser_path,
        output_csv_path=args.output_csv_path,
        output_jpg_path=args.output_jpg_path,
        properties=properties)


if __name__ == '__main__':
    main()
