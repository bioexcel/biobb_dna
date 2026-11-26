#!/usr/bin/env python3

"""Module containing the Canion class and the command line interface."""
import os
import zipfile
from typing import Optional
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu


class Canion(BiobbObject):
    """
    | biobb_dna Canion
    | Wrapper for the Canion executable  that is part of the Curves+ software suite.
    | Analyzes the trajectory of ions around a DNA molecule.

    Args:
        input_cdi_path (str): Trajectory input file. File type: input. `Sample file <https://github.com/bioexcel/biobb_dna/releases/download/assets/THGA_K.cdi>`_. Accepted formats: cdi (edam:format_2330).
        input_afr_path (str): Helical axis frames corresponding to the input conformation to be analyzed. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/curvesplus/THGA.afr>`_. Accepted formats: afr (edam:format_2330).
        input_avg_struc_path (str): Average DNA conformation. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/curvesplus/THGA_avg.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_zip_path (str): Filename for .zip files containing Canion output files. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/curvesplus/canion_output.zip>`_. Accepted formats: zip (edam:format_3987).
        properties (dict):
            * **bases** (*str*) - (None) Sequence of bases to be analyzed (default is blank, meaning no specified sequence).
            * **type** (*str*) - ('*') Ions (or atoms) to be analyzed. Options are 'Na+', 'K', 'K+', 'Cl', 'Cl-', 'CL', 'P', 'C1*', 'NH1', 'NH2', 'NZ', '1' for all cations, '-1' for all anions, '0' for neutral species or '*' for all available data.
            * **dlow** (*float*) - (0) Select starting segment of the oglimer to analyze. If both dhig and dlow are 0, entire oglimer is analyzed.
            * **dhig** (*float*) - (0) Select ending segment of the oglimer to analyze, being the maximum value the total number of base pairs in the oligomer. If both dhig and dlow are 0, entire oglimer is analyzed.
            * **rlow** (*float*) - (0) Minimal distances from the helical axis taken into account in the analysis.
            * **rhig** (*float*) - (0) Maximal distances from the helical axis taken into account in the analysis.
            * **alow** (*float*) - (0) Minimal angle range to analyze.
            * **ahig** (*float*) - (360) Maximal angle range to analyze.
            * **itst** (*int*) - (0) Number of first snapshot to be analyzed.
            * **itnd** (*int*) - (0) Number of last snapshot to be analyzed.
            * **itdel** (*int*) - (1) Spacing between analyzed snapshots.
            * **rmsf** (*bool*) - (False) If set to True uses the combination of the helical ion parameters and an average helical axis to map the ions into Cartesian space and then calculates their average position (pdb output) and their root mean square fluctuation values (rmsf output). A single pass rmsf algorithm to make this calculation possible with a single read of the trajectory file. This option is generally used for solute atoms and not for solvent molecules or ions.
            * **circ** (*bool*) - (False) If set to True, minicircles are analyzed.
            * **binary_path** (*str*) - ("Canion") Path to Canion executable, otherwise the program wil look for Canion executable in the binaries folder.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
            * **container_path** (*str*) - (None)  Path to the binary executable of your container.
            * **container_image** (*str*) - ("cmip/cmip:latest") Container Image identifier.
            * **container_volume_path** (*str*) - ("/data") Path to an internal directory in the container.
            * **container_working_dir** (*str*) - (None) Path to the internal CWD in the container.
            * **container_user_id** (*str*) - (None) User number id to be mapped inside the container.
            * **container_shell_path** (*str*) - ("/bin/bash") Path to the binary executable of the container shell.
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
            self, input_cdi_path: str, input_afr_path: str, input_avg_struc_path: str,
            output_zip_path: Optional[str] = None, properties: Optional[dict] = None, **kwargs) -> None:
        super().__init__(**locals())

        # Properties specific for BB
        self.rmsf = ".t." if self.rmsf else ".f."
        self.circ = ".t." if self.circ else ".f."

    def run(self) -> None:
        """Execute the :class:`Canion <biobb_dna.curvesplus.biobb_canion.Canion>` object."""

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

        # define temporary file names
        input_cdi_file = Path(self.stage_io_dict['in']['input_cdi_path']).name
        input_afr_file = Path(self.stage_io_dict['in']['input_afr_path']).name
        input_avg_struc = Path(self.stage_io_dict['in']['input_avg_struc_path']).name

        # change directory to temporary folder
        original_directory = os.getcwd()

        os.chdir(self.stage_io_dict.get("unique_dir", ""))

        # create intructions
        instructions = [
            f"{self.binary_path} <<! ",
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
            f"  ahig={self.ahig},",
            f"  itst={self.itst},",
            f"  itnd={self.itnd},",
            f"  itdel={self.itdel},",
            f"  rmsf={self.rmsf},",
            f"  circ={self.circ},"]
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

        workdir = self.stage_io_dict.get("unique_dir", "")

        # create zipfile and write output inside
        with zipfile.ZipFile(self.sandbox_file("output_zip_path"), "w") as zf:
            for curves_outfile in Path(workdir).glob("canion_output*"):
                fu.log(f"Adding {curves_outfile} to zip file", self.out_log, self.global_log)
                if curves_outfile.suffix != ".zip":
                    zf.write(
                        curves_outfile,
                        arcname=curves_outfile.name)


biobb_canion = launcher(Canion)

if __name__ == '__main__':
    Canion.main()
