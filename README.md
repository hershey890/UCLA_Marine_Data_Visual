# UCLA_Marine_Data_Visual

Data visualization application/GUI in development in python for the Marine Operations Program at UCLA. Used to depict Ocean temperature along with GPS data ovelayed on a map. Check out the UCLA Marine Operations Program for which this was developed at: https://dept.atmos.ucla.edu/marineops


## Setup
To setup your environment to run this program, you must first install the following python packages: matplotlib, and cartopy. If you already have any of these installed you can just skip that step. Be patient, as installing some of these packages can take some time. Everytime conda asks you to Proceed([y]/n)?, type in yes (read the prompt it gives you and only follow this within reason). An internet connection is required for the setup.
1. Make sure you have python installed first
2. Install conda (specifically minoconda, although anaconda also works, it just takes longer to install and has unneeded packages) from https://conda.io/miniconda.html. 
3. Open anaconda
4. Install matplotlib
```
# only the first time...
conda install conda-build

# the Python version you want a package for...
set CONDA_PY=3.5

# builds the package, using a clean build environment
conda build ci\conda_recipe

# install the new package
conda install --use-local matplotlib
```
5. Install cartopy
```
conda install -c conda-forge cartopy
```


Addmittedly, there are a lot of steps involved with setting up your environment to run this program, but it allows for the most rapid development of this software.