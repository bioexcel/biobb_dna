#!/usr/bin/env python3

"""Module containing the Canion class and the command line interface."""
import os
import zipfile
import argparse
import shutil
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger


class Canion(BiobbObject):
    """
    | biobb_dna Canion
    | Wrapper for the Canion executable  that is part of the Curves+ software suite. 

    Args:        
        input_cdi_path (str): Trajectory input file. File type: input. `Sample file <https://mmb.irbbarcelona.org/biobb-dev/biobb-api/public/samples/THGA_K.cdi>`_. Accepted formats: cdi (edam:format_2330).
        input_afr_path (str): Helical axis frames corresponding to the input conformation to be analyzed. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/curvesplus/THGA.afr>`_. Accepted formats: afr (edam:format_2330).
        input_avg_struc_path (str): Average DNA conformation. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/curvesplus/THGA_avg.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_zip_path (str) (Optional): Filename for .zip files containing Canion output files. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/curvesplus/canion_output.zip>`_. Accepted formats: zip (edam:format_3987).
        properties (dict):
            * **bases** (*str*) - (None) Sequence of bases to be analyzed (default is blank, meaning no specified sequence). 
            * **type** (*str*) - ('*') Ions (or atoms) to be analyzed. Options are 'Na+', 'K', 'K+', 'Cl', 'Cl-', 'CL', 'P', 'C1*', 'NH1', 'NH2', 'NZ', '1' for all cations, '-1' for all anions, '0' for neutral species or '*' for all available data.
            * **dlow** (*float*) - (0) Select starting segment of the oglimer to analyze. If both dhig and dlow are 0, entire oglimer is analyzed.
            * **dhig** (*float*) - (0) Select ending segment of the oglimer to analyze, being the maximum value the total number of base pairs in the oligomer. If both dhig and dlow are 0, entire oglimer is analyzed.
            * **rlow** (*float*) - (0) Minimal distances from the helical axis taken into account in the analysis.
            * **rhig** (*float*) - (0) Maximal distances from the helical axis taken into account in the analysis.
            * **alow** (*float*) - (0) Minimal angle range to analyze.
            * **ahig** (*float*) - (360) Maximal angle range to analyze.
            * **itst** (*int*) - (None) Number of first snapshot to be analyzed.
            * **itnd** (*int*) - (None) Number of last snapshot to be analyzed.
            * **itdel** (*int*) - (None) Spacing between analyzed snapshots.
            * **rmsf** (*bool*) - (False) If set to True uses the combination of the helical ion parameters and an average helical axis to map the ions into Cartesian space and then calculates their average position (pdb output) and their root mean square fluctuation values (rmsf output). A single pass rmsf algorithm to make this calculation possible with a single read of the trajectory file. This option is generally used for solute atoms and not for solvent molecules or ions.
            * **circ** (*bool*) - (False) If set to True, minicircles are analyzed.
            * **canion_exec** (*str*) - (Canion) Path to Canion executable, otherwise the program wil look for Canion executable in the binaries folder.
    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_dna.curvesplus.biobb_canion import biobb_canion
            prop = { 
                'type': 'K+',
                'bases': 'G'
            }
            biobb_canion(
                input_cdi_path='/path/to/input.cdi',
                input_afr_path='/path/to/input.afr',
                input_avg_struc_path='/path/to/input.pdb',
                output_zip_path='/path/to/output.zip',
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
            self, input_cdi_path, input_afr_path, input_avg_struc_path,
            output_zip_path=None, properties=None, **kwargs) -> None:
        properties = properties or {}
        super().__init__(properties)

        # Input/Output files
        self.io_dict = {
            'in': {
                'input_cdi_path': input_cdi_path,
                'input_afr_path': input_afr_path,
                'input_avg_struc_path': input_avg_struc_path,
            },
            'out': {
                'output_zip_path': output_zip_path
            }
        }

        # Properties specific for BB
        self.canion_exec = properties.get('canion_exec', 'Canion')
        self.bases = properties.get('bases', None)
        self.type = properties.get('type', '*')
        self.dlow = properties.get('dlow', 0)
        self.dhig = properties.get('dhig', 0)
        self.rlow = properties.get('rlow', 0)
        self.rhig = properties.get('rhig', 0)
        self.alow = properties.get('alow', 0)
        self.ahig = properties.get('ahig', 360)
        self.itst = properties.get('itst', None)
        self.itnd = properties.get('itnd', None)
        self.itdel = properties.get('itdel', None)
        self.rmsf = properties.get('rmsf', '.f.')
        self.circ = properties.get('circ', '.f.')
        self.properties = properties

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`Canion <biobb_dna.curvesplus.biobb_canion.Canion>` object."""

        # Check the properties
        fu.check_properties(self, self.properties)

        ion_type_options = [
            'Na+',
            'K',
            'K+',
            'Cl',
            'Cl-',
            'CL',
            'P',
            'C1*',
            'NH1',
            'NH2',
            'NZ',
            '1',
            '-1',
            '0',
            '*'
        ]
        if self.type not in ion_type_options:
            raise ValueError(("Invalid value for property type! "
                              f"Option include: {ion_type_options}"))

        # Creating temporary folder
        self.tmp_folder = fu.create_unique_dir(prefix="canion_")
        fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)

        # copy input files to temporary folder
        shutil.copy(self.io_dict['in']['input_cdi_path'], self.tmp_folder)
        shutil.copy(self.io_dict['in']['input_afr_path'], self.tmp_folder)
        shutil.copy(
            self.io_dict['in']['input_avg_struc_path'], self.tmp_folder)
        input_cdi_file = Path(self.io_dict['in']['input_cdi_path']).name
        input_afr_file = Path(self.io_dict['in']['input_afr_path']).name
        input_avg_struc = Path(self.io_dict['in']['input_avg_struc_path']).name

        # change directory to temporary folder
        original_directory = os.getcwd()
        os.chdir(self.tmp_folder)

        # create intructions
        instructions = [
            f"{self.canion_exec} <<! ",
            "&inp",
            "  lis=canion_output,",
            f"  dat={input_cdi_file[:-4]},",
            f"  axfrm={input_afr_file[:-4]},",
            f"  solute={input_avg_struc[:-4]},",
            f"  type={self.type},",
            f"  dlow={self.dlow},",
            f"  dhig={self.dhig},",
            f"  rlow={self.rlow},",
            f"  rhig={self.rhig},",
            f"  alow={self.alow},",
            f"  ahig={self.ahig},"]
        if self.bases is not None:
            # add topology file if needed
            fu.log('Appending sequence of bases to be searched to command',
                   self.out_log, self.global_log)
            instructions.append(f"  seq={self.bases},")
        instructions.append("&end")
        instructions.append("!")
        self.cmd = ["\n".join(instructions)]

        fu.log('Creating command line with instructions and required arguments',
               self.out_log, self.global_log)
        # Run Biobb block
        self.run_biobb()

        # change back to original directory
        os.chdir(original_directory)

        # create zipfile and write output inside
        zf = zipfile.ZipFile(
            Path(self.io_dict["out"]["output_zip_path"]),
            "w")
        for curves_outfile in Path(self.tmp_folder).glob("canion_output*"):
            zf.write(curves_outfile, arcname=curves_outfile.name)
        zf.close()

        # Remove temporary file(s)
        if self.remove_tmp:
            self.tmp_files.append(self.tmp_folder)
            self.remove_tmp_files()

        return self.return_code


def biobb_canion(
        input_cdi_path: str, input_afr_path: str, input_avg_struc_path: str,
        output_zip_path: str = None, properties: dict = None, **kwargs) -> int:
    """Create :class:`Canion <biobb_dna.curvesplus.biobb_canion.Canion>` class and
    execute the :meth:`launch() <biobb_dna.curvesplus.biobb_canion.Canion.launch>` method."""

    return Canion(
        input_cdi_path=input_cdi_path,
        input_afr_path=input_afr_path,
        input_avg_struc_path=input_avg_struc_path,
        output_zip_path=output_zip_path,
        properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description='Execute Canion form the Curves+ software suite.',
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_cdi_path', required=True,
                               help='Ion position data file. Accepted formats: cdi.')
    required_args.add_argument('--input_afr_path', required=True,
                               help='Helical axis frames data. Accepted formats: afr.')
    required_args.add_argument('--input_avg_struc_path', required=True,
                               help='Average DNA conformation fike file. Accepted formats: pdb.')
    parser.add_argument('--output_zip_path', required=False,
                        help='Filename to give to output files. Accepted formats: zip.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    biobb_canion(
        input_cdi_path=args.input_cdi_path,
        input_afr_path=args.input_afr_path,
        input_avg_struc_path=args.input_avg_struc_path,
        output_zip_path=args.output_zip_path,
        properties=properties)


if __name__ == '__main__':
    main()
