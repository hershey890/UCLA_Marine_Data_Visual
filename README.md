# UCLA_Marine_Data_Visual

Data visualization application/GUI in development in python for the Marine Operations Program at UCLA. Used to depict Ocean temperature along with GPS data ovelayed on a map. Check out the UCLA Marine Operations Program for which this was developed at: https://dept.atmos.ucla.edu/marineops


## Setup
To setup your environment to run this program, you must first install the following python packages: matplotlib, and cartopy. If you already have any of these installed you can just skip that step. Be patient, as installing some of these packages can take some time. Everytime conda asks you to Proceed([y]/n)?, type in y (read the prompt it gives you and only follow this within reason). An internet connection is required for the setup.
1. Make sure you have python installed first
2. Install conda (specifically minoconda, although anaconda also works, it just takes longer to install and has unneeded packages) from https://conda.io/miniconda.html. 
3. Open anaconda (do not close any pop ups while anaconda is being installed as this can cause issues)
4. Check that conda.exe and python.exe are installed. If the file locations are not returned, uninstall and reinstall anaconda.exe.
In anaconda:
```
where conda
where python
```
5. Set up your anaconda environment. If you aren't running python 3.6, use whatever version you have (although you may want to update it).
```
conda create -n name_of_environment python=3.5
```
It will ask you to active the environment, in which case you must input:
```
conda activate name_of_environment
```
(to deactive an active environment, type in: conda deactivate).

6. Install cartopy
```
conda install -c conda-forge cartopy
```
7. Install an updated version of numpy
```
conda install numpy
```
8. You can now close anaconda.


Admittedly, there are a lot of steps involved with setting up your environment to run this program, but it allows for the most rapid development of this software.


### Acknowledgements:
This program was built based on matplotlib: https://matplotlib.org/users/installing.html#install-requirements, and cartopy: https://scitools.org.uk/cartopy/docs/latest/index.html