#!/usr/bin/env python3

"""Module containing the DnaTimeseriesUnzip class and the command line interface."""
import re
import zipfile
import shutil
import argparse

from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


class DnaTimeseriesUnzip(BiobbObject):
    """
    | biobb_dna DnaTimeseriesUnzip
    | Tool for extracting dna_timeseries output files.

    Args:
        input_zip_file (str): Zip file with dna_timeseries output files. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/dna/timeseries_output.zip>`_. Accepted formats: zip (edam:format_3987).
        output_path_csv (str): dna_timeseries output csv file contained within input_zip_file. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/dna/dna_timeseries_unzip.csv>`_. Accepted formats: csv (edam:format_3752).
        output_path_jpg (str): dna_timeseries output jpg file contained within input_zip_file. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/dna/dna_timeseries_unzip.jpg>`_. Accepted formats: jpg (edam:format_3579).
        output_list_path (str) (Optional): Text file with a list of all dna_timeseries output files contained within input_zip_file. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/dna/dna_timeseries_unzip.txt>`_. Accepted formats: txt (edam:format_2330).
        properties (dic):
            * **type** (*str*) - (None) Type of analysis, series or histogram. Values: series, hist.
            * **parameter** (*str*) - (None) Type of parameter. Values: majd, majw, mind, minw, inclin, tip, xdisp, ydisp, shear, stretch, stagger, buckle, propel, opening, rise, roll, twist, shift, slide, tilt, alphaC, alphaW, betaC, betaW, gammaC, gammaW, deltaC, deltaW, epsilC, epsilW, zetaC, zetaW, chiC, chiW, phaseC, phaseW.
            * **sequence** (*str*) - (None) Nucleic acid sequence used for generating dna_timeseries output file.
            * **index** (*int*) - (0) Base pair index in the parameter 'sequence', starting from 0.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.dna.dna_timeseries_unzip import dna_timeseries_unzip
            prop = {
                'type': 'hist',
                'parameter': 'shift',
                'sequence': 'CGCGAATTCGCG',
                'index': 5
            }
            dna_timeseries_unzip(
                input_zip_file='/path/to/dna_timeseries/output.zip',
                output_path='/path/to/output.csv',
                output_list_path='/path/to/output.txt'
                properties=prop)
    Info:
        * wrapped_software:
            * name: In house
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_zip_file,
                 output_path_csv, output_path_jpg, output_list_path=None, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_zip_file': input_zip_file
            },
            'out': {
                'output_path_csv': output_path_csv,
                'output_path_jpg': output_path_jpg,
                'output_list_path': output_list_path
            }
        }

        # Properties specific for BB
        self.type = properties.get('type', None)
        self.parameter = properties.get('parameter', None)
        self.sequence = properties.get('sequence', None)
        self.index = properties.get('index', 0)
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`DnaTimeseriesUnzip <biobb_dna.dna.dna_timeseries_unzip.DnaTimeseriesUnzip>` object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Check that both properties are set
        if self.type is None or self.parameter is None or self.sequence is None:
            fu.log("Properties 'type', 'parameter' and 'sequence' are mandatory to run DnaTimeseriesUnzip. Please set them.",
                   self.out_log, self.global_log)
            exit(1)

        # Check that the type is valid
        if self.type not in ["series", "hist"]:
            fu.log(f"Type {self.type} not valid. Valid types are: series, hist.",
                   self.out_log, self.global_log)
            exit(1)

        # Check that the parameter is valid
        if self.parameter not in ["majd", "majw", "mind", "minw", "inclin", "tip", "xdisp", "ydisp", "shear", "stretch",
                                  "stagger", "buckle", "propel", "opening", "rise", "roll", "twist", "shift", "slide",
                                  "tilt", "alphaC", "alphaW", "betaC", "betaW", "gammaC", "gammaW", "deltaC", "deltaW",
                                  "epsilC", "epsilW", "zetaC", "zetaW", "chiC", "chiW", "phaseC", "phaseW"]:
            fu.log(f"Parameter {self.parameter} not valid. Valid parameters are: majd, majw, mind, minw, inclin, tip, xdisp, ydisp, shear, stretch, stagger, buckle, propel, opening, rise, roll, twist, shift, slide, tilt, alphaC, alphaW, betaC, betaW, gammaC, gammaW, deltaC, deltaW, epsilC, epsilW, zetaC, zetaW, chiC, chiW, phaseC, phaseW.",
                   self.out_log, self.global_log)
            exit(1)

        # Check that the sequence is valid
        pattern = r'^[ACGT]+$'
        if not re.match(pattern, self.sequence):
            fu.log(f"Sequence {self.sequence} not valid. Only 'A', 'C', 'G' or 'T' bases allowed.",
                   self.out_log, self.global_log)
            exit(1)

        # Check that the index is valid
        if self.index < 0 or self.index >= len(self.sequence) - 1:
            fu.log(f"Index {self.index} not valid. It should be between 0 and {len(self.sequence) - 2}.",
                   self.out_log, self.global_log)
            exit(1)

        # Get index sequence base and next base
        bp = self.sequence[self.index] + self.sequence[self.index + 1]

        # Get the filename
        filename = f"{self.type}_{self.parameter}_{self.index + 1}_{bp}"
        csv_file = f"{filename}.csv"
        jpg_file = f"{filename}.jpg"

        # Unzip the file
        with zipfile.ZipFile(self.stage_io_dict["in"]["input_zip_file"], 'r') as zip_ref:
            # Check if the csv file exists in the zip file
            if csv_file in zip_ref.namelist():
                # Extract the file
                fu.log(f'{csv_file} exists, copying into {self.stage_io_dict["out"]["output_path_csv"]}.',
                       self.out_log, self.global_log)
                with zip_ref.open(csv_file) as source, open(self.stage_io_dict["out"]["output_path_csv"], "wb") as target:
                    shutil.copyfileobj(source, target)
            else:
                fu.log(f"File {csv_file} not found in the zip file.", self.out_log, self.global_log)
                exit(1)

            # Check if the jpg file exists in the zip file
            if jpg_file in zip_ref.namelist():
                # Extract the file
                fu.log(f'{jpg_file} exists, copying into {self.stage_io_dict["out"]["output_path_jpg"]}.',
                       self.out_log, self.global_log)
                with zip_ref.open(jpg_file) as source, open(self.stage_io_dict["out"]["output_path_jpg"], "wb") as target:
                    shutil.copyfileobj(source, target)
            else:
                fu.log(f"File {jpg_file} not found in the zip file.", self.out_log, self.global_log)
                exit(1)

            # Write the list of files
            if self.stage_io_dict["out"]["output_list_path"]:
                with open(self.stage_io_dict["out"]["output_list_path"], "w") as f:
                    for name in zip_ref.namelist():
                        f.write(f"{name}\n")

        # Run Biobb block
        # self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporary file(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def dna_timeseries_unzip(
        input_zip_file: str,
        output_path_csv: str,
        output_path_jpg: str,
        output_list_path: str = None,
        properties: dict = None,
        **kwargs) -> int:
    """Create :class:`DnaTimeseriesUnzip <biobb_dna.dna.dna_timeseries_unzip.DnaTimeseriesUnzip>` class and
    execute the :meth:`launch() <biobb_dna.dna.dna_timeseries_unzip.DnaTimeseriesUnzip.launch>` method."""

    return DnaTimeseriesUnzip(
        input_zip_file=input_zip_file,
        output_path_csv=output_path_csv,
        output_path_jpg=output_path_jpg,
        output_list_path=output_list_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Tool for extracting dna_timeseries output files.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_zip_file', required=True,
                               help='Zip file with dna_timeseries output files. Accepted formats: zip.')
    required_args.add_argument('--output_path_csv', required=True,
                               help='dna_timeseries output csv file contained within input_zip_file. Accepted formats: csv.')
    required_args.add_argument('--output_path_jpg', required=True,
                               help='dna_timeseries output jpg file contained within input_zip_file. Accepted formats: jpg.')
    parser.add_argument('--output_list_path', required=False,
                        help='Text file with a list of all dna_timeseries output files contained within input_zip_file. Accepted formats: txt.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    dna_timeseries_unzip(
        input_zip_file=args.input_zip_file,
        output_path_csv=args.output_path_csv,
        output_path_jpg=args.output_path_jpg,
        output_list_path=args.output_list_path,
        properties=properties)


if __name__ == '__main__':
    main()
