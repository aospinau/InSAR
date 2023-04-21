#%%

import contextlib
import csv
from datetime import datetime
from getpass import getpass
import h5py
import os
from pathlib import Path
import re
import rioxarray as rxr
from tqdm.notebook import tqdm
from typing import Union
import urllib
import xarray as xr
import zipfile
import shutil

from ipyfilechooser import FileChooser

import numpy as np

# diff behavior based on mintpy <= 1.4.1 or > 1.4.1
from importlib.metadata import version as getVersion
from packaging import version as compareVersion
isLatest = compareVersion.parse(getVersion('mintpy')) > compareVersion.parse('1.4.1')

# MintPy ver beyond 1.4.1
if isLatest:
    from mintpy.cli import view, tsview, plot_network, plot_transection, plot_coherence_matrix
# MintPy <= 1.4.1 (old)
else:
    import mintpy.view as view
    import mintpy.tsview as tsview
    import mintpy.plot_network as plot_network
    import mintpy.plot_transection as plot_transection
    import mintpy.plot_coherence_matrix as plot_coherence_matrix

import mintpy.plot_coherence_matrix
from osgeo import gdal, osr

import rasterio
from rasterio.transform import from_origin

import mintpy.objects.insar_vs_gps
import mintpy.utils

import opensarlab_lib as asfn
#%%
path = Path.cwd()
fc = FileChooser(path)
display(fc)
#%%
# define the work directory
work_path = Path(fc.selected_path)
print(f"Work directory: {work_path}")

# define a project name
proj_name = input("Prueba3")

# define the MintPy time-series directory
mint_path = work_path/'MintPy'
mint_path.mkdir(exist_ok=True)
print(f"MintPy directory: {mint_path}")

#create a directory in which to store plots
plot_path = mint_path/"plots"
plot_path.mkdir(exist_ok=True)
#%%

#%%

ts_demErr=mint_path/'timeseries_ERA5_demErr.h5'

%matplotlib widget
tsview.main([str(ts_demErr), 
                    f'-d={mint_path}/inputs/geometryGeo.h5', 
                    f'-o={mint_path}/displacement_ts', 
                    f'--outfile={mint_path}/displacement_ts.pdf'])
# %%
