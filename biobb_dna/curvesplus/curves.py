#!/usr/bin/env python3

"""Module containing the Template class and the command line interface."""
import os
import argparse
import shutil
from platform import system as platform_system
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper


class Curves():
    """
    | biobb_dna Curves
    | Wrapper for the Cur+ executable  that is part of the Curves+ software suite. 

    Args:        
        filename (str): Trajectory or PDB input file. File type: input. `Sample file <https://urlto.sample>`_. Accepted formats: trj (edam:format_3910), pdb (edam:format_1476).
        ftop (str) (Optional): Topology file, needed along with .trj file (optional). File type: input. `Sample file <https://urlto.sample>`_. Accepted formats: top (edam:format_3881).
        curves_exec (str): Path to Cur+ executable.
        outfile (str): Filename for output .lis files. File type: output. `Sample file <https://urlto.sample>`_. Accepted formats: str.
        properties (dic):
            * **stdlib_path** (*path*) - (None) Path to Curves' standard library files for nucleotides.
            * **itst** (*int*) - (0) Iteration start index.
            * **itnd** (*int*) - (0) Iteration end index.
            * **itdel** (*int*) - (1) Iteration delimiter. 
            * **ions** (*bool*) - (False) If True, helicoidal analysis of ions (or solvent molecules) around solute is carried out.
            * **s1range** (*str*) - (None) Range of first strand. Must be specified in the form "start:end". 
            * **s2range** (*str*) - (None) Range of second strand. Must be specified in the form "start:end".
    Examples:
        This is a use example of how to use the building block from Python::
            from biobb_template.template.template import template
            prop = { 
                'boolean_property': True 
            }
            template(input_file_path1='/path/to/myTopology.top',
                    output_file_path='/path/to/newCompressedFile.zip',
                    input_file_path2='/path/to/mytrajectory.dcd',
                    properties=prop)
    Info:
        * wrapped_software:
            * name: Curves
            * version: >=2.6
            * license: BSD 3-Clause
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, curves_exec, filename, outfile, ftop=None,
                 properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': {
                'filename': filename,
                'ftop': ftop,
                'curves_exec': curves_exec
            },
            'out': {'outfile': outfile}
        }

        # Properties specific for BB
        self.itst = properties.get('itst', 0)
        self.itnd = properties.get('itnd', 0)
        self.itdel = properties.get('itdel', 1)
        self.ions = properties.get('ions', '.f.')
        self.s1range = properties.get('s1range', None)
        self.s2range = properties.get('s2range', None)
        self.stdlib_path = properties.get('stdlib_path', None)
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
        """Execute the :class:`Template <template.template.Template>` object."""

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Check the properties
        fu.check_properties(self, self.properties)
        if self.stdlib_path is None:
            raise ValueError("property 'stdlib_path' must be specified!")
        if self.s1range is None:
            raise ValueError("property 's1range' must be specified!")
        if self.s2range is None:
            raise ValueError("property 's2range' must be specified!")

        # Restart
        if self.restart:
            output_file_list = [self.io_dict['out']['outfile']]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' %
                       self.step, out_log, self.global_log)
                return 0

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        shutil.copy(self.io_dict['in']['filename'], self.tmp_folder)
        if self.io_dict['in']['ftop'] is not None:
            shutil.copy(self.io_dict['in']['ftop'], self.tmp_folder)

        # If platform is Darwin (MacOS) then set dylib environment variable
        set_envvar = []
        if platform_system().lower() == "darwin":
            # AMBERHOME environment variable must exist
            # since it was part of the installation
            envpath = os.getenv("AMBERHOME")
            set_envvar = [f"export DYLD_LIBRARY_PATH='{envpath}/lib';"]

        # create intructions
        instructions = [
            f"{self.io_dict['in']['curves_exec']} <<! ",
            "&inp",
            f"  file={self.io_dict['in']['filename']},"]
        if self.io_dict['in']['ftop'] is not None:
            # add topology file if needed
            fu.log('Appending provided topology to command',
                   out_log, self.global_log)
            instructions.append(f"  ftop={self.io_dict['in']['ftop']},")

        instructions = set_envvar + instructions + [
            f"  lis={self.io_dict['out']['outfile']},",
            f"  lib={self.stdlib_path},",
            f"  ions={self.ions},",
            f"  itst={self.itst},itnd={self.itnd},itdel={self.itdel},",
            "&end",
            "2 1 -1 0 0",
            f"{self.s1range}",
            f"{self.s2range}",
            "!"
        ]
        cmd = ["\n".join(instructions)]
        fu.log('Creating command line with instructions and required arguments',
               out_log, self.global_log)
        # Launch execution
        returncode = cmd_wrapper.CmdWrapper(
            cmd, out_log, err_log, self.global_log).launch()

        # Remove temporary file(s)
        if self.remove_tmp:
            fu.rm(self.tmp_folder)
            fu.log('Removed: %s' % str(self.tmp_folder), out_log)

        return returncode


def curves(curves_exec: str, filename: str, ftop: str, outfile: str = None, properties: dict = None, **kwargs) -> int:
    """Create :class:`Curves <biobb_dna.curvesplus.curves.Curves>` class and
    execute the :meth:`launch() <biobb_dna.curvesplus.curves.Curves.launch>` method."""

    return Curves(
        curves_exec=curves_exec,
        filename=filename,
        ftop=ftop,
        outfile=outfile,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Description for the template module.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--curves_exec', required=True,
                               help='Path to Curves+ executable.')
    required_args.add_argument('--filename', required=True,
                               help='Trajectory or PDB input file. Accepted formats: trj, pdb.')
    parser.add_argument('--ftop', required=False,
                        help='Topology file, needed along with .trj file (optional). Accepted formats: top.')
    required_args.add_argument('--outfile', required=True,
                               help='Filename to give to output .lis files (without the .lis extension). Accepted formats: str.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    curves(
        curves_exec=args.curves_exec,
        filename=args.filename,
        ftop=args.ftop,
        outfile=args.outfile,
        properties=properties)


if __name__ == '__main__':
    main()
