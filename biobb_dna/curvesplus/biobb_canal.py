#!/usr/bin/env python3

"""Module containing the Canal class and the command line interface."""
import os
import zipfile
from typing import Optional
from pathlib import Path

from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu


class Canal(BiobbObject):
    """
    | biobb_dna Canal
    | Wrapper for the Canal executable that is part of the Curves+ software suite.
    | The Canal program is used to analyze the curvature of DNA structures.

    Args:
        input_cda_file (str): Input cda file, from Cur+ output. File type: input. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/curvesplus/curves_output.cda>`_. Accepted formats: cda (edam:format_2330).
        input_lis_file (str) (Optional): Input lis file, from Cur+ output. File type: input. Accepted formats: lis (edam:format_2330).
        output_zip_path (str): zip filename for output files. File type: output. `Sample file <https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/curvesplus/canal_output.zip>`_. Accepted formats: zip (edam:format_3987).
        properties (dic):
            * **bases** (*str*) - (None) sequence of bases to be searched for in the I/P data (default is blank, meaning no specified sequence).
            * **itst** (*int*) - (0) Iteration start index.
            * **itnd** (*int*) - (0) Iteration end index.
            * **itdel** (*int*) - (1) Iteration delimiter.
            * **lev1** (*int*) - (0) Lower base level limit (i.e. base pairs) used for analysis.
            * **lev2** (*int*) - (0) Upper base level limit used for analysis. If lev1 > 0 and lev2 = 0, lev2 is set to lev1 (i.e. analyze lev1 only). If lev1=lev2=0, lev1 is set to 1 and lev2 is set to the length of the oligmer (i.e. analyze all levels).
            * **nastr** (*str*) - (None) character string used to indicate missing data in .ser files. If not set, the tool uses its own default.
            * **cormin** (*float*) - (0.6) minimal absolute value for printing linear correlation coefficients between pairs of analyzed variables.
            * **series** (*bool*) - (False) if True then output spatial or time series data. Only possible for the analysis of single structures or single trajectories.
            * **histo** (*bool*) - (False) if True then output histogram data.
            * **corr** (*bool*) - (False) if True than output linear correlation coefficients between all variables.
            * **sequence** (*str*) - (None) sequence of the first strand of the corresponding DNA fragment, for each .cda file. If not given it will be parsed from .lis file.
            * **binary_path** (*str*) - ('Canal') Path to Canal executable, otherwise the program wil look for Canal executable in the binaries folder.
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

            from biobb_dna.curvesplus.biobb_canal import biobb_canal
            prop = {
                'series': 'True',
                'histo': 'True',
                'sequence': 'CGCGAATTCGCG'
            }
            biobb_canal(
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
        super().__init__(**locals())

        # Properties specific for BB
        self.series = ".t." if self.series else ".f."
        self.histo = ".t." if self.histo else ".f."
        self.corr = ".t." if self.corr else ".f."

    def run(self) -> None:
        """Execute the :class:`Canal <biobb_dna.curvesplus.biobb_canal.Canal>` object."""

        if self.sequence is None:
            if self.stage_io_dict['in']['input_lis_file'] is None:
                raise RuntimeError(
                    "if no sequence is passed in the configuration, "
                    "you must at least specify `input_lis_file` "
                    "so sequence can be parsed from there")
            lis_lines = Path(
                self.stage_io_dict['in']['input_lis_file']).read_text().splitlines()
            for line in lis_lines:
                if line.strip().startswith("Strand  1"):
                    self.sequence = line.split(" ")[-1]
                    fu.log(
                        f"using sequence {self.sequence} "
                        f"from {self.stage_io_dict['in']['input_lis_file']}",
                        self.out_log)

        # define temporary file name
        if self.container_path:
            tmp_cda_path = Path(self.container_working_dir).joinpath(Path(self.stage_io_dict['in']['input_cda_file']).name)
        else:
            tmp_cda_path = Path(self.stage_io_dict['in']['input_cda_file']).name

        # change directory to temporary folder
        original_directory = os.getcwd()

        os.chdir(self.stage_io_dict.get("unique_dir", ""))

        # create intructions
        instructions = [
            f"{self.binary_path} <<! ",
            "&inp",
            "  lis=canal_output,"]
        if self.bases is not None:
            # add topology file if needed
            fu.log('Appending sequence of bases to be searched to command',
                   self.out_log, self.global_log)
            instructions.append(f"  seq={self.bases},")
        if self.nastr is not None:
            # add topology file if needed
            fu.log('Adding null values string specification to command',
                   self.out_log, self.global_log)
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
            for canal_outfile in Path(workdir).glob("canal_output*"):
                fu.log(f"Adding {canal_outfile} to zip file", self.out_log, self.global_log)
                if canal_outfile.suffix != ".zip":
                    zf.write(
                        canal_outfile,
                        arcname=canal_outfile.name)


def biobb_canal(
        input_cda_file: str,
        output_zip_path: str,
        input_lis_file: Optional[str] = None,
        properties: Optional[dict] = None,
        **kwargs) -> int:
    """Create :class:`Canal <biobb_dna.curvesplus.biobb_canal.Canal>` class and
    execute the :meth:`launch() <biobb_dna.curvesplus.biobb_canal.Canal.launch>` method."""
    return Canal(**dict(locals())).launch()


biobb_canal.__doc__ = Canal.__doc__
main = Canal.get_main(biobb_canal, "Execute Canal from the Curves+ software suite.")


if __name__ == '__main__':
    main()
