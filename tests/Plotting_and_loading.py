from EIS_class import EIS
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
path=os.getcwd().split("/")

files=["txt_example.txt", "csv_example.csv"]
file_idx=path.index("York_EIS")
fig, ax=plt.subplots(1,2)#one row, two columns
for filename in files:
    data_loc=("/").join(path[:file_idx+1]+["Data", filename])
    if ".txt" in filename:
        header=0#header length
        data=np.loadtxt(data_loc, skiprows=header)
        real=np.flip(data[:,0])#real data, flipped to make lowest frequency first
        imag=np.flip(data[:,1])#imag data - be careful, sometimes EIS software flips the true value by -1
        spectra=np.column_stack((real, imag))#To plot, the data has to have two columns of 1:real and 2: imaginary data
        frequency=np.flip(data[:,2])
        #everything with a keyword (x=y) has a default argument, but have explained what each one does
        #BODE PLOT
        EIS().bode(spectra, frequency, 
                    ax=ax[0],#plotting axis,
                    twinx=ax[0].twinx(),#the twinned axis that allows for plotting phase and magnitude on the same axis
                    label=filename,#label to appear in legend,
                    data_type="complex",#Assumes real/imag data by default - if it's in a 1: phase 2:magnitude format, this argument should be 'phase_mag'
                    compact_labels=True,#plots symbols for phase and magnitude, if False it'll be text
                    lw=1.5,#Width of the plotted line
                    scatter=1,#If not False, then the number is for how many scatter points - 2 for example would be every other frequency
                    line=True,#If False will just plot scatter points,
                    alpha=1,#Degree of transparancy between 0 and 1
                    colour="black",)
    elif ".csv" in filename:
        header=6
        footer=2
        pd_data=read_csv(data_loc, sep=",", encoding="utf-16", engine="python", skiprows=header, skipfooter=footer)
        data=pd_data.to_numpy(copy=True, dtype='float')
        real=np.flip(data[:,3])
        imag= -np.flip(data[:,4])
        spectra=np.column_stack((real,imag))

        frequencies=np.flip(data[:,0])
        #NYQUIST PLOT
        EIS().nyquist(spectra, #No frequencies in a nyquist plot
                    ax=ax[1],#plotting axis,
                    label=filename,#label to appear in legend,
                    data_type="complex",#Assumes real/imag data by default - if it's in a 1: phase 2:magnitude format, this argument should be 'phase_mag'
                    marker="o",#If scatter points, then the type of marker
                    linestyle="-",#Style of solid line
                    lw=1.5,#Width of the plotted line
                    scatter=1,#If not False, then the number is for how many scatter points - 2 for example would be every other frequency
                    line=True,#If False will just plot scatter points
                    alpha=1,#Degree of transparancy between 0 and 1
                    orthonormal=False,#Fixes the axes to be the same if True
                    colour="black",)
#show the legends
ax[0].legend()
ax[1].legend()
plt.show()

    

