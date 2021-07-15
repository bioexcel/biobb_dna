#!/usr/bin/env python3

"""Module containing the HelParTimeSeries class and the command line interface."""
import argparse
import shutil
import zipfile
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_dna.dna.loader import read_series


class HelParTimeSeries():
    """
    | biobb_dna HelParTimeSeries
    | Load .ser file for a given helical parameter, read and analyze each column corresponding to a base. Created time series and histogram plots for each base.

    Args:
        input_serfile_path (str): Path to .ser file for helical parameter. File is expected to be a table, with the first column being an index and the rest the helical parameter values for each base/basepair. File type: input. Accepted formats: ser
        output_file_path (str): Path to output .zip files where data is saved. File type: output. Accepted formats: .zip
        properties (dict):
            * **strand1** (*str*) - Nucleic acid sequence for the first strand (5'->3') corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *usecols* option).
            * **strand2** (*str*) - Nucleic acid sequence for the second strand (3'->5') corresponding to the input .ser file.
            * **bins** (*int* or *sequence* or *str*) - Bins for histogram. Parameter has same options as matplotlib.pyplot.hist.
            * **helpar_name** (*str*) - (helical_parameter) helical parameter name.
            * **stride** (*int*) - (1000) granularity of the number of snapshots for plotting time series.
            * **usecols** (*list*) - (None) list of column indices to use.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.dna.timeseries import HelParTimeSeries

            prop = {
                'helpar_name': 'twist',
                'usecols': [1,2,3,4,5],
                'strand1': 'GCAACGTGCTATGGAAGC',
                'strand2': 'GCTTCCATAGCACGTTGC'
            }
            HelParTimeSeries(
                input_serfile_path='/path/to/twist.ser',
                output_file_path='/path/to/output/file.zip'
                properties=prop)

        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_serfile_path, output_file_path,
                 properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_serfile_path': input_serfile_path,
            },
            'out': {
                'output_file_path': output_file_path
            }
        }

        self.properties = properties
        self.strand1 = properties.get("strand1")
        self.strand2 = properties.get("strand2")
        self.bins = properties.get("bins", "auto")
        self.stride = properties.get(
            "stride", 10)
        self.usecols = properties.get(
            "usecols", None)
        helpar_name = properties.get(
            "helpar_name", None)

        if helpar_name is None:
            for hp in [
                    "shift", "slide", "rise",
                    "tilt", "roll", "twist",
                    "buckle", "opening", "propel",
                    "shear", "stagger", "stretch"]:
                if hp in input_serfile_path:
                    helpar_name = hp
            if helpar_name is None:
                raise ValueError("Helical Parameter name must be specified!")
        self.helpar_name = helpar_name

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
        """Execute the :class:`HelParTimeSeries <dna.timeseries.HelParTimeSeries>` object."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Check the properties
        fu.check_properties(self, self.properties)

        # Restart
        if self.restart:
            output_file_list = [self.io_dict['out']['output_file_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' %
                       self.step, out_log, self.global_log)
                return 0

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir(prefix="timeseries_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # Copy input_serfile_path to temporary folder
        shutil.copy(self.io_dict['in']['input_serfile_path'], self.tmp_folder)

        # read input .ser file and create dataframe
        ser_data = read_series(
            self.io_dict['in']['input_serfile_path'], self.usecols)
        hp_basepairs = ["shift", "slide", "rise", "tilt", "roll", "twist"]
        hp_singlebases = [
            "buckle", "opening", "propel", "shear", "stagger", "stretch"]
        if self.helpar_name in hp_basepairs:
            step = 1
        elif self.helpar_name in hp_singlebases:
            step = 0
        strand1 = self.strand1
        strand2 = self.strand2[::-1]
        ser_data.columns = [
            f"{strand1[col-step-1:col]}{strand2[col-step-1:col][::-1]}"
            for col in ser_data.columns]

        # write output files for all selected bases (one per column)
        zf = zipfile.ZipFile(
            Path(self.io_dict["out"]["output_file_path"]), "w")
        for col in ser_data.columns:
            fu.log(f"Computing base number {col}...")

            # column series
            series_colfn = f"series.{self.helpar_name}.{col}"
            ser_data.to_csv(
                Path(self.tmp_folder) / f"{series_colfn}.csv", columns=[col])
            # save table
            zf.write(
                Path(self.tmp_folder) / f"{series_colfn}.csv", arcname=f"{series_colfn}.csv")

            fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
            reduced_data = ser_data[col].loc[::self.stride]
            axs.plot(reduced_data.index, reduced_data.to_numpy())
            axs.set_xlabel("Time (Snapshots)")
            axs.set_ylabel(self.helpar_name)
            axs.set_title(
                f"Helical Parameter vs Time: {self.helpar_name} "
                f"(base {col})")
            fig.savefig(
                Path(self.tmp_folder) / f"{series_colfn}.jpg", format="jpg")
            # save plot
            zf.write(
                Path(self.tmp_folder) / f"{series_colfn}.jpg", arcname=f"{series_colfn}.jpg")
            plt.close()

            # columns histogram
            hist_colfn = f"hist.{self.helpar_name}.{col}"
            fig, axs = plt.subplots(1, 1, dpi=300, tight_layout=True)
            ybins, x, _ = axs.hist(ser_data[col], bins=self.bins)
            pd.DataFrame({"bins": x[:-1], "value": ybins}).to_csv(
                Path(self.tmp_folder) / f"{hist_colfn}.csv",
                index=False)
            # save table
            zf.write(
                Path(self.tmp_folder) / f"{hist_colfn}.csv",
                arcname=f"{hist_colfn}.csv")

            axs.set_ylabel("density")
            fig.savefig(
                Path(self.tmp_folder) / f"{hist_colfn}.jpg",
                format="jpg")
            # save plot
            zf.write(
                Path(self.tmp_folder) / f"{hist_colfn}.jpg",
                arcname=f"{hist_colfn}.jpg")
            plt.close()
        zf.close()

        # Remove temporary file(s)
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)

        return 0


def helpartimeseries(
        input_serfile_path: str, output_file_path: str,
        properties: dict = None, **kwargs) -> int:
    """Create :class:`HelParTimeSeries <dna.timeseries.HelParTimeSeries>` class and
    execute the :meth:`launch() <dna.timeseries.HelParTimeSeries.launch>` method."""

    return HelParTimeSeries(
        input_serfile_path=input_serfile_path,
        output_file_path=output_file_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Load helical parameter file and save base data individually.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False,
                        help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_serfile_path', required=True,
                               help='Helical parameter input ser file path. Accepted formats: ser.')
    required_args.add_argument('--output_file_path', required=True,
                               help='Path to output directory.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    helpartimeseries(
        input_serfile_path=args.input_serfile_path,
        output_file_path=args.output_file_path,
        properties=properties)


if __name__ == '__main__':
    main()
