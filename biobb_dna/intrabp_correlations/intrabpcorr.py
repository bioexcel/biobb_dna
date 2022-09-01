#!/usr/bin/env python3

"""Module containing the IntraBasePairCorrelation class and the command line interface."""
import argparse
from itertools import product

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_dna.utils.loader import read_series
from biobb_dna.utils import constants


class IntraBasePairCorrelation(BiobbObject):
    """
    | biobb_dna IntraBasePairCorrelation
    | Calculate correlation between all intra-base pairs of a single sequence and for a single helical parameter.

    Args:
        input_filename_shear (str): Path to .ser file with data for helical parameter 'shear'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/canal_output_shear.ser>`_. Accepted formats: ser (edam:format_2330).
        input_filename_stretch (str): Path to .ser file with data for helical parameter 'stretch'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/canal_output_stretch.ser>`_. Accepted formats: ser (edam:format_2330).
        input_filename_stagger (str): Path to .ser file with data for helical parameter 'stagger'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/canal_output_stagger.ser>`_. Accepted formats: ser (edam:format_2330).
        input_filename_buckle (str): Path to .ser file with data for helical parameter 'buckle'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/canal_output_buckle.ser>`_. Accepted formats: ser (edam:format_2330).
        input_filename_propel (str): Path to .ser file with data for helical parameter 'propel'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/canal_output_propel.ser>`_. Accepted formats: ser (edam:format_2330).
        input_filename_opening (str): Path to .ser file with data for helical parameter 'opening'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/correlation/canal_output_opening.ser>`_. Accepted formats: ser (edam:format_2330).
        output_csv_path (str): Path to directory where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/correlation/intra_bpcorr_ref.csv>`_. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/correlation/intra_bpcorr_ref.jpg>`_. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **sequence** (*str*) - (None) Nucleic acid sequence for the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option).
            * **seqpos** (*list*) - (None) list of sequence positions (columns indices starting by 0) to analyze.  If not specified it will analyse the complete sequence.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.intrabp_correlations.intrabpcorr import intrabpcorr

            intrabpcorr(
                input_filename_shear='path/to/input/shear.ser',
                input_filename_stretch='path/to/input/stretch.ser',
                input_filename_stagger='path/to/input/stagger.ser',
                input_filename_buckle='path/to/input/buckle.ser',
                input_filename_propel='path/to/input/propel.ser',
                input_filename_opening='path/to/input/opening.ser',
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
            self, input_filename_shear, input_filename_stretch,
            input_filename_stagger, input_filename_buckle,
            input_filename_propel, input_filename_opening,
            output_csv_path, output_jpg_path,
            properties=None, **kwargs) -> None:
        properties = properties or {}
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_filename_shear': input_filename_shear,
                'input_filename_stretch': input_filename_stretch,
                'input_filename_stagger': input_filename_stagger,
                'input_filename_buckle': input_filename_buckle,
                'input_filename_propel': input_filename_propel,
                'input_filename_opening': input_filename_opening
            },
            'out': {
                'output_csv_path': output_csv_path,
                'output_jpg_path': output_jpg_path
            }
        }

        self.properties = properties
        self.sequence = properties.get("sequence", None)
        self.seqpos = properties.get("seqpos", None)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`HelParCorrelation <intrabp_correlations.intrabpcorr.IntraBasePairCorrelation>` object."""

        # Check the properties
        fu.check_properties(self, self.properties)

        # check sequence
        if self.sequence is None or len(self.sequence) < 2:
            raise ValueError("sequence is null or too short!")

        # check seqpos
        if self.seqpos is not None:
            if not (isinstance(self.seqpos, list) and len(self.seqpos) > 1):
                raise ValueError(
                    "seqpos must be a list of at least two integers")

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir(prefix="bpcorrelation_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # read input
        shear = read_series(
            self.io_dict["in"]["input_filename_shear"], usecols=self.seqpos)
        stretch = read_series(
            self.io_dict["in"]["input_filename_stretch"], usecols=self.seqpos)
        stagger = read_series(
            self.io_dict["in"]["input_filename_stagger"], usecols=self.seqpos)
        buckle = read_series(
            self.io_dict["in"]["input_filename_buckle"], usecols=self.seqpos)
        propel = read_series(
            self.io_dict["in"]["input_filename_propel"], usecols=self.seqpos)
        opening = read_series(
            self.io_dict["in"]["input_filename_opening"], usecols=self.seqpos)

        if self.seqpos is None:
            # drop first and last columns
            shear = shear[shear.columns[1:-1]]
            stretch = stretch[stretch.columns[1:-1]]
            stagger = stagger[stagger.columns[1:-1]]
            buckle = buckle[buckle.columns[1:-1]]
            propel = propel[propel.columns[1:-1]]
            opening = opening[opening.columns[1:-1]]
            labels = [
                f"{i+1}_{self.sequence[i:i+1]}" for i in range(1, len(shear.columns) + 1)]
            corr_index = [
                f"{self.sequence[i:i+2]}" for i in range(1, len(shear.columns) + 1)]
        else:
            labels = [f"{i+1}_{self.sequence[i:i+1]}" for i in self.seqpos]
            corr_index = [f"{self.sequence[i:i+2]}" for i in self.seqpos]

        # rename duplicated subunits
        shear.columns = labels
        stretch.columns = labels
        stagger.columns = labels
        buckle.columns = labels
        propel.columns = labels
        opening.columns = labels

        # set names to each dataset
        shear.name = "shear"
        stretch.name = "stretch"
        stagger.name = "stagger"
        buckle.name = "buckle"
        propel.name = "propel"
        opening.name = "opening"

        # get correlation between neighboring basepairs among all helical parameters
        results = {}
        datasets = [shear, stretch, stagger, buckle, propel, opening]
        for ser1, ser2 in product(datasets, datasets):
            ser2_shifted = ser2.shift(axis=1)
            ser2_shifted[labels[0]] = ser2[labels[-1]]
            if (
                    ser1.name in constants.hp_angular and
                    ser2.name in constants.hp_angular):
                method = self.circular
            elif (
                (
                    ser1.name in constants.hp_angular and not (
                        ser2.name in constants.hp_angular)
                ) or (
                    ser2.name in constants.hp_angular and not (
                        ser1.name in constants.hp_angular)
                )
            ):
                method = self.circlineal
            else:
                method = "pearson"
            corr_data = ser1.corrwith(ser2_shifted, method=method)
            corr_data.index = corr_index
            results[f"{ser1.name}/{ser2.name}"] = corr_data
        result_df = pd.DataFrame.from_dict(results)
        result_df.index = corr_index

        # save csv data
        result_df.to_csv(self.io_dict["out"]["output_csv_path"])

        # create heatmap
        cmap = plt.get_cmap("bwr").copy()
        bounds = [-1, -.8, -.6, -.4, -.2, .2, .4, .6, .8, 1]
        num = cmap.N
        norm = mpl.colors.BoundaryNorm(bounds, num)
        cmap.set_bad(color="gainsboro")
        fig, ax = plt.subplots(
            1,
            1,
            dpi=300,
            figsize=(7.5, 5),
            tight_layout=True)
        im = ax.imshow(result_df, cmap=cmap, norm=norm, aspect='auto')
        plt.colorbar(im, ticks=[-1, -.8, -.6, -.4, -.2, .2, .4, .6, .8, 1])

        # axes
        xlocs = np.arange(len(result_df.columns))
        _ = ax.set_xticks(xlocs)
        _ = ax.set_xticklabels(result_df.columns.to_list(), rotation=90)

        ylocs = np.arange(len(result_df.index))
        _ = ax.set_yticks(ylocs)
        _ = ax.set_yticklabels(result_df.index.to_list())

        ax.set_title(
            "Correlation for neighboring basepairs "
            "and pairs of helical parameters")

        fig.tight_layout()
        fig.savefig(
            self.io_dict['out']['output_jpg_path'],
            format="jpg")
        plt.close()

        # Remove temporary file(s)
        if self.remove_tmp:
            self.tmp_files.append(self.tmp_folder)
            self.remove_tmp_files()

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

    @staticmethod
    def circlineal(x1, x2):
        x2 = x2 * np.pi / 180
        rc = np.corrcoef(x1, np.cos(x2))[1, 0]
        rs = np.corrcoef(x1, np.sin(x2))[1, 0]
        rcs = np.corrcoef(np.sin(x2), np.cos(x2))[1, 0]
        num = (rc ** 2) + (rs ** 2) - 2 * rc * rs * rcs
        den = 1 - (rcs ** 2)
        correlation = np.sqrt(num / den)
        if np.corrcoef(x1, x2)[1, 0] < 0:
            correlation *= -1
        return correlation


def intrabpcorr(
        input_filename_shear: str, input_filename_stretch: str,
        input_filename_stagger: str, input_filename_buckle: str,
        input_filename_propel: str, input_filename_opening: str,
        output_csv_path: str, output_jpg_path: str,
        properties: dict = None, **kwargs) -> int:
    """Create :class:`HelParCorrelation <intrabp_correlations.intrabpcorr.IntraBasePairCorrelation>` class and
    execute the :meth:`launch() <intrabp_correlations.intrabpcorr.IntraBasePairCorrelation.launch>` method."""

    return IntraBasePairCorrelation(
        input_filename_shear=input_filename_shear,
        input_filename_stretch=input_filename_stretch,
        input_filename_stagger=input_filename_stagger,
        input_filename_buckle=input_filename_buckle,
        input_filename_propel=input_filename_propel,
        input_filename_opening=input_filename_opening,
        output_csv_path=output_csv_path,
        output_jpg_path=output_jpg_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Load .ser file from Canal output and calculate correlation between base pairs of the corresponding sequence.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_filename_shear', required=True,
                               help='Path to ser file for helical parameter shear. Accepted formats: ser.')
    required_args.add_argument('--input_filename_stretch', required=True,
                               help='Path to ser file for helical parameter stretch. Accepted formats: ser.')
    required_args.add_argument('--input_filename_stagger', required=True,
                               help='Path to ser file for helical parameter stagger. Accepted formats: ser.')
    required_args.add_argument('--input_filename_buckle', required=True,
                               help='Path to ser file for helical parameter buckle. Accepted formats: ser.')
    required_args.add_argument('--input_filename_propel', required=True,
                               help='Path to ser file for helical parameter propel. Accepted formats: ser.')
    required_args.add_argument('--input_filename_opening', required=True,
                               help='Path to ser file for helical parameter opening. Accepted formats: ser.')
    required_args.add_argument('--output_csv_path', required=True,
                               help='Path to output file. Accepted formats: csv.')
    required_args.add_argument('--output_jpg_path', required=True,
                               help='Path to output plot. Accepted formats: jpg.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    intrabpcorr(
        input_filename_shear=args.input_filename_shear,
        input_filename_stretch=args.input_filename_stretch,
        input_filename_stagger=args.input_filename_stagger,
        input_filename_buckle=args.input_filename_buckle,
        input_filename_propel=args.input_filename_propel,
        input_filename_opening=args.input_filename_opening,
        output_csv_path=args.output_csv_path,
        output_jpg_path=args.output_jpg_path,
        properties=properties)


if __name__ == '__main__':
    main()
