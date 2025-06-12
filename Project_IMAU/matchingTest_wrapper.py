import matplotlib.pyplot as plt
import matchingTest as mt

library_files = ["massLibrPE.csv", "massLibrPET.csv", "massLibrPP.csv", "massLibrPS.csv", "massLibrPVC.csv"]
plastics = ["PE","PET","PP","PS","PVC"]
sample_files = ["data_files\\peak_0.csv"]

results = {}
for i in sample_files:
    results[i] = []
    for j in library_files:
        results[i].append(mt.main(libFile=j,sampleFile=i))

print(results)

for i in results:
    plt.figure(i)
    plt.pie(results[i], labels=plastics)
plt.show()