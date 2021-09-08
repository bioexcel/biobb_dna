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

## Averages
Load .ser file for a given helical parameter and read each column corresponding to a base calculating average over each one.
### Get help
Command:
```python
averages -h
```
    Traceback (most recent call last):
      File "/opt/anaconda3/envs/curves_env/bin/averages", line 33, in <module>
        sys.exit(load_entry_point('biobb-dna', 'console_scripts', 'averages')())
      File "/opt/anaconda3/envs/curves_env/bin/averages", line 25, in importlib_load_entry_point
        return next(matches).load()
    StopIteration
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
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_averages.yml)
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
averages --config config_averages.yml --input_ser_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_averages.json)
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
averages --config config_averages.json --input_ser_path input.ser --output_csv_path output.csv --output_jpg_path output.jpg
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
* **input_filename_shift** (*string*): Path to .csv file with data for helical parameter 'shift'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_slide** (*string*): Path to .csv file with data for helical parameter 'slide'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_rise** (*string*): Path to .csv file with data for helical parameter 'rise'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_tilt** (*string*): Path to .csv file with data for helical parameter 'tilt'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_roll** (*string*): Path to .csv file with data for helical parameter 'roll'. File type: input. [Sample file](None). Accepted formats: CSV
* **input_filename_twist** (*string*): Path to .csv file with data for helical parameter 'twist'. File type: input. [Sample file](None). Accepted formats: CSV
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

## Bimodality
Determine binormality/bimodality from a helical parameter series dataset.
### Get help
Command:
```python
bimodality -h
```
    Traceback (most recent call last):
      File "/opt/anaconda3/envs/curves_env/bin/bimodality", line 33, in <module>
        sys.exit(load_entry_point('biobb-dna', 'console_scripts', 'bimodality')())
      File "/opt/anaconda3/envs/curves_env/bin/bimodality", line 25, in importlib_load_entry_point
        return next(matches).load()
    StopIteration
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
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_bimodality.yml)
```python
properties:
  confidence_level: 5.0
  helpar_name: shift
  max_iter: 400
  tol: 1.0e-05

```
#### Command line
```python
bimodality --config config_bimodality.yml --input_csv_file input.csv --input_zip_file input.zip --output_csv_path output.csv --output_jpg_path output.jpg
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_dna/blob/master/biobb_dna/test/data/config/config_bimodality.json)
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
bimodality --config config_bimodality.json --input_csv_file input.csv --input_zip_file input.zip --output_csv_path output.csv --output_jpg_path output.jpg
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
