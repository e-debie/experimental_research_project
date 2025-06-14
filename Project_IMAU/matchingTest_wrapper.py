import matplotlib.pyplot as plt
import matchingTest as mt
import os

library_files = ["massLibrPE.csv", "massLibrPET.csv", "massLibrPP.csv", "massLibrPS.csv", "massLibrPVC.csv"]
plastics = ["PE","PET","PP","PS","PVC"]
sample_files = ['zeroed_files/c0_fin.csv']

results = {}
for i in sample_files:
    results[i] = []
    for j in library_files:
        results[i].append(mt.main(libFile=j,sampleFile=i))


fig, axs = plt.subplots(2, 2)
for i,j in enumerate(results):
    axs[i//2,i%2].pie(results[j], labels=plastics, autopct='%1.1f%%')
plt.show()

def get_results():
    global results
    return results
