#!/usr/bin/env python3

"""Utility functions to load files."""
import zipfile
from pathlib import Path

import pandas as pd


def read_series(input_serfile, usecols=None):
    """Read .ser file"""
    extra_kwargs = dict(
        header=None,
        sep='\s+',
        index_col=0)
    ser_data = pd.read_csv(input_serfile, **extra_kwargs)
    if usecols is not None:
        if 0 in usecols:
            usecols.pop(usecols.index(0))
        ser_data = ser_data[[i+1 for i in usecols]]
    return ser_data


def load_data(data_filename, inner_file=None):
    """Read .csv file directly or from inside a .zip file."""
    if Path(data_filename).suffix == ".zip":
        zf = zipfile.ZipFile(data_filename, "r")
        # use provided data filename of look for csv file
        if inner_file is not None:
            dataset = zf.open(inner_file)
        else:
            print(
                "inner file name not provided, "
                "using first .csv file found inside .zip.")
            for fn in zf.infolist():
                if fn.filename.endswith(".csv"):
                    dataset = zf.open(fn)
                    break
    elif Path(data_filename).suffix == ".csv":
        dataset = data_filename
    else:
        raise IOError("input file extension must be .zip or .csv!")
    data = pd.read_csv(dataset, index_col=0)
    return data
