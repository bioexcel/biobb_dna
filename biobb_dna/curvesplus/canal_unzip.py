#!/usr/bin/env python3

"""Module containing the CanalUnzip class and the command line interface."""
import re
import zipfile
import shutil
import argparse

from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


class CanalUnzip(BiobbObject):
    """
    | biobb_dna CanalUnzip
    | Tool for extracting biobb_canal output files.

    Args:
        input_zip_file (str): Zip file with Canal output files. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/curvesplus/canal_output.zip>`_. Accepted formats: zip (edam:format_3987).
        output_path (str): Canal output file contained within input_zip_file. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/curvesplus/canal_unzip_output.ser>`_. Accepted formats: ser (edam:format_2330), his (edam:format_3905), cor (edam:format_3465).
        output_list_path (str) (Optional): Text file with a list of all Canal output files contained within input_zip_file. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/curvesplus/canal_unzip_output.txt>`_. Accepted formats: txt (edam:format_2330).
        properties (dic):
            * **type** (*str*) - (None) Type of file. Values: series, histo, corr.
            * **helpar_name** (*str*) - (None) Helical parameter name, only for 'series' and 'histo' types. Values: alphaC, alphaW, ampC, ampW, ax-bend, betaC, betaW, buckle, chiC, chiW, curv, deltaC, deltaW, epsilC, epsilW, gammaC, gammaW, h-ris, h-twi, inclin, majd, majw, mind, minw, opening, phaseC, phaseW, propel, reg, rise, roll, shear, shift, slide, stagger, stretch, tbend, tilt, tip, twist, xdisp, ydisp, zetaC, zetaW.
            * **correlation** (*str*) - (None) Correlation indexes separated by underscore (ie '98_165'), only for 'corr' type.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.curvesplus.canal_unzip import canal_unzip
            prop = {
                'type': 'series',
                'helpar_name': 'alphaC'
            }
            canal_unzip(
                input_zip_file='/path/to/canal/output.zip',
                output_path='/path/to/output.ser',
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
                 output_path, output_list_path=None, properties=None, **kwargs) -> None:
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
                'output_path': output_path,
                'output_list_path': output_list_path
            }
        }

        # Properties specific for BB
        self.type = properties.get('type', None)
        self.helpar_name = properties.get('helpar_name', None)
        self.correlation = properties.get('correlation', None)
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`CanalUnzip <biobb_dna.curvesplus.canal_unzip.CanalUnzip>` object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Check that both properties are set
        if self.type is None:
            fu.log("Property 'type' is mandatory to run CanalUnzip. Please set it.",
                   self.out_log, self.global_log)
            exit(1)

        # Check that helpar_name is set if type is series or histo
        if self.type in ["series", "histo"] and self.helpar_name is None:
            fu.log("Property 'helpar_name' is mandatory to run CanalUnzip with type 'series' or 'histo'. Please set it.",
                   self.out_log, self.global_log)
            exit(1)

        # Check that correlation is set if type is corr
        if self.type == "corr" and self.correlation is None:
            fu.log("Property 'correlation' is mandatory to run CanalUnzip with type 'corr'. Please set it.",
                   self.out_log, self.global_log)
            exit(1)

        extensions = {
            "series": "ser",
            "histo": "his",
            "corr": "cor"
        }
        # Check that the type is valid
        if self.type not in extensions:
            fu.log(f"Type {self.type} not valid. Valid types are: {', '.join(extensions.keys())}.",
                   self.out_log, self.global_log)
            exit(1)

        # generate sufix
        sufix = ""
        if self.type == "corr":
            # Check that the correlation is valid
            pattern = r'\d+_\d+'
            if not re.match(pattern, self.correlation):
                fu.log(f"Correlation {self.correlation} not valid. It should match the pattern <number_number>.",
                       self.out_log, self.global_log)
                exit(1)
            sufix = self.correlation
        else:
            # Check that the helpar_name is valid
            if self.helpar_name not in ["alphaC", "alphaW", "ampC", "ampW", "ax-bend", "betaC", "betaW", "buckle",
                                        "chiC", "chiW", "curv", "deltaC", "deltaW", "epsilC", "epsilW", "gammaC",
                                        "gammaW", "h-ris", "h-twi", "inclin", "majd", "majw", "mind", "minw",
                                        "opening", "phaseC", "phaseW", "propel", "reg", "rise", "roll", "shear",
                                        "shift", "slide", "stagger", "stretch", "tbend", "tilt", "tip", "twist",
                                        "xdisp", "ydisp", "zetaC", "zetaW"]:
                fu.log(f"Parameter {self.helpar_name} not valid. Valid parameters are: alphaC, alphaW, ampC, ampW, ax-bend, betaC, betaW, buckle, chiC, chiW, curv, deltaC, deltaW, epsilC, epsilW, gammaC, gammaW, h-ris, h-twi, inclin, majd, majw, mind, minw, opening, phaseC, phaseW, propel, reg, rise, roll, shear, shift, slide, stagger, stretch, tbend, tilt, tip, twist, xdisp, ydisp, zetaC, zetaW.",
                       self.out_log, self.global_log)
                exit(1)
            sufix = self.helpar_name

        # Generate the filename
        filename = f"canal_output_{sufix}.{extensions[self.type]}"

        # Unzip the file
        with zipfile.ZipFile(self.stage_io_dict["in"]["input_zip_file"], 'r') as zip_ref:
            # Check if the file exists in the zip file
            if filename in zip_ref.namelist():
                # Extract the file
                fu.log(f'{filename} exists, copying into {self.stage_io_dict["out"]["output_path"]}.',
                       self.out_log, self.global_log)
                with zip_ref.open(filename) as source, open(self.stage_io_dict["out"]["output_path"], "wb") as target:
                    shutil.copyfileobj(source, target)
            else:
                fu.log(f"File {filename} not found in the zip file.", self.out_log, self.global_log)
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


def canal_unzip(
        input_zip_file: str,
        output_path: str,
        output_list_path: str = None,
        properties: dict = None,
        **kwargs) -> int:
    """Create :class:`CanalUnzip <biobb_dna.curvesplus.canal_unzip.CanalUnzip>` class and
    execute the :meth:`launch() <biobb_dna.curvesplus.canal_unzip.CanalUnzip.launch>` method."""

    return CanalUnzip(
        input_zip_file=input_zip_file,
        output_path=output_path,
        output_list_path=output_list_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Tool for extracting biobb_canal output files.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_zip_file', required=True,
                               help='Zip file with Canal output files. Accepted formats: zip.')
    required_args.add_argument('--output_path', required=True,
                               help='Canal output file contained within input_zip_file. Accepted formats: ser, his, cor.')
    parser.add_argument('--output_list_path', required=False,
                        help='Text file with a list of all Canal output files contained within input_zip_file. Accepted formats: txt.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    canal_unzip(
        input_zip_file=args.input_zip_file,
        output_path=args.output_path,
        output_list_path=args.output_list_path,
        properties=properties)


if __name__ == '__main__':
    main()
