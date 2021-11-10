#!/usr/bin/env python3

"""Module containing the HelParStiffness class and the command line interface."""
import argparse
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_dna.utils.loader import load_data


class BPStiffness(BiobbObject):
    """
    | biobb_dna BPStiffness
    | Calculate stiffness constants matrix between all six helical parameters for a single base pair step.

    Args:        
        input_filename_shift (str): Path to csv file with data for helical parameter 'shift'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_shift_AA.csv>`_. Accepted formats: csv (edam:format_3752)
        input_filename_slide (str): Path to csv file with data for helical parameter 'slide'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_slide_AA.csv>`_. Accepted formats: csv (edam:format_3752)
        input_filename_rise (str): Path to csv file with data for helical parameter 'rise'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_rise_AA.csv>`_. Accepted formats: csv (edam:format_3752)
        input_filename_tilt (str): Path to csv file with data for helical parameter 'tilt'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_tilt_AA.csv>`_. Accepted formats: csv (edam:format_3752)
        input_filename_roll (str): Path to csv file with data for helical parameter 'roll'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_roll_AA.csv>`_. Accepted formats: csv (edam:format_3752)
        input_filename_twist (str): Path to csv file with data for helical parameter 'twist'. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_twist_AA.csv>`_. Accepted formats: csv (edam:format_3752)
        output_csv_path (str): Path to directory where stiffness matrix file is saved as a csv file. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/stiffness/stiffbp_ref.csv>`_. Accepted formats: csv (edam:format_3752)
        output_jpg_path (str): Path to directory where stiffness heatmap image is saved as a jpg file. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/stiffness/stiffbp_ref.jpg>`_. Accepted formats: jpg (edam:format_3579)
        properties (dict):
            * **KT** (*float*) - (0.592186827) Value of Boltzmann temperature factor.
            * **scaling** (*list*) - ([1, 1, 1, 10.6, 10.6, 10.6]) Values by which to scale stiffness. Positions correspond to helical parameters in the order: shift, slide, rise, tilt, roll, twist.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.stiffness.basepair_stiffness import basepair_stiffness

            prop = { 
                'KT': 0.592186827,
                'scaling': [1, 1, 1, 10.6, 10.6, 10.6]
            }
            basepair_stiffness(
                input_filename_shift='path/to/basepair/shift.csv',
                input_filename_slide='path/to/basepair/slide.csv',
                input_filename_rise='path/to/basepair/rise.csv',
                input_filename_tilt='path/to/basepair/tilt.csv',
                input_filename_roll='path/to/basepair/roll.csv',
                input_filename_twist='path/to/basepair/twist.csv',
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

    def __init__(self, input_filename_shift, input_filename_slide,
                 input_filename_rise, input_filename_tilt,
                 input_filename_roll, input_filename_twist,
                 output_csv_path, output_jpg_path, properties=None, **kwargs) -> None:
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
        self.KT = properties.get(
            "KT", 0.592186827)
        self.scaling = properties.get(
            "scaling", [1, 1, 1, 10.6, 10.6, 10.6])

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`BPStiffness <stiffness.basepair_stiffness.BPStiffness>` object."""

        # Check the properties
        fu.check_properties(self, self.properties)

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir(prefix="bp_stiffness_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # read input
        shift = load_data(
            self.io_dict["in"]["input_filename_shift"])
        slide = load_data(
            self.io_dict["in"]["input_filename_slide"])
        rise = load_data(
            self.io_dict["in"]["input_filename_rise"])
        tilt = load_data(
            self.io_dict["in"]["input_filename_tilt"])
        roll = load_data(
            self.io_dict["in"]["input_filename_roll"])
        twist = load_data(
            self.io_dict["in"]["input_filename_twist"])

        # build matrix cols_arr from helpar input data files
        coordinates = ["shift", "slide", "rise", "tilt", "roll", "twist"]
        basepairname = shift.columns[0]
        helpar_matrix = pd.concat(
            [shift, slide, rise, tilt, roll, twist], axis=1)
        helpar_matrix.columns = coordinates
        # covariance
        cov_df = helpar_matrix.cov()
        # stiffness
        stiff = np.linalg.inv(cov_df) * self.KT
        stiff_diag = stiff * np.array(self.scaling)
        stiff_df = pd.DataFrame(
            stiff_diag,
            columns=cov_df.columns,
            index=cov_df.index)
        stiff_df.index.name = basepairname

        # save csv data
        stiff_df.to_csv(Path(self.io_dict["out"]["output_csv_path"]))

        # create heatmap
        fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
        axs.pcolor(stiff_df)
        # Loop over data dimensions and create text annotations.
        for i in range(len(stiff_df)):
            for j in range(len(stiff_df)):
                axs.text(
                    j+.5,
                    i+.5,
                    f"{stiff_df[coordinates[j]].loc[coordinates[i]]:.2f}",
                    ha="center",
                    va="center",
                    color="w")
        axs.text(
            0, -1.35,
            "Units:\n"
            "Diagonal Shift/Slide/Rise in kcal/(mol*Å²), Diagonal Tilt/Roll/Twist in kcal/(mol*degree²)\n"
            "Out of Diagonal: Shift/Slide/Rise in kcal/(mol*Å), Out of Diagonal Tilt/Roll/Twist in kcal/(mol*degree)",
            fontsize=6)
        axs.set_xticks([i + 0.5 for i in range(len(stiff_df))])
        axs.set_xticklabels(stiff_df.columns, rotation=90)
        axs.set_yticks([i+0.5 for i in range(len(stiff_df))])
        axs.set_yticklabels(stiff_df.index)
        axs.set_title(
            f"Stiffness Constants for Base Pair Step \'{basepairname}\'")
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


def basepair_stiffness(
        input_filename_shift: str, input_filename_slide: str,
        input_filename_rise: str, input_filename_tilt: str,
        input_filename_roll: str, input_filename_twist: str,
        output_csv_path: str, output_jpg_path: str, properties: dict = None, **kwargs) -> int:
    """Create :class:`BPStiffness <stiffness.basepair_stiffness.BPStiffness>` class and
    execute the :meth:`launch() <stiffness.basepair_stiffness.BPStiffness.BPStiffness.launch>` method."""

    return BPStiffness(
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
    parser = argparse.ArgumentParser(description='Calculate stiffness constants matrix between all six helical parameters for a single base pair step.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_filename_shift', required=True,
                               help='Path to csv file with shift inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_slide', required=True,
                               help='Path to csv file with slide inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_rise', required=True,
                               help='Path to csv file with rise inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_tilt', required=True,
                               help='Path to csv file with tilt inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_roll', required=True,
                               help='Path to csv file with roll inputs. Accepted formats: csv.')
    required_args.add_argument('--input_filename_twist', required=True,
                               help='Path to csv file with twist inputs. Accepted formats: csv.')
    required_args.add_argument('--output_csv_path', required=True,
                               help='Path to output covariance data file. Accepted formats: csv.')
    required_args.add_argument('--output_jpg_path', required=True,
                               help='Path to output covariance data file. Accepted formats: csv.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    basepair_stiffness(
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
