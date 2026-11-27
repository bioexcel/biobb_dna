# Biobb Analysis changelog

## [Unreleased]

## What's new in version [5.4.0](https://github.com/bioexcel/biobb_dna/releases/tag/v5.4.0)?

### Changes

* [UPDATE] Update to biobb_common 5.4.0.
* [FIX] `basepair_stiffness`: the `scaling` values are no longer truncated to integers. The default `10.6` of tilt, roll and twist was applied as `10`, so their stiffness values change.
* [FIX] `interseqcorr` and `intraseqcorr`: the angular parameters (roll, tilt, twist, buckle, ...) are correlated with the circular method and the others with Pearson; the two methods were swapped.
* [FIX] `dna_averages`: the backbone torsions (alphaC, betaW, ...) work, with one value per nucleotide; they failed with an `AttributeError`.
* [FIX] `biobb_curves`: `output_zip_path` is optional, as documented.
* [FIX] `dna_timeseries_unzip`: `output_list_path` is optional, as documented.
* [FIX] `biobb_curves`, `biobb_canal` and `biobb_canion` run in containers: they changed the host working directory to the container's `container_working_dir`.
* [FIX] `bipopulations` no longer prints debug output.
* [DOCS] `dna_timeseries`: the `stride` property documents its default (10).
* [UPDATE] Python 3.11 to 3.13.

## What's new in version [5.3.0](https://github.com/bioexcel/biobb_amber/releases/tag/v5.3.0)?

### Changes

* [UPDATE] Update to biobb_common 5.3.1

## What's new in version [5.2.1](https://github.com/bioexcel/biobb_amber/releases/tag/v5.2.1)?

### Changes

* [UPDATE] Update to biobb_common 5.2.2

## What's new in version [5.2.0](https://github.com/bioexcel/biobb_amber/releases/tag/v5.2.0)?

### Changes

* [UPDATE] Update to biobb_common 5.2.0

## What's new in version [5.1.0](https://github.com/bioexcel/biobb_dna/releases/tag/v5.1.0)?

### Changes

* [UPDATE]: Update to biobb_common 5.1.0

## What's new in version [5.0.1](https://github.com/bioexcel/biobb_dna/releases/tag/v5.0.1)?

### Changes

* [FIX](all): Accept lists in different formats on input properties.

## What's new in version [5.0.0](https://github.com/bioexcel/biobb_dna/releases/tag/v5.0.0)?

### Changes

* [FIX] Bug fixes in seqpos of dna timeseries
* [UPDATE] Adding sandbox_path property to the json schemas

## What's new in version [4.2.4](https://github.com/bioexcel/biobb_dna/releases/tag/v4.2.4)?
In version 4.2.4 some bugs in Canion and Curves have been fixed. Added two new tools: CanalUnzip and DnaTimeseriesUnzip.

### New features

* Bug fixes in Canion and Curves (curvesplus)
* New CanalUnzip tool (curvesplus)
* New DnaTimeseriesUnzip tool (dna)

## What's new in version [4.2.2](https://github.com/bioexcel/biobb_dna/releases/tag/v4.2.2)?
In version 4.2.2 a bug in HelParBimodality has been fixed.

### New features

* Bug fix in HelParBimodality (dna)

## What's new in version [4.2.1](https://github.com/bioexcel/biobb_dna/releases/tag/v4.2.1)?
In version 4.2.1 the dependency curves+ has been updated to 3.0.2 version.

### New features

* Update to curves+ 3.0.2 (curvesplus)

## What's new in version [4.2.0](https://github.com/bioexcel/biobb_dna/releases/tag/v4.2.0)?
In version 4.2.0 the dependency biobb_common has been updated to 4.2.0 version.

### New features

* Update to biobb_common 4.2.0 (general)

## What's new in version [4.1.0](https://github.com/bioexcel/biobb_dna/releases/tag/v4.1.0)?
In version 4.1.0 the dependency biobb_common has been updated to 4.1.0 version.

### New features

* Update to biobb_common 4.1.0 (general)

## What's new in version [4.0.0](https://github.com/bioexcel/biobb_dna/releases/tag/v4.0.0)?
In version 4.0.0 the dependency biobb_common has been updated to 4.0.0 version.

### New features

* Update to biobb_common 4.0.0 (general)

## What's new in version [3.9.0](https://github.com/bioexcel/biobb_dna/releases/tag/v3.9.0)?
In version 3.9.0 the dependency biobb_common has been updated to 3.9.0 version.

### New features

* Update to biobb_common 3.9.0 (general)
* All inputs/outputs are checked for correct file format, extension and type (general)

## What's new in version [3.8.2](https://github.com/bioexcel/biobb_dna/releases/tag/v3.8.2)?
In version 3.8.2 the some dependencies have been updated for the sake of having compatibility woth other BioBB packages.

### New features

* Updated dependencies (general)

## What's new in version [3.8.1](https://github.com/bioexcel/biobb_dna/releases/tag/v3.8.1)?
In version 3.8.1 the some dependencies have been updated for the sake of having compatibility woth other BioBB packages.

### New features

* Updated dependencies (general)

## What's new in version [3.8.0](https://github.com/bioexcel/biobb_dna/releases/tag/v3.8.0)?
In version 3.8.0 the dependency biobb_common has been updated to 3.8.1 version.

### New features

* Update to biobb_common 3.8.1 (general)

## What's new in version [3.7.0](https://github.com/bioexcel/biobb_dna/releases/tag/v3.7.0)?
In version 3.7.0 the dependency biobb_common has been updated to 3.7.0 version.

### New features

* Update to biobb_common 3.7.0 (general)