# Main Program
import os
import time

import matplotlib.pyplot as plt
from scipy.io import loadmat

from Fitness import Fitness
from GA import GA, num2str
from Norm import Norm

_HERE = os.path.dirname(os.path.abspath(__file__))

plt.close("all")
# %% Start the timer
start = time.perf_counter()

# %% User Inputs
inputs = {}
inputs["budget"] = float(input("Enter your budget: "))  # 2000 is used
Places = loadmat(os.path.join(_HERE, "Places.mat"), mat_dtype=True)["Places"]  # Istanbul Museums
inputs["data"] = Places
inputs["begin"] = inputs["data"][5, :]  # The Starting Place in the route (place 6)
inputs["ObjectFunction"] = Fitness
inputs["nPlaces"] = max(inputs["data"].shape)  # Number of places in the route (MATLAB length)

# %% The parameters used in GA
parameters = {}
parameters["nGen"] = 100  # Number of iterations (#Generations)
parameters["nRoute"] = 100  # Population size (#Routes)
parameters["pOff"] = 1  # Offsprings Percentage
parameters["pMut"] = 0.1  # Percentage related to Mutation

# %% Executing the GA
output = GA(inputs, parameters)

# %% Figures
plt.figure()
plt.plot(Norm(output["bestfit"]), "r")
plt.plot(Norm(output["bestcost"]), "g")
plt.plot(Norm(output["bestdistance"]), "b")
plt.plot(Norm(output["besttime"]), "black")
plt.xlabel("Generations")
plt.ylabel("Best Solutions")
plt.legend(["Fitness", "Cost", "Distance", "Time"], loc="upper right")
plt.grid(True)

# %% Stop the timer and display the elapsed time
elapsedTime = time.perf_counter() - start
print("Elapsed time: " + num2str(elapsedTime) + " seconds")

plt.show()
