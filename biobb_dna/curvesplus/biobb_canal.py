#!/usr/bin/env python3

"""Module containing the Canal class and the command line interface."""
import os
import shutil
import zipfile
import argparse
from pathlib import Path

from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper


class Canal():
    """
    | biobb_dna Canal
    | Wrapper for the Canal executable that is part of the Curves+ software suite. 

    Args:        
        input_cda_file (str): Input cda file, from Cur+ output. File type: input. Accepted formats: cda (edam:format_2330).
        input_lis_file (str): (Optional) Input lis file, from Cur+ output. File type: input. Accepted formats: lis (edam:format_2330).
        output_zip_path (str): zip filename for output files. File type: output.  Accepted formats: zip (edam:format_3987).
        properties (dic):
            * **bases** (*str*) - (None) sequence of bases to be searched for in the I/P data (default is blank, meaning no specified sequence). 
            * **itst** (*int*) - (0) Iteration start index.
            * **itnd** (*int*) - (0) Iteration end index.
            * **itdel** (*int*) - (1) Iteration delimiter. 
            * **lev1** (*int*) - (0) Lower base level limit (i.e. base pairs) used for analysis.
            * **lev2** (*int*) - (0) Upper base level limit used for analysis. If lev1 > 0 and lev2 = 0, lev2 is set to lev1 (i.e. analyze lev1 only). If lev1=lev2=0, lev1 is set to 1 and lev2 is set to the length of the oligmer (i.e. analyze all levels).
            * **nastr** (*str*) - ('NA') character string used to indicate missing data in .ser files.
            * **cormin** (*float*) - (0.6) minimal absolute value for printing linear correlation coefficients between pairs of analyzed variables.
            * **series** (*str*) - (False) if True then output spatial or time series data. Only possible for the analysis of single structures or single trajectories.
            * **histo** (*str*) - (False) if True then output histogram data.
            * **corr** (*str*) - (False) if True than output linear correlation coefficients between all variables.
            * **sequence** (*str*) - (Optional) sequence of the first strand of the corresponding DNA fragment, for each .cda file. If not given it will be parsed from .lis file.
            * **canal_exec** (*str*) - ('Canal') Path to Canal executable, otherwise the program wil look for Canal executable in the binaries folder.
    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.curvesplus.biobb_canal import canal
            prop = { 
                'series': '.t.',
                'histo': '.t.',
                'sequence': 'CGCGAATTCGCG'
            }
            canal(
                input_cda_file='/path/to/curves/output.cda',
                output_zip_path='/path/to/output.zip',
                properties=prop)
    Info:
        * wrapped_software:
            * name: Canal
            * version: >=2.6
            * license: BSD 3-Clause
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_cda_file, input_lis_file=None,
                 output_zip_path=None, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_cda_file': input_cda_file,
                'input_lis_file': input_lis_file,
            },
            'out': {
                'output_zip_path': output_zip_path
            }
        }

        # Properties specific for BB
        self.bases = properties.get('bases', None)
        self.nastr = properties.get('nastr', None)
        self.cormin = properties.get('cormin', 0.6)
        self.lev1 = properties.get('lev1', 0)
        self.lev2 = properties.get('lev2', 0)
        self.itst = properties.get('itst', 0)
        self.itnd = properties.get('itnd', 0)
        self.itdel = properties.get('itdel', 1)
        self.series = ".t." if properties.get('series', False) else ".f."
        self.histo = ".t." if properties.get('histo', False) else ".f."
        self.corr = ".t." if properties.get('corr', False) else ".f."
        self.sequence = properties.get('sequence', None)
        self.canal_exec = properties.get('canal_exec', 'Canal')
        self.properties = properties

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
        """Execute the :class:`Canal <biobb_dna.curvesplus.biobb_canal.Canal>` object."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Check the properties
        fu.check_properties(self, self.properties)
        if self.sequence is None:
            if self.io_dict['in']['input_lis_file'] is None:
                raise RuntimeError(
                    "if no sequence is passed in the configuration, "
                    "you must at least specify `input_lis_file` "
                    "so sequence can be parsed from there")
            lis_lines = Path(
                self.io_dict['in']['input_lis_file']).read_text().splitlines()
            for line in lis_lines:
                if line.strip().startswith("Strand  1"):
                    self.sequence = line.split(" ")[-1]
                    fu.log(
                        f"using sequence {self.sequence} "
                        f"from {self.io_dict['in']['input_lis_file']}",
                        out_log)

        # Restart
        if self.restart:
            output_file_list = [self.io_dict['out']['output_zip_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' %
                       self.step, out_log, self.global_log)
                return 0

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir(prefix="canal_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # copy input files to temporary folder
        shutil.copy(
            self.io_dict['in']['input_cda_file'],
            self.tmp_folder)
        tmp_cda_path = Path(self.io_dict['in']['input_cda_file']).name
        if self.io_dict['in']['input_lis_file'] is not None:
            shutil.copy(
                self.io_dict['in']['input_lis_file'],
                self.tmp_folder)

        # change directory to temporary folder
        original_directory = os.getcwd()
        os.chdir(self.tmp_folder)

        # create intructions
        instructions = [
            f"{self.canal_exec} <<! ",
            "&inp",
            "  lis=canal_output,"]
        if self.bases is not None:
            # add topology file if needed
            fu.log('Appending sequence of bases to be searched to command',
                   out_log, self.global_log)
            instructions.append(f"  seq={self.bases},")
        if self.nastr is not None:
            # add topology file if needed
            fu.log('Adding null values string specification to command',
                   out_log, self.global_log)
            instructions.append(f"  nastr={self.nastr},")

        instructions = instructions + [
            f"  cormin={self.cormin},",
            f"  lev1={self.lev1},lev2={self.lev2},",
            f"  itst={self.itst},itnd={self.itnd},itdel={self.itdel},",
            f"  histo={self.histo},",
            f"  series={self.series},",
            f"  corr={self.corr},",
            "&end",
            f"{tmp_cda_path} {self.sequence}",
            "!"]

        cmd = ["\n".join(instructions)]
        fu.log('Creating command line with instructions and required arguments',
               out_log, self.global_log)
        # Launch execution
        returncode = cmd_wrapper.CmdWrapper(
            cmd, out_log, err_log, self.global_log).launch()

        # change back to original directory
        os.chdir(original_directory)

        # create zipfile and write output inside
        zf = zipfile.ZipFile(
            Path(self.io_dict["out"]["output_zip_path"]), "w")
        for canal_outfile in Path(self.tmp_folder).glob("canal_output*"):
            zf.write(
                canal_outfile,
                arcname=canal_outfile.name)
        zf.close()

        # Remove temporary file(s)
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)

        return returncode


def canal(
        input_cda_file: str,
        output_zip_path: str,
        input_lis_file: str = None,
        properties: dict = None,
        **kwargs) -> int:
    """Create :class:`Canal <biobb_dna.curvesplus.biobb_canal.Canal>` class and
    execute the :meth:`launch() <biobb_dna.curvesplus.biobb_canal.Canal.launch>` method."""

    return Canal(
        input_cda_file=input_cda_file,
        input_lis_file=input_lis_file,
        output_zip_path=output_zip_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Execute Canal from the Curves+ software suite.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_cda_file', required=True,
                               help='cda input file from Curves+ output. Accepted formats: cda.')
    required_args.add_argument('--output_zip_path', required=True,
                               help='Filename for .zip file with Canal output. Accepted formats: zip.')
    parser.add_argument('--input_lis_file', required=False,
                        help='lis input file from Curves+ output. Accepted formats: lis.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    canal(
        input_cda_file=args.input_cda_file,
        input_lis_file=args.input_lis_file,
        output_zip_path=args.output_zip_path,
        properties=properties)


if __name__ == '__main__':
    main()
