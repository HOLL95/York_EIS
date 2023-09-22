from EIS_class import EIS
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
import pints
path=os.getcwd().split("/")

filename="csv_example.csv"
file_idx=path.index("Standalone_EIS")


data_loc=("/").join(path[:file_idx+1]+["Data", filename])
   
header=6
footer=2
pd_data=read_csv(data_loc, sep=",", encoding="utf-16", engine="python", skiprows=header, skipfooter=footer)
data=pd_data.to_numpy(copy=True, dtype='float')
real=np.flip(data[:,3])
imag= -np.flip(data[:,4])
spectra=np.column_stack((real,imag))
frequencies=np.flip(data[:,0])

model={"z1":"R0", "z2":{"p_1":("Q1", "alpha1"),"p_2":["R1", "W1"]}}
#     |-----CPE1-----| 
#--R0-               |     
#     | ---R1---W1---|
names=["R0", "W1", "R1", "Q1", "alpha1"]#Parameter names

boundaries={"R0":[0, 1e4,],
            "R1":[1e-6, 1e6], 
            "Q1":[0,2], 
            "alpha1":[0,1],
            "W1":[0,1e6]}#Region in which to search
sim_class=EIS(circuit=model, fitting=True, parameter_bounds=boundaries, normalise=True, parameter_names=names)
mode="bode"#Form of the data that you fit to - either bode or nyquist
data_to_fit=sim_class.convert_to_bode(spectra)#covert to phase/magnitude data
fitting_frequencies=frequencies*2*np.pi#normalise frequencies
sim_class.options["data_representation"]=mode

cmaes_problem=pints.MultiOutputProblem(sim_class, fitting_frequencies,data_to_fit)#define the fitting problem
best=1e12#arbitarily large number
score = pints.SumOfSquaresError(cmaes_problem)#Score function
lower_bound=[0 for x in names]#For CMAES, everything is normalised between 0 and 1
upper_bound=[1 for x in names]#
num_fit_repeats=3
for j in range(0, num_fit_repeats):
    CMAES_boundaries=pints.RectangularBoundaries(lower_bound, upper_bound)
    random_init=list(abs(np.random.rand(sim_class.n_parameters())))#random starting location
    cmaes_fitting=pints.OptimisationController(score, random_init, sigma0=None, boundaries=CMAES_boundaries, method=pints.CMAES)
    cmaes_fitting.set_max_unchanged_iterations(iterations=200, threshold=1e-7)

    cmaes_fitting.set_parallel(True)

    found_params, found_value=cmaes_fitting.run()   
    if found_value<best:
        found_parameters=found_params
        best=found_value

real_params=sim_class.change_norm_group(dict(zip(names, found_parameters)), "un_norm", return_type="dict")
print(real_params)
sim_data=sim_class.test_vals(real_params, fitting_frequencies)
fig, ax=plt.subplots()
twinx=ax.twinx()
EIS().bode(data_to_fit, frequencies, ax=ax, twinx=twinx, data_type="phase_mag")
EIS().bode(sim_data, frequencies,ax=ax, twinx=twinx, data_type="phase_mag")
           
plt.show()

    

