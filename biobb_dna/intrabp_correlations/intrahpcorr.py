#!/usr/bin/env python3

"""Module containing the IntraHelParCorrelation class and the command line interface."""
import argparse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_dna.utils.loader import load_data


class IntraHelParCorrelation():
    """
    | biobb_dna IntraHelParCorrelation
    | Calculate correlation between helical parameters for a single intra-base pair.

    Args:
        input_filename_shear (str): Path to .csv file with data for helical parameter 'shear'. File type: input. Accepted formats: csv (edam:format_3752).
        input_filename_stretch (str): Path to .csv file with data for helical parameter 'stretch'. File type: input. Accepted formats: csv (edam:format_3752).
        input_filename_stagger (str): Path to .csv file with data for helical parameter 'stagger'. File type: input. Accepted formats: csv (edam:format_3752).
        input_filename_buckle (str): Path to .csv file with data for helical parameter 'buckle'. File type: input. Accepted formats: csv (edam:format_3752).
        input_filename_propel (str): Path to .csv file with data for helical parameter 'propeller'. File type: input. Accepted formats: csv (edam:format_3752).
        input_filename_opening (str): Path to .csv file with data for helical parameter 'opening'. File type: input. Accepted formats: csv (edam:format_3752).
        output_csv_path (str): Path to directory where output is saved. File type: output. Accepted formats: csv (edam:format_3752).
        output_jpg_path (str): Path to .jpg file where output is saved. File type: output. Accepted formats: jpg (edam:format_3579).
        properties (dict):
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **base** (*str*) - (None) Name of base analyzed.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.intrabp_correlations.intrahpcorr import intrahelparcorrelation

            prop = { 
                'base': 'A',
            }
            intrahelparcorrelation(
                input_filename_shear='path/to/shear.csv',
                input_filename_stretch='path/to/stretch.csv',
                input_filename_stagger='path/to/stagger.csv',
                input_filename_buckle='path/to/buckle.csv',
                input_filename_propel='path/to/propel.csv',
                input_filename_opening='path/to/opening.csv',
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
            self, input_filename_shear, input_filename_stretch,
            input_filename_stagger, input_filename_buckle,
            input_filename_propel, input_filename_opening,
            output_csv_path, output_jpg_path,
            properties=None, **kwargs) -> None:
        properties = properties or {}

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
        self.base = properties.get("base", None)

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
        """Execute the :class:`IntraHelParCorrelation <intrabp_correlations.intrahpcorr.IntraHelParCorrelation>` object."""

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
        self.tmp_folder = fu.create_unique_dir(prefix="hpcorrelation_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # read input
        shear = load_data(self.io_dict["in"]["input_filename_shear"])
        stretch = load_data(self.io_dict["in"]["input_filename_stretch"])
        stagger = load_data(self.io_dict["in"]["input_filename_stagger"])
        buckle = load_data(self.io_dict["in"]["input_filename_buckle"])
        propel = load_data(self.io_dict["in"]["input_filename_propel"])
        opening = load_data(self.io_dict["in"]["input_filename_opening"])

        # get base
        if self.base is None:
            self.base = shear.columns[0]

        # make matrix
        # coordinates = ["shear", "stretch", "stagger", "buckle", "propel", "opening"]
        coordinates = [
            "shear", "stretch", "stagger", "buckle", "propel", "opening"]
        corr_matrix = pd.DataFrame(
            np.eye(6, 6), index=coordinates, columns=coordinates)

        # shear
        corr_matrix["shear"]["stretch"] = shear.corrwith(
            stretch, method="pearson")
        corr_matrix["shear"]["stagger"] = shear.corrwith(
            stagger, method="pearson")
        corr_matrix["shear"]["buckle"] = shear.corrwith(
            buckle, method=self.circlineal)
        corr_matrix["shear"]["propel"] = shear.corrwith(
            propel, method=self.circlineal)
        corr_matrix["shear"]["opening"] = shear.corrwith(
            opening, method=self.circlineal)
        # symmetric values
        corr_matrix["stretch"]["shear"] = corr_matrix["shear"]["stretch"]
        corr_matrix["stagger"]["shear"] = corr_matrix["shear"]["stagger"]
        corr_matrix["buckle"]["shear"] = corr_matrix["shear"]["buckle"]
        corr_matrix["propel"]["shear"] = corr_matrix["shear"]["propel"]
        corr_matrix["opening"]["shear"] = corr_matrix["shear"]["opening"]

        # stretch
        corr_matrix["stretch"]["stagger"] = stretch.corrwith(
            stagger, method="pearson")
        corr_matrix["stretch"]["buckle"] = stretch.corrwith(
            buckle, method=self.circlineal)
        corr_matrix["stretch"]["propel"] = stretch.corrwith(
            propel, method=self.circlineal)
        corr_matrix["stretch"]["opening"] = stretch.corrwith(
            opening, method=self.circlineal)
        # symmetric values
        corr_matrix["stagger"]["stretch"] = corr_matrix["stretch"]["stagger"]
        corr_matrix["buckle"]["stretch"] = corr_matrix["stretch"]["buckle"]
        corr_matrix["propel"]["stretch"] = corr_matrix["stretch"]["propel"]
        corr_matrix["opening"]["stretch"] = corr_matrix["stretch"]["opening"]

        # stagger
        corr_matrix["stagger"]["buckle"] = stagger.corrwith(
            buckle, method=self.circlineal)
        corr_matrix["stagger"]["propel"] = stagger.corrwith(
            propel, method=self.circlineal)
        corr_matrix["stagger"]["opening"] = stagger.corrwith(
            opening, method=self.circlineal)
        # symmetric values
        corr_matrix["buckle"]["stagger"] = corr_matrix["stagger"]["buckle"]
        corr_matrix["propel"]["stagger"] = corr_matrix["stagger"]["propel"]
        corr_matrix["opening"]["stagger"] = corr_matrix["stagger"]["opening"]

        # buckle
        corr_matrix["buckle"]["propel"] = buckle.corrwith(
            propel, method=self.circular)
        corr_matrix["buckle"]["opening"] = buckle.corrwith(
            opening, method=self.circular)
        # symmetric values
        corr_matrix["propel"]["buckle"] = corr_matrix["buckle"]["propel"]
        corr_matrix["opening"]["buckle"] = corr_matrix["buckle"]["opening"]

        # propel
        corr_matrix["propel"]["opening"] = propel.corrwith(
            opening, method=self.circular)
        # symmetric values
        corr_matrix["opening"]["propel"] = corr_matrix["propel"]["opening"]

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
            f"for Base Pair Step \'{self.base}\'")
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


def intrahelparcorrelation(
        input_filename_shear: str, input_filename_stretch: str,
        input_filename_stagger: str, input_filename_buckle: str,
        input_filename_propel: str, input_filename_opening: str,
        output_csv_path: str, output_jpg_path: str,
        properties: dict = None, **kwargs) -> int:
    """Create :class:`IntraHelParCorrelation <intrabp_correlations.intrahpcorr.IntraHelParCorrelation>` class and
    execute the :meth:`launch() <intrabp_correlations.intrahpcorr.IntraHelParCorrelation.launch>` method."""

    return IntraHelParCorrelation(
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
    parser = argparse.ArgumentParser(description='Load helical parameter file and save base data individually.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_filename_shear', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_stretch', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_stagger', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_buckle', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_propel', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_opening', required=True,
                               help='Path to csv file with inputs. Accepted formats: csv.')
    required_args.add_argument('--output_csv_path', required=True,
                               help='Path to output file. Accepted formats: csv.')
    required_args.add_argument('--output_jpg_path', required=True,
                               help='Path to output file. Accepted formats: csv.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    intrahelparcorrelation(
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
