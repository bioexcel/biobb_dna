# BioBB DNA Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Average_stiffness
Calculate average stiffness constants for each base pair of a trajectory's series.
### Get help
Command:
```python
average_stiffness -h
```
    /bin/sh: average_stiffness: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_ser_path** (*string*): Path to .ser file for helical parameter. File is expected to be a table, with the first column being an index and the rest the helical parameter values for each base/basepair. File type: input. [Sample file](None). Accepted formats: SER
* **output_csv_path** (*string*): Path to .csv file where output is saved. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to .jpg file where output is saved. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **KT** (*number*): (0.592186827) Value of Boltzmann temperature factor..
* **sequence** (*string*): (None) Nucleic acid sequence corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *usecols* option)..
* **helpar_name** (*string*): (None) helical parameter name..
* **seqpos** (*array*): (None) list of sequence positions to analyze. If not specified it will analyse the complete sequence..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_average_stiffness.yml)
```python
properties:
  sequence: CGCGAATTCGCG

```
#### Command line
```python
average_stiffness --config config_average_stiffness.yml --input_ser_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_average_stiffness.json)
```python
{
  "properties": {
    "sequence": "CGCGAATTCGCG"
  }
}
```
#### Command line
```python
average_stiffness --config config_average_stiffness.json --input_ser_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```

## Basepair_stiffness
Calculate stiffness constants matrix between all six helical parameters for a single base pair step.
### Get help
Command:
```python
basepair_stiffness -h
```
    /bin/sh: basepair_stiffness: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_filename_shift** (*string*): Path to csv file with data for helical parameter 'shift'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_slide** (*string*): Path to csv file with data for helical parameter 'slide'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_rise** (*string*): Path to csv file with data for helical parameter 'rise'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_tilt** (*string*): Path to csv file with data for helical parameter 'tilt'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_roll** (*string*): Path to csv file with data for helical parameter 'roll'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_twist** (*string*): Path to csv file with data for helical parameter 'twist'. File type: input. [Sample file](None). Accepted formats: CSV
* **output_csv_path** (*string*): Path to directory where stiffness matrix file is saved as a csv file. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to directory where stiffness heatmap image is saved as a jpg file. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **KT** (*number*): (0.592186827) Value of Boltzmann temperature factor..
* **scaling** (*array*): ([1, 1, 1, 10.6, 10.6, 10.6]) Values by which to scale stiffness. Positions correspond to helical parameters in the order: shift, slide, rise, tilt, roll, twist..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_basepair_stiffness.yml)
```python
properties:
  remove_tmp: false

```
#### Command line
```python
basepair_stiffness --config config_basepair_stiffness.yml --input_filename_shift input.csv --input_filename_slide input.csv --input_filename_rise input.csv --input_filename_tilt input.csv --input_filename_roll input.csv --input_filename_twist input.csv --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_basepair_stiffness.json)
```python
{
  "properties": {
    "remove_tmp": false
  }
}
```
#### Command line
```python
basepair_stiffness --config config_basepair_stiffness.json --input_filename_shift input.csv --input_filename_slide input.csv --input_filename_rise input.csv --input_filename_tilt input.csv --input_filename_roll input.csv --input_filename_twist input.csv --output_csv_path output.csv --output_jpg_path output.jpg
```

## Biobb_canal
Wrapper for the Canal executable that is part of the Curves+ software suite.
### Get help
Command:
```python
biobb_canal -h
```
    /bin/sh: biobb_canal: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_cda_file** (*string*): Input cda file, from Cur+ output. File type: input. [Sample file](None). Accepted formats: CDA
* **input_lis_file** (*string*): (Optional) Input lis file, from Cur+ output. File type: input. [Sample file](None). Accepted formats: LIS
* **output_zip_path** (*string*): zip filename for output files. File type: output. [Sample file](None). Accepted formats: ZIP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **bases** (*string*): (None) sequence of bases to be searched for in the I/P data (default is blank, meaning no specified sequence)..
* **itst** (*integer*): (0) Iteration start index..
* **itnd** (*integer*): (0) Iteration end index..
* **itdel** (*integer*): (1) Iteration delimiter..
* **lev1** (*integer*): (0) Lower base level limit (i.e. base pairs) used for analysis..
* **lev2** (*integer*): (0) Upper base level limit used for analysis. If lev1 > 0 and lev2 = 0, lev2 is set to lev1 (i.e. analyze lev1 only). If lev1=lev2=0, lev1 is set to 1 and lev2 is set to the length of the oligmer (i.e. analyze all levels)..
* **nastr** (*string*): (NA) character string used to indicate missing data in .ser files..
* **cormin** (*number*): (0.6) minimal absolute value for printing linear correlation coefficients between pairs of analyzed variables..
* **series** (*string*): (False) if True then output spatial or time series data. Only possible for the analysis of single structures or single trajectories..
* **histo** (*string*): (False) if True then output histogram data..
* **corr** (*string*): (False) if True than output linear correlation coefficients between all variables..
* **sequence** (*string*): (Optional) sequence of the first strand of the corresponding DNA fragment, for each .cda file. If not given it will be parsed from .lis file..
* **canal_exec** (*string*): (Canal) Path to Canal executable, otherwise the program wil look for Canal executable in the binaries folder..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_biobb_canal.yml)
```python
properties:
  sequence: CGCGAATTCGCG
  series: true

```
#### Command line
```python
biobb_canal --config config_biobb_canal.yml --input_cda_file input.cda --input_lis_file input.lis --output_zip_path output.zip
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_biobb_canal.json)
```python
{
  "properties": {
    "series": true,
    "sequence": "CGCGAATTCGCG"
  }
}
```
#### Command line
```python
biobb_canal --config config_biobb_canal.json --input_cda_file input.cda --input_lis_file input.lis --output_zip_path output.zip
```

## Biobb_curves
Wrapper for the Cur+ executable  that is part of the Curves+ software suite.
### Get help
Command:
```python
biobb_curves -h
```
    /bin/sh: biobb_curves: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_struc_path** (*string*): Trajectory or PDB input file. File type: input. [Sample file](None). Accepted formats: TRJ, PDB
* **input_top_path** (*string*): Topology file, needed along with .trj file (optional). File type: input. [Sample file](None). Accepted formats: TOP
* **output_cda_path** (*string*): Filename for Curves+ output .cda file. File type: output. [Sample file](None). Accepted formats: CDA
* **output_lis_path** (*string*): Filename for Curves+ output .lis file. File type: output. [Sample file](None). Accepted formats: LIS
* **output_zip_path** (*string*): Filename for .zip files containing Curves+ output that is not .cda or .lis files. File type: output. [Sample file](None). Accepted formats: ZIP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **s1range** (*string*): (None) Range of first strand. Must be specified in the form "start:end"..
* **s2range** (*string*): (None) Range of second strand. Must be specified in the form "start:end"..
* **stdlib_path** (*string*): (standard) Path to Curves' standard library files for nucleotides. If not specified will look for 'standard' files in current directory..
* **itst** (*integer*): (0) Iteration start index..
* **itnd** (*integer*): (0) Iteration end index..
* **itdel** (*integer*): (1) Iteration delimiter..
* **ions** (*boolean*): (False) If True, helicoidal analysis of ions (or solvent molecules) around solute is carried out..
* **curves_exec** (*string*): (Cur+) Path to Curves+ executable, otherwise the program wil look for Cur+ executable in the binaries folder..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_biobb_curves.yml)
```python
properties:
  s1range: '1:12'

```
#### Command line
```python
biobb_curves --config config_biobb_curves.yml --input_struc_path input.trj --input_top_path input.top --output_cda_path output.cda --output_lis_path output.lis --output_zip_path output.zip
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_biobb_curves.json)
```python
{
  "properties": {
    "s1range": "1:12"
  }
}
```
#### Command line
```python
biobb_curves --config config_biobb_curves.json --input_struc_path input.trj --input_top_path input.top --output_cda_path output.cda --output_lis_path output.lis --output_zip_path output.zip
```

## Bipopulations
Calculate BI/BII populations from epsilon and zeta parameters.
### Get help
Command:
```python
bipopulations -h
```
    /bin/sh: bipopulations: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_epsilC_path** (*string*): Path to .ser file for helical parameter 'epsilC'. File type: input. [Sample file](None). Accepted formats: SER
* **input_epsilW_path** (*string*): Path to .ser file for helical parameter 'epsilW'. File type: input. [Sample file](None). Accepted formats: SER
* **input_zetaC_path** (*string*): Path to .ser file for helical parameter 'zetaC'. File type: input. [Sample file](None). Accepted formats: SER
* **input_zetaW_path** (*string*): Path to .ser file for helical parameter 'zetaW'. File type: input. [Sample file](None). Accepted formats: SER
* **output_csv_path** (*string*): Path to .csv file where output is saved. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to .jpg file where output is saved. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **sequence** (*string*): (None) Nucleic acid sequence corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option)..
* **seqpos** (*array*): ((None) ) list of sequence positions to analyze. If not specified it will analyse the complete sequence..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_bipopulations.yml)
```python
properties:
  sequence: CGCGAATTCGCG

```
#### Command line
```python
bipopulations --config config_bipopulations.yml --input_epsilC_path input.ser --input_epsilW_path input.ser --input_zetaC_path input.ser --input_zetaW_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_bipopulations.json)
```python
{
  "properties": {
    "sequence": "CGCGAATTCGCG"
  }
}
```
#### Command line
```python
bipopulations --config config_bipopulations.json --input_epsilC_path input.ser --input_epsilW_path input.ser --input_zetaC_path input.ser --input_zetaW_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```

## Canonicalag
Calculate Canonical Alpha/Gamma populations from alpha and gamma parameters.
### Get help
Command:
```python
canonicalag -h
```
    /bin/sh: canonicalag: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_alphaC_path** (*string*): Path to .ser file for helical parameter 'alphaC'. File type: input. [Sample file](None). Accepted formats: SER
* **input_alphaW_path** (*string*): Path to .ser file for helical parameter 'alphaW'. File type: input. [Sample file](None). Accepted formats: SER
* **input_gammaC_path** (*string*): Path to .ser file for helical parameter 'gammaC'. File type: input. [Sample file](None). Accepted formats: SER
* **input_gammaW_path** (*string*): Path to .ser file for helical parameter 'gammaW'. File type: input. [Sample file](None). Accepted formats: SER
* **output_csv_path** (*string*): Path to .csv file where output is saved. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to .jpg file where output is saved. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **sequence** (*string*): (None) Nucleic acid sequence corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option)..
* **seqpos** (*array*): (None) list of sequence positions to analyze. If not specified it will analyse the complete sequence..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_canonicalag.yml)
```python
properties:
  sequence: CGCGAATTCGCG

```
#### Command line
```python
canonicalag --config config_canonicalag.yml --input_alphaC_path input.ser --input_alphaW_path input.ser --input_gammaC_path input.ser --input_gammaW_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_canonicalag.json)
```python
{
  "properties": {
    "sequence": "CGCGAATTCGCG"
  }
}
```
#### Command line
```python
canonicalag --config config_canonicalag.json --input_alphaC_path input.ser --input_alphaW_path input.ser --input_gammaC_path input.ser --input_gammaW_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```

## Dna_averages
Load .ser file for a given helical parameter and read each column corresponding to a base calculating average over each one.
### Get help
Command:
```python
dna_averages -h
```
    /bin/sh: dna_averages: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_ser_path** (*string*): Path to .ser file for helical parameter. File is expected to be a table, with the first column being an index and the rest the helical parameter values for each base/basepair. File type: input. [Sample file](None). Accepted formats: SER
* **output_csv_path** (*string*): Path to .csv file where output is saved. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to .jpg file where output is saved. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **sequence** (*string*): (None) Nucleic acid sequence corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option)..
* **helpar_name** (*string*): (Optional) helical parameter name..
* **stride** (*integer*): (1000) granularity of the number of snapshots for plotting time series..
* **seqpos** (*array*): (None) list of base pairs (columns indices) to use..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_dna_averages.yml)
```python
properties:
  seqpos:
  - 4
  - 5
  - 6
  sequence: CGCGAATTCGCG
  stride: 1

```
#### Command line
```python
dna_averages --config config_dna_averages.yml --input_ser_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_dna_averages.json)
```python
{
  "properties": {
    "sequence": "CGCGAATTCGCG",
    "seqpos": [
      4,
      5,
      6
    ],
    "stride": 1
  }
}
```
#### Command line
```python
dna_averages --config config_dna_averages.json --input_ser_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```

## Dna_bimodality
Determine binormality/bimodality from a helical parameter series dataset.
### Get help
Command:
```python
dna_bimodality -h
```
    /bin/sh: dna_bimodality: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_csv_file** (*string*): Path to .csv file with helical parameter series. If `input_zip_file` is passed, this should be just the filename of the .csv file inside .zip. File type: input. [Sample file](None). Accepted formats: CSV
* **input_zip_file** (*string*): (Optional) .zip file containing the `input_csv_file` .csv file. File type: input. [Sample file](None). Accepted formats: ZIP
* **output_csv_path** (*string*): Path to .csv file where output is saved. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to .jpg file where output is saved. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **helpar_name** (*string*): (Optional) helical parameter name..
* **confidence_level** (*number*): (5.0) Confidence level for Byes Factor test (in percentage)..
* **max_iter** (*integer*): (400) Number of maximum iterations for EM algorithm..
* **tol** (*number*): (1e-05) Tolerance value for EM algorithm..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist.1.
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_dna_bimodality.yml)
```python
properties:
  confidence_level: 5.0
  helpar_name: shift
  max_iter: 400
  tol: 1.0e-05

```
#### Command line
```python
dna_bimodality --config config_dna_bimodality.yml --input_csv_file input.csv --input_zip_file input.zip --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_dna_bimodality.json)
```python
{
  "properties": {
    "helpar_name": "shift",
    "confidence_level": 5.0,
    "max_iter": 400,
    "tol": 1e-05
  }
}
```
#### Command line
```python
dna_bimodality --config config_dna_bimodality.json --input_csv_file input.csv --input_zip_file input.zip --output_csv_path output.csv --output_jpg_path output.jpg
```

## Dna_timeseries
Created time series and histogram plots for each base pair from a helical parameter series file.
### Get help
Command:
```python
dna_timeseries -h
```
    /bin/sh: dna_timeseries: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_ser_path** (*string*): Path to .ser file for helical parameter. File is expected to be a table, with the first column being an index and the rest the helical parameter values for each base/basepair. File type: input. [Sample file](None). Accepted formats: SER
* **output_zip_path** (*string*): Path to output .zip files where data is saved. File type: output. [Sample file](None). Accepted formats: ZIP
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **sequence** (*string*): (None) Nucleic acid sequence corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *usecols* option)..
* **bins** (*integer*): (None) Bins for histogram. Parameter has same options as matplotlib.pyplot.hist..
* **helpar_name** (*string*): (Optional) helical parameter name..
* **stride** (*integer*): (1000) granularity of the number of snapshots for plotting time series..
* **seqpos** (*array*): (Optional) list of sequence positions to analyze. If not specified it will analyse the complete sequence..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_dna_timeseries.yml)
```python
properties:
  seqpos:
  - 4
  - 5
  sequence: CGCGAATTCGCG

```
#### Command line
```python
dna_timeseries --config config_dna_timeseries.yml --input_ser_path input.ser --output_zip_path output.zip
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_dna_timeseries.json)
```python
{
  "properties": {
    "sequence": "CGCGAATTCGCG",
    "seqpos": [
      4,
      5
    ]
  }
}
```
#### Command line
```python
dna_timeseries --config config_dna_timeseries.json --input_ser_path input.ser --output_zip_path output.zip
```

## Interbpcorr
Calculate correlation between all base pairs of a single sequence and for a single helical parameter.
### Get help
Command:
```python
interbpcorr -h
```
    /bin/sh: interbpcorr: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_filename_shift** (*string*): Path to .ser file with data for helical parameter 'shift'. File type: input. [Sample file](None). Accepted formats: SER
* **input_filename_slide** (*string*): Path to .ser file with data for helical parameter 'slide'. File type: input. [Sample file](None). Accepted formats: SER
* **input_filename_rise** (*string*): Path to .ser file with data for helical parameter 'rise'. File type: input. [Sample file](None). Accepted formats: SER
* **input_filename_tilt** (*string*): Path to .ser file with data for helical parameter 'tilt'. File type: input. [Sample file](None). Accepted formats: SER
* **input_filename_roll** (*string*): Path to .ser file with data for helical parameter 'roll'. File type: input. [Sample file](None). Accepted formats: SER
* **input_filename_twist** (*string*): Path to .ser file with data for helical parameter 'twist'. File type: input. [Sample file](None). Accepted formats: SER
* **output_csv_path** (*string*): Path to directory where output is saved. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to .jpg file where output is saved. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **sequence** (*string*): (None) Nucleic acid sequence for the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option)..
* **seqpos** (*array*): (None) list of sequence positions to analyze. If not specified it will analyse the complete sequence..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_interbpcorr.yml)
```python
properties:
  sequence: CGCGAATTCGCG

```
#### Command line
```python
interbpcorr --config config_interbpcorr.yml --input_filename_shift input.ser --input_filename_slide input.ser --input_filename_rise input.ser --input_filename_tilt input.ser --input_filename_roll input.ser --input_filename_twist input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_interbpcorr.json)
```python
{
  "properties": {
    "sequence": "CGCGAATTCGCG"
  }
}
```
#### Command line
```python
interbpcorr --config config_interbpcorr.json --input_filename_shift input.ser --input_filename_slide input.ser --input_filename_rise input.ser --input_filename_tilt input.ser --input_filename_roll input.ser --input_filename_twist input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```

## Interhpcorr
Calculate correlation between helical parameters for a single inter-base pair.
### Get help
Command:
```python
interhpcorr -h
```
    /bin/sh: interhpcorr: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_filename_shift** (*string*): Path to .csv file with data for helical parameter 'shift'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_slide** (*string*): Path to .csv file with data for helical parameter 'slide'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_rise** (*string*): Path to .csv file with data for helical parameter 'rise'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_tilt** (*string*): Path to .csv file with data for helical parameter 'tilt'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_roll** (*string*): Path to .csv file with data for helical parameter 'roll'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_twist** (*string*): Path to .csv file with data for helical parameter 'twist'. File type: input. [Sample file](None). Accepted formats: CSV
* **output_csv_path** (*string*): Path to directory where output is saved. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to .jpg file where output is saved. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **basepair** (*string*): (None) Name of basepair analyzed..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_interhpcorr.yml)
```python
properties:
  remove_tmp: false

```
#### Command line
```python
interhpcorr --config config_interhpcorr.yml --input_filename_shift input.csv --input_filename_slide input.csv --input_filename_rise input.csv --input_filename_tilt input.csv --input_filename_roll input.csv --input_filename_twist input.csv --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_interhpcorr.json)
```python
{
  "properties": {
    "remove_tmp": false
  }
}
```
#### Command line
```python
interhpcorr --config config_interhpcorr.json --input_filename_shift input.csv --input_filename_slide input.csv --input_filename_rise input.csv --input_filename_tilt input.csv --input_filename_roll input.csv --input_filename_twist input.csv --output_csv_path output.csv --output_jpg_path output.jpg
```

## Interseqcorr
Calculate correlation between all base pairs of a single sequence and for a single helical parameter.
### Get help
Command:
```python
interseqcorr -h
```
    /bin/sh: interseqcorr: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_ser_path** (*string*): Path to .ser file with data for single helical parameter. File type: input. [Sample file](None). Accepted formats: SER
* **output_csv_path** (*string*): Path to directory where output is saved. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to .jpg file where output is saved. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **sequence** (*string*): (None) Nucleic acid sequence for the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option)..
* **helpar_name** (*string*): (None) helical parameter name..
* **seqpos** (*array*): (None) list of sequence positions to analyze. If not specified it will analyse the complete sequence..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_interseqcorr.yml)
```python
properties:
  sequence: CGCGAATTCGCG

```
#### Command line
```python
interseqcorr --config config_interseqcorr.yml --input_ser_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_interseqcorr.json)
```python
{
  "properties": {
    "sequence": "CGCGAATTCGCG"
  }
}
```
#### Command line
```python
interseqcorr --config config_interseqcorr.json --input_ser_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```

## Intrabpcorr
Calculate correlation between all intra-base pairs of a single sequence and for a single helical parameter.
### Get help
Command:
```python
intrabpcorr -h
```
    /bin/sh: intrabpcorr: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_filename_shear** (*string*): Path to .ser file with data for helical parameter 'shear'. File type: input. [Sample file](None). Accepted formats: SER
* **input_filename_stretch** (*string*): Path to .ser file with data for helical parameter 'stretch'. File type: input. [Sample file](None). Accepted formats: SER
* **input_filename_stagger** (*string*): Path to .ser file with data for helical parameter 'stagger'. File type: input. [Sample file](None). Accepted formats: SER
* **input_filename_buckle** (*string*): Path to .ser file with data for helical parameter 'buckle'. File type: input. [Sample file](None). Accepted formats: SER
* **input_filename_propel** (*string*): Path to .ser file with data for helical parameter 'propel'. File type: input. [Sample file](None). Accepted formats: SER
* **input_filename_opening** (*string*): Path to .ser file with data for helical parameter 'opening'. File type: input. [Sample file](None). Accepted formats: SER
* **output_csv_path** (*string*): Path to directory where output is saved. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to .jpg file where output is saved. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **sequence** (*string*): (None) Nucleic acid sequence for the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option)..
* **seqpos** (*array*): (None) list of sequence positions to analyze. If not specified it will analyse the complete sequence..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_intrabpcorr.yml)
```python
properties:
  sequence: CGCGAATTCGCG

```
#### Command line
```python
intrabpcorr --config config_intrabpcorr.yml --input_filename_shear input.ser --input_filename_stretch input.ser --input_filename_stagger input.ser --input_filename_buckle input.ser --input_filename_propel input.ser --input_filename_opening input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_intrabpcorr.json)
```python
{
  "properties": {
    "sequence": "CGCGAATTCGCG"
  }
}
```
#### Command line
```python
intrabpcorr --config config_intrabpcorr.json --input_filename_shear input.ser --input_filename_stretch input.ser --input_filename_stagger input.ser --input_filename_buckle input.ser --input_filename_propel input.ser --input_filename_opening input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```

## Intrahpcorr
Calculate correlation between helical parameters for a single intra-base pair.
### Get help
Command:
```python
intrahpcorr -h
```
    /bin/sh: intrahpcorr: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_filename_shear** (*string*): Path to .csv file with data for helical parameter 'shear'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_stretch** (*string*): Path to .csv file with data for helical parameter 'stretch'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_stagger** (*string*): Path to .csv file with data for helical parameter 'stagger'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_buckle** (*string*): Path to .csv file with data for helical parameter 'buckle'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_propel** (*string*): Path to .csv file with data for helical parameter 'propeller'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_opening** (*string*): Path to .csv file with data for helical parameter 'opening'. File type: input. [Sample file](None). Accepted formats: CSV
* **output_csv_path** (*string*): Path to directory where output is saved. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to .jpg file where output is saved. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **base** (*string*): (None) Name of base analyzed..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_intrahpcorr.yml)
```python
properties:
  remove_tmp: false

```
#### Command line
```python
intrahpcorr --config config_intrahpcorr.yml --input_filename_shear input.csv --input_filename_stretch input.csv --input_filename_stagger input.csv --input_filename_buckle input.csv --input_filename_propel input.csv --input_filename_opening input.csv --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_intrahpcorr.json)
```python
{
  "properties": {
    "remove_tmp": false
  }
}
```
#### Command line
```python
intrahpcorr --config config_intrahpcorr.json --input_filename_shear input.csv --input_filename_stretch input.csv --input_filename_stagger input.csv --input_filename_buckle input.csv --input_filename_propel input.csv --input_filename_opening input.csv --output_csv_path output.csv --output_jpg_path output.jpg
```

## Intraseqcorr
Calculate correlation between all intra-base pairs of a single sequence and for a single helical parameter.
### Get help
Command:
```python
intraseqcorr -h
```
    /bin/sh: intraseqcorr: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_ser_path** (*string*): Path to .ser file with data for single helical parameter. File type: input. [Sample file](None). Accepted formats: SER
* **output_csv_path** (*string*): Path to directory where output is saved. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to .jpg file where output is saved. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **sequence** (*string*): (None) Nucleic acid sequence for the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option)..
* **helpar_name** (*string*): (None) helical parameter name..
* **seqpos** (*array*): (None) list of sequence positions to analyze. If not specified it will analyse the complete sequence..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_intraseqcorr.yml)
```python
properties:
  sequence: CGCGAATTCGCG

```
#### Command line
```python
intraseqcorr --config config_intraseqcorr.yml --input_ser_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_intraseqcorr.json)
```python
{
  "properties": {
    "sequence": "CGCGAATTCGCG"
  }
}
```
#### Command line
```python
intraseqcorr --config config_intraseqcorr.json --input_ser_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```

## Puckering
Calculate Puckering from phase parameters.
### Get help
Command:
```python
puckering -h
```
    /bin/sh: puckering: command not found
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_phaseC_path** (*string*): Path to .ser file for helical parameter 'phaseC'. File type: input. [Sample file](None). Accepted formats: SER
* **input_phaseW_path** (*string*): Path to .ser file for helical parameter 'phaseW'. File type: input. [Sample file](None). Accepted formats: SER
* **output_csv_path** (*string*): Path to .csv file where output is saved. File type: output. [Sample file](None). Accepted formats: CSV
* **output_jpg_path** (*string*): Path to .jpg file where output is saved. File type: output. [Sample file](None). Accepted formats: JPG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **sequence** (*string*): (None) Nucleic acid sequence corresponding to the input .ser file. Length of sequence is expected to be the same as the total number of columns in the .ser file, minus the index column (even if later on a subset of columns is selected with the *seqpos* option)..
* **helpar_name** (*string*): (None) helical parameter name..
* **stride** (*integer*): (1000) granularity of the number of snapshots for plotting time series..
* **seqpos** (*array*): (None) list of sequence positions to analyze. If not specified it will analyse the complete sequence..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_puckering.yml)
```python
properties:
  sequence: CGCGAATTCGCG

```
#### Command line
```python
puckering --config config_puckering.yml --input_phaseC_path input.ser --input_phaseW_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_puckering.json)
```python
{
  "properties": {
    "sequence": "CGCGAATTCGCG"
  }
}
```
#### Command line
```python
puckering --config config_puckering.json --input_phaseC_path input.ser --input_phaseW_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```
