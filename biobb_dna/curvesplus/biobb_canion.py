#!/usr/bin/env python3

"""Module containing the Canion class and the command line interface."""
import os
import zipfile
import argparse
import shutil
from pathlib import Path
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper


class Canion():
    """
    | biobb_dna Canion
    | Wrapper for the Canion executable  that is part of the Curves+ software suite. 

    Args:        
        input_avg_path (str): Trajectory or PDB input file. File type: input. Accepted formats: trj (edam:format_3910), pdb (edam:format_1476).
        input_top_path (str) (Optional): Topology file, needed along with .trj file (optional). File type: input. Accepted formats: top (edam:format_3881).
        output_cda_path (str): Filename for Curves+ output .cda file. File type: output. Accepted formats: cda (edam:format_2330).
        output_lis_path (str): Filename for Curves+ output .lis file. File type: output. Accepted formats: lis (edam:format_2330).
        output_zip_path (str) (Optional): Filename for .zip files containing Curves+ output that is not .cda or .lis files. File type: output. Accepted formats: zip (edam:format_3987).
        properties (dict):
            * **bases** (*str*) - (None) sequence of bases to be searched for in the I/P data (default is blank, meaning no specified sequence). 
            * **type** (*str*) - ('K+') Ions (or atoms) to be analyzed. Options are 'Na+', 'K', 'K+', 'Cl', 'Cl-', 'CL', 'P', 'C1*', 'NH1', 'NH2', 'NZ', '1' for all cations, '-1' for all anions, '0' for neutral species or '*' for all available data.
            * **dlow** (*float*) - (0) Select starting segment of the oglimer to analyze. If both dhig and dlow are 0, entire oglimer is analyzed.
            * **dhig** (*float*) - (0) Select ending segment of the oglimer to analyze, being the maximum value the total number of base pairs in the oligomer. If both dhig and dlow are 0, entire oglimer is analyzed.
            * **rlow** (*float*) - (0) Minimal distances from the helical axis taken into account in the analysis.
            * **rhig** (*float*) - (0) Maximal distances from the helical axis taken into account in the analysis.
            * **alow** (*float*) - (0) Minimal angle range to analyze.
            * **ahig** (*float*) - (0) Maximal angle range to analyze.
            * **canion_exec** (*str*) - (Canion) Path to Canion executable, otherwise the program wil look for Canion executable in the binaries folder.
    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.curvesplus.biobb_canion import canion
            prop = { 
                'type': 'K+'
            }
            canion(
                input=,
                properties=prop)
    Info:
        * wrapped_software:
            * name: Canion
            * version: >=2.6
            * license: BSD 3-Clause
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(
            self, input_struc_path, output_lis_path,
            output_cda_path, output_zip_path=None,
            input_top_path=None, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_struc_path': input_struc_path,
                'input_top_path': input_top_path
            },
            'out': {
                'output_lis_path': output_lis_path,
                'output_cda_path': output_cda_path,
                'output_zip_path': output_zip_path
            }
        }

        # Properties specific for BB
        self.s1range = properties.get('s1range', None)
        self.curves_exec = properties.get('curves_exec', 'Cur+')
        self.stdlib_path = properties.get('stdlib_path', None)
        self.s2range = properties.get('s2range', None)
        self.itst = properties.get('itst', 0)
        self.itnd = properties.get('itnd', 0)
        self.itdel = properties.get('itdel', 1)
        self.ions = properties.get('ions', '.f.')
        self.test = properties.get('test', '.f.')
        self.line = properties.get('line', '.f.')
        self.fit = properties.get('fit', '.f.')
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
        """Execute the :class:`Canion <biobb_dna.curvesplus.biobb_canion.Canion>` object."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Check the properties
        fu.check_properties(self, self.properties)

        if self.s1range is None:
            raise ValueError("property 's1range' must be specified!")
        if self.s2range is None:
            # compute s2range if not provided
            range1_end = int(self.s1range.split(":")[1])
            s2start = range1_end + 1
            s2end = 2 * range1_end
            self.s2range = f"{s2end}:{s2start}"

        # check standard library files location if not provided
        if self.stdlib_path is None:
            if os.getenv("CONDA_PREFIX", False):
                curves_aux_path = Path(
                    os.getenv("CONDA_PREFIX")) / ".curvesplus"
                # check if .curvesplus directory is in $CONDA_PREFIX
                if curves_aux_path.exists():
                    if len(list(curves_aux_path.glob("standard_*.lib"))) != 3:
                        raise FileNotFoundError(
                            "One or all standard library files "
                            f"missing from {curves_aux_path}! "
                            "Check files standard_b.lib, "
                            "standard_s.lib and standard_i.lib exist.")
                    self.stdlib_path = curves_aux_path / "standard"
                else:
                    raise FileNotFoundError(
                        ".curvesplus directory not found in "
                        f"{os.getenv('CONDA_PREFIX')} !"
                        "Please indicate where standard_*.lib files are "
                        "located with the stdlib_path property.")
            else:
                # CONDA_PREFIX undefined
                self.stdlib_path = Path.cwd() / "standard"

        # Restart
        if self.restart:
            output_file_list = [
                self.io_dict['out']['output_lis_path'],
                self.io_dict['out']['output_cda_path'],
                self.io_dict['out']['output_zip_path']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' %
                       self.step, out_log, self.global_log)
                return 0

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir(prefix="curves_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        # copy input files to temporary folder
        shutil.copy(self.io_dict['in']['input_struc_path'], self.tmp_folder)
        tmp_struc_input = Path(self.io_dict['in']['input_struc_path']).name
        if self.io_dict['in']['input_top_path'] is not None:
            shutil.copy(self.io_dict['in']['input_top_path'], self.tmp_folder)
            tmp_top_input = Path(self.io_dict['in']['input_top_path']).name

        # change directory to temporary folder
        original_directory = os.getcwd()
        os.chdir(self.tmp_folder)

        # create intructions
        instructions = [
            f"{self.canion_exec} <<! ",
            "&inp",
            f"  lis=canion_output,",
            f"  axfrm={input_avg_struc},"
            f"  dat={input_cdi_file},",
            f"  solute={input_avg_struc},",
            f"  dlow={self.dlow},",
            f"  dhig={self.dhig},",
            f"  type={self.type},",
            f"  rlow={self.rlow},",
            f"  rhig={self.rhig},"]
        if self.bases is not None:
            # add topology file if needed
            fu.log('Appending sequence of bases to be searched to command',
                   out_log, self.global_log)
            instructions.append(f"  seq={self.bases},")
        instructions.append([
            "&end",
            "!"])
        cmd = ["\n".join(instructions)]

        fu.log('Creating command line with instructions and required arguments',
               out_log, self.global_log)
        # Launch execution
        returncode = cmd_wrapper.CmdWrapper(
            cmd, out_log, err_log, self.global_log).launch()

        # change back to original directory
        os.chdir(original_directory)

        # create zipfile and write output inside
        if self.io_dict["out"]["output_zip_path"] is not None:
            zf = zipfile.ZipFile(
                Path(self.io_dict["out"]["output_zip_path"]),
                "w")
            for curves_outfile in Path(self.tmp_folder).glob("curves_output*"):
                if curves_outfile.suffix not in (".cda", ".lis"):
                    zf.write(
                        curves_outfile,
                        arcname=curves_outfile.name)
            zf.close()

        # rename cda and lis files
        (Path(self.tmp_folder) / "curves_output.cda").rename(
            self.io_dict["out"]["output_cda_path"])
        (Path(self.tmp_folder) / "curves_output.lis").rename(
            self.io_dict["out"]["output_lis_path"])

        # Remove temporary file(s)
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)

        return returncode


def canion(
        input_struc_path: str, output_lis_path: str, output_cda_path: str,
        input_top_path: str = None, output_zip_path: str = None,
        properties: dict = None, **kwargs) -> int:
    """Create :class:`Canion <biobb_dna.curvesplus.biobb_canion.Canion>` class and
    execute the :meth:`launch() <biobb_dna.curvesplus.biobb_canion.Canion.launch>` method."""

    return Canion(
        input_struc_path=input_struc_path,
        input_top_path=input_top_path,
        output_lis_path=output_lis_path,
        output_cda_path=output_cda_path,
        output_zip_path=output_zip_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Execute Cur+ form the Curves+ software suite.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_struc_path', required=True,
                               help='Trajectory or PDB input file. Accepted formats: trj, pdb.')
    required_args.add_argument('--output_cda_path', required=True,
                               help='Filename to give to output .cda file. Accepted formats: str.')
    required_args.add_argument('--output_lis_path', required=True,
                               help='Filename to give to output .lis file. Accepted formats: str.')
    parser.add_argument('--input_top_path', required=False,
                        help='Topology file, needed along with .trj file (optional). Accepted formats: top.')
    parser.add_argument('--output_zip_path', required=False,
                        help='Filename to give to output files (except .cda and .lis files). Accepted formats: str.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    canion(
        input_struc_path=args.input_struc_path,
        input_top_path=args.input_top_path,
        output_cda_path=args.output_cda_path,
        output_lis_path=args.output_lis_path,
        output_zip_path=args.output_zip_path,
        properties=properties)


if __name__ == '__main__':
    main()