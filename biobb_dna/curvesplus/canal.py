#!/usr/bin/env python3

"""Module containing the Template class and the command line interface."""
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper


class Canal():
    """
    | biobb_dna Canal
    | Wrapper for the Canal executable  that is part of the Curves+ software suite. 

    Args:        
        cda_filename (str): Input file, from Cur+ output. File type: input. Accepted formats: cda.
        seq (str) (Optional): sequence of bases to be searched for in the I/P data (default is blank, meaning no specified sequence). 
        canal_exec (str): Path to Canal executable.
        outfile (str): Filename for output files. File type: output.  Accepted formats: str.
        properties (dic):
            * **itst** (*int*) - (0) Iteration start index.
            * **itnd** (*int*) - (0) Iteration end index.
            * **itdel** (*int*) - (1) Iteration delimiter. 
            * **lev1** (*int*) - (0) Lower base level limit (i.e. base pairs) used for analysis
            * **lev2** (*int*) - (0) Upper base level limit used for analysis. If lev1 > 0 and lev2 = 0, lev2 is set to lev1 (i.e. analyze lev1 only). If lev1=lev2=0, lev1 is set to 1 and lev2 is set to the length of the oligmer (i.e. analyze all levels)
            * **nastr** (*str*) - ('NA') character string used to indicate missing data in .ser files
            * **cormin** (*float*) - (0.6) minimal absolute value for printing linear correlation coefficients between pairs of analyzed variables
            * **series** (*str*) - ('.f.') if '.t.' then O/P a spatial or time series. Only possible for the analysis of single structures or single trajectories
            * **histo** (*str*) - ('.f.') if '.t.' then O/P a histograms
            * **corr** (*str*) - ('.f.') if '.t.' than calculate linear correlation coefficients between all variables.
            * **sequence** (*list[str]*) - ([]) Sequences of the first strand of the corresponding DNA fragment, for each .cda file.
    Examples:
        This is a use example of how to use the building block from Python::
            from biobb_dna.curvesplus.canal import canal
            prop = { 
                'series': '.t.',
                'histo': '.t.',
                'sequences': ['CGCGAATTCGCG'] 
            }
            canal(
                canal_exec='/path/to/Canal/executable',
                cda_filename='/path/to/curves/output.cda',
                outfile='outfile_filename',
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

    def __init__(self, canal_exec, cda_filename, outfile, seq,
                 properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.io_dict = {
            'in': {
                'cda_filename': cda_filename,
                'seq': seq,
                'canal_exec': canal_exec
            },
            'out': {'outfile': outfile}
        }

        # Properties specific for BB
        self.nastr = properties.get('nastr', None)
        self.cormin = properties.get('cormin', 0.6)
        self.lev1 = properties.get('lev1', 0)
        self.lev2 = properties.get('lev2', 0)
        self.itst = properties.get('itst', 0)
        self.itnd = properties.get('itnd', 0)
        self.itdel = properties.get('itdel', 1)
        self.series = properties.get('series', '.f.')
        self.histo = properties.get('histo', '.f.')
        self.corr = properties.get('corr', '.f.')
        self.sequences = properties.get('sequences', [])
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
        if self.sequences == []:
            raise ValueError(
                "property 'sequences' must be specified! "
                "The number of sequences specified must match "
                "the number of .cda files.")
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

        # create intructions
        instructions = [
            f"{self.io_dict['in']['canal_exec']} <<! ",
            "&inp",
            f"  lis={self.io_dict['out']['outfile']},"]
        if self.io_dict['in']['seq'] is not None:
            # add topology file if needed
            fu.log('Appending provided topology to command',
                   out_log, self.global_log)
            instructions.append(f"  ftop={self.io_dict['in']['seq']},")
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
            "&end"]
        for cda, seq in zip(self.io_dict['in']['cda_filename'], self.sequences):
            instructions.append(
                f"{cda} {seq}")
        instructions.append("!")

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


def canal(canal_exec: str, cda_filename: str, seq: str, outfile: str = None, properties: dict = None, **kwargs) -> int:
    """Create :class:`Curves <biobb_dna.curvesplus.curves.Curves>` class and
    execute the :meth:`launch() <biobb_dna.curvesplus.curves.Curves.launch>` method."""

    return Canal(
        canal_exec=canal_exec,
        cda_filename=cda_filename,
        seq=seq,
        outfile=outfile,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Description for the template module.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--canal_exec', required=True,
                               help='Path to Canal executable.')
    required_args.add_argument('--cda_filename', required=True, nargs="+",
                               help='Trajectory or PDB input file. Accepted formats: trj, pdb.')
    parser.add_argument('--seq', required=False,
                        help='Topology file, needed along with .trj file (optional). Accepted formats: top.')
    required_args.add_argument('--outfile', required=True,
                               help='Filename to give to output .lis files (without the .lis extension). Accepted formats: str.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    canal(
        canal_exec=args.canal_exec,
        cda_filename=args.cda_filename,
        seq=args.seq,
        outfile=args.outfile,
        properties=properties)


if __name__ == '__main__':
    main()
