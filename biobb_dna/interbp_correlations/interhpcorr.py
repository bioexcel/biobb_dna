#!/usr/bin/env python3

"""Module containing the InterHelParCorrelation class and the command line interface."""
import argparse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_dna.utils.loader import load_data


class InterHelParCorrelation(BiobbObject):
    """
    | biobb_dna InterHelParCorrelation
    | Calculate correlation between helical parameters for a single inter-base pair.

    Args:
        input_filename_shift (str): Path to .csv file with data for helical parameter 'shift'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_shift_AA.csv>`_. Accepted formats: csv (edam:format_3752).
        input_filename_slide (str): Path to .csv file with data for helical parameter 'slide'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_slide_AA.csv>`_. Accepted formats: csv (edam:format_3752).
        input_filename_rise (str): Path to .csv file with data for helical parameter 'rise'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_rise_AA.csv>`_. Accepted formats: csv (edam:format_3752).
        input_filename_tilt (str): Path to .csv file with data for helical parameter 'tilt'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_tilt_AA.csv>`_. Accepted formats: csv (edam:format_3752).
        input_filename_roll (str): Path to .csv file with data for helical parameter 'roll'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_roll_AA.csv>`_. Accepted formats: csv (edam:format_3752).
        input_filename_twist (str): Path to .csv file with data for helical parameter 'twist'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_twist_AA.csv>`_. Accepted formats: csv (edam:format_3752).
        output_csv_path (str): Path to directory where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/correlation/inter_hpcorr_ref.csv>`_. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/correlation/inter_hpcorr_ref.jpg>`_. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **basepair** (*str*) - (None) Name of basepair analyzed.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.interbp_correlations.interhpcorr import interhpcorr

            prop = { 
                'basepair': 'AA',
            }
            interhpcorr(
                input_filename_shift='path/to/shift.csv',
                input_filename_slide='path/to/slide.csv',
                input_filename_rise='path/to/rise.csv',
                input_filename_tilt='path/to/tilt.csv',
                input_filename_roll='path/to/roll.csv',
                input_filename_twist='path/to/twist.csv',
                output_csv_path='path/to/output/file.csv',
                output_jpg_path='path/to/output/file.jpg',
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
            self, input_filename_shift, input_filename_slide,
            input_filename_rise, input_filename_tilt,
            input_filename_roll, input_filename_twist,
            output_csv_path, output_jpg_path,
            properties=None, **kwargs) -> None:
        properties = properties or {}
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_filename_shift': input_filename_shift,
                'input_filename_slide': input_filename_slide,
                'input_filename_rise': input_filename_rise,
                'input_filename_tilt': input_filename_tilt,
                'input_filename_roll': input_filename_roll,
                'input_filename_twist': input_filename_twist
            },
            'out': {
                'output_csv_path': output_csv_path,
                'output_jpg_path': output_jpg_path
            }
        }

        self.properties = properties
        self.basepair = properties.get("basepair", None)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`InterHelParCorrelation <interbp_correlations.interhpcorr.InterHelParCorrelation>` object."""

        # Check the properties
        fu.check_properties(self, self.properties)

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir(prefix="hpcorrelation_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # read input
        shift = load_data(self.io_dict["in"]["input_filename_shift"])
        slide = load_data(self.io_dict["in"]["input_filename_slide"])
        rise = load_data(self.io_dict["in"]["input_filename_rise"])
        tilt = load_data(self.io_dict["in"]["input_filename_tilt"])
        roll = load_data(self.io_dict["in"]["input_filename_roll"])
        twist = load_data(self.io_dict["in"]["input_filename_twist"])

        # get basepair
        if self.basepair is None:
            self.basepair = shift.columns[0]

        # make matrix
        coordinates = ["shift", "slide", "rise", "tilt", "roll", "twist"]
        corr_matrix = pd.DataFrame(
            np.eye(6, 6), index=coordinates, columns=coordinates)

        # shift
        corr_matrix["shift"]["slide"] = shift.corrwith(slide, method="pearson")
        corr_matrix["shift"]["rise"] = shift.corrwith(rise, method="pearson")
        corr_matrix["shift"]["tilt"] = shift.corrwith(
            tilt, method=self.circlineal)
        corr_matrix["shift"]["roll"] = shift.corrwith(
            roll, method=self.circlineal)
        corr_matrix["shift"]["twist"] = shift.corrwith(
            twist, method=self.circlineal)
        # symmetric values
        corr_matrix["slide"]["shift"] = corr_matrix["shift"]["slide"]
        corr_matrix["rise"]["shift"] = corr_matrix["shift"]["rise"]
        corr_matrix["tilt"]["shift"] = corr_matrix["shift"]["tilt"]
        corr_matrix["roll"]["shift"] = corr_matrix["shift"]["roll"]
        corr_matrix["twist"]["shift"] = corr_matrix["shift"]["twist"]

        # slide
        corr_matrix["slide"]["rise"] = slide.corrwith(rise, method="pearson")
        corr_matrix["slide"]["tilt"] = slide.corrwith(
            tilt, method=self.circlineal)
        corr_matrix["slide"]["roll"] = slide.corrwith(
            roll, method=self.circlineal)
        corr_matrix["slide"]["twist"] = slide.corrwith(
            twist, method=self.circlineal)
        # symmetric values
        corr_matrix["rise"]["slide"] = corr_matrix["slide"]["rise"]
        corr_matrix["tilt"]["slide"] = corr_matrix["slide"]["tilt"]
        corr_matrix["roll"]["slide"] = corr_matrix["slide"]["roll"]
        corr_matrix["twist"]["slide"] = corr_matrix["slide"]["twist"]

        # rise
        corr_matrix["rise"]["tilt"] = rise.corrwith(
            tilt, method=self.circlineal)
        corr_matrix["rise"]["roll"] = rise.corrwith(
            roll, method=self.circlineal)
        corr_matrix["rise"]["twist"] = rise.corrwith(
            twist, method=self.circlineal)
        # symmetric values
        corr_matrix["tilt"]["rise"] = corr_matrix["rise"]["tilt"]
        corr_matrix["roll"]["rise"] = corr_matrix["rise"]["roll"]
        corr_matrix["twist"]["rise"] = corr_matrix["rise"]["twist"]

        # tilt
        corr_matrix["tilt"]["roll"] = tilt.corrwith(roll, method=self.circular)
        corr_matrix["tilt"]["twist"] = tilt.corrwith(
            twist, method=self.circular)
        # symmetric values
        corr_matrix["roll"]["tilt"] = corr_matrix["tilt"]["roll"]
        corr_matrix["twist"]["tilt"] = corr_matrix["tilt"]["twist"]

        # roll
        corr_matrix["roll"]["twist"] = roll.corrwith(
            twist, method=self.circular)
        # symmetric values
        corr_matrix["twist"]["roll"] = corr_matrix["roll"]["twist"]

        # save csv data
        corr_matrix.to_csv(self.io_dict["out"]["output_csv_path"])

        # create heatmap
        fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
        axs.pcolor(corr_matrix)
        # Loop over data dimensions and create text annotations.
        for i in range(len(corr_matrix)):
            for j in range(len(corr_matrix)):
                axs.text(
                    j+.5,
                    i+.5,
                    f"{corr_matrix[coordinates[j]].loc[coordinates[i]]:.2f}",
                    ha="center",
                    va="center",
                    color="w")
        axs.set_xticks([i + 0.5 for i in range(len(corr_matrix))])
        axs.set_xticklabels(corr_matrix.columns, rotation=90)
        axs.set_yticks([i+0.5 for i in range(len(corr_matrix))])
        axs.set_yticklabels(corr_matrix.index)
        axs.set_title(
            "Helical Parameter Correlation "
            f"for Base Pair Step \'{self.basepair}\'")
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

    def get_corr_method(self, corrtype1, corrtype2):
        if corrtype1 == "circular" and corrtype2 == "linear":
            method = self.circlineal
        if corrtype1 == "linear" and corrtype2 == "circular":
            method = self.circlineal
        elif corrtype1 == "circular" and corrtype2 == "circular":
            method = self.circular
        else:
            method = "pearson"
        return method

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


def interhpcorr(
        input_filename_shift: str, input_filename_slide: str,
        input_filename_rise: str, input_filename_tilt: str,
        input_filename_roll: str, input_filename_twist: str,
        output_csv_path: str, output_jpg_path: str,
        properties: dict = None, **kwargs) -> int:
    """Create :class:`InterHelParCorrelation <interbp_correlations.interhpcorr.InterHelParCorrelation>` class and
    execute the :meth:`launch() <interbp_correlations.interhpcorr.InterHelParCorrelation.launch>` method."""

    return InterHelParCorrelation(
        input_filename_shift=input_filename_shift,
        input_filename_slide=input_filename_slide,
        input_filename_rise=input_filename_rise,
        input_filename_tilt=input_filename_tilt,
        input_filename_roll=input_filename_roll,
        input_filename_twist=input_filename_twist,
        output_csv_path=output_csv_path,
        output_jpg_path=output_jpg_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Load helical parameter file and save base data individually.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_filename_shift', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_slide', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_rise', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_tilt', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_roll', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_twist', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--output_csv_path', required=True,
                               help='Path to output file. Accepted formats: csv.')
    required_args.add_argument('--output_jpg_path', required=True,
                               help='Path to output file. Accepted formats: csv.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    interhpcorr(
        input_filename_shift=args.input_filename_shift,
        input_filename_slide=args.input_filename_slide,
        input_filename_rise=args.input_filename_rise,
        input_filename_tilt=args.input_filename_tilt,
        input_filename_roll=args.input_filename_roll,
        input_filename_twist=args.input_filename_twist,
        output_csv_path=args.output_csv_path,
        output_jpg_path=args.output_jpg_path,
        properties=properties)


if __name__ == '__main__':
    main()
