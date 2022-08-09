# Readme for read_nc.py


### Requires libraries pandas and scipy ###

### Place read_nc.py in a directory containing a folder named "nc_files" (see tree below)

## Directory structure:
│   readme.txt
│   read_nc.py
│
├───nc_files
│       cami_0000-09-01_64x128_L26_c030918.nc
│       ECMWF_ERA-40_subset.nc
│       madis-hydro.nc
│       madis-mesonet.nc
│       madis-metar.nc
│       madis-raob.nc
│       madis-sao.nc
│       tos_O1_2001-2002.nc
│
└───xyz_files
        madis-hydro_xyz.csv


### Processed files are written to /xyz_files/

## change dir
cd /d path/to/read_nc.py

## run script
python read_nc.py

From here follow instructions...
