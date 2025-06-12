#!/usr/bin/python

#to match 2 files or libraries
#last update 8.8.2019
from FngClass import massSpec
import numpy as np
from FngClass import Fingeprint
import random
import math
import pandas as pd

def main(libFile, sampleFile):
	# libFile = "massLibrPE.csv"
	# sampleFile = pd.read_csv("park-R11.csv") # wrote by hanne for csv
	# print(sampleFile)

	#"Sample_DB1-1A.csv"

	mStart = 100
	mStop = 1000
	tolerance = 0.005 		#tolerance in m/z
	ranged = 30		#how many ions to consider 10, 20 or 40
	loops = 1000			#number of sintettic spectra 1000
	array1 = []
	array2 = []
	array3 = []
	array4 = []


	msL = massSpec()
	msL.toleranceMZ = tolerance
	msL.set (libFile)
	msL.subset(mStart, mStop)
	msL.highestN(msL.mzSub, msL.specSub, ranged)
	msL.normalise(msL.mzH, msL.specH)

	maxima = np.mean(msL.specH)#takes the mean for the log random sepctra
	#print msL.specH
	#print ("maxima" + str(maxima))
	#ms = np.random.lognormal(np.log(maxima),1,ranged)c
	#print ms


	for i in range (loops):
		ms = []
		ms1 = []#added to normalise to the highest
		ms2 = []


		#generating random numbers (lognormal distributed)
		ms = np.random.lognormal(np.log(maxima),1,ranged)

		f = Fingeprint()
		f.tol1 = tolerance

		#normalise to the highest missing i other progs

		high = max(ms)#the highest elemet
		for t1 in ms:
			ms1.append(float(t1*100/high))

		f.calculate(msL.mzNhigh, msL.specNhigh, msL.mzNhigh, ms1)
		array1.append(f.match)
		array2.append(f.match2)

		#normalising ms[] to the sum
		sum1 = float(np.sum(ms))
		#print sum1
		for t1 in ms:
			ms2.append(float(t1*100/sum1))
			#print float(t1*100/sum1)
		#print ms2

		f.calculate(msL.mzNsum, msL.specNsum, msL.mzNsum, ms2)
		array3.append(f.match)
		array4.append(f.match2)

		#f.plott()

	x=np.mean(array1)
	y=np.std(array1,ddof=1)
	w=np.mean(array2)
	z=np.std(array2,ddof=1)

	x2=np.mean(array3)
	y2=np.std(array3,ddof=1)
	w2=np.mean(array4)
	z2=np.std(array4,ddof=1)


	print("The match is " , x, " +/- ", y)
	print("Identification from ", x+y*2)
	print("The match2 is " , w, " +/- ", z)
	print("Identification from ", w+z*2)
	print("The match is " , x2, " +/- ", y2)
	print("Identification from ", x2+y2*2)
	print("The match2 is " , w2, " +/- ", z2)
	print("Identification from ", w2+z2*2)



	#calculating the mathc to the file
	ms2 = massSpec()
	ms2.toleranceMZ = tolerance
	ms2.set(sampleFile)
	ms2.subset(mStart, mStop)
	ms2.match(msL.mzH)#use matchS instead of match() for strict results (ignores zeto mz due to the no unified list
	#ms2.highestN(ms2.mzSub, ms2.specSub, 40)
	#print ms2.mzSub2
	#print ms2.specSub2

	#ms2.quantify()
	ms2.quant(0.08,8,.5)#flow [l/min], integration time [min], load [mL]
	print(("ng/mL => " + str(ms2.ng)))
	ms2.normalise(ms2.mzSub2, ms2.specSub2)

	#print msL.mzH


	f2 = Fingeprint()
	f2.calculate(msL.mzNhigh, msL.specNhigh, ms2.mzNhigh, ms2.specNhigh)

	#corrected quantificaiton
	f2.quant(0.08,8,.5, ms2.specSub2, ms2.mzSub2)#seems good odred of matched mz
	print(("ng/mL corr=> " + str(f2.ng)))
	corr_ng = f2.ng

	#print len(f2.ng_corr_fact)
	#print msL.mzNhigh
	#print len(ms2.mzSub2)
	#print len(f2.mz)
	#print len(f2.diff)

	a = f2.match
	b = f2.match2

	#cuantificatin correction

	#ms2.quant2(0.06,8,1.5,f2.ng_corr_fact)#flow [l/min], integration time [min], load [mL]
	#print ("ng/mL corr => " + str(ms2.ng))

	#
	#f2.plott()
	#print (f2.diff)

	print("Alg. 1 " , a)
	print("Alg. 2 " , b)

	f2.calculate(msL.mzNsum, msL.specNsum, ms2.mzNsum, ms2.specNsum)
	c = f2.match
	d = f2.match2
	#corrected quantificaiton
	#f2.quant(0.06,8,1.5, ms2.specSub2, ms2.mzSub2)
	#print ("ng/mL corr=> " + str(f2.ng))
	#print len(ms2.mzSub2)
	#print len(f2.ng_corr_fact)


	print("Alg. 3 " , c)
	print("Alg. 4 " , d)

	print("\n")
	if a > x+y*4:
		print("Algorithm 1: MATCH ! (***) confidence")
	elif a>x+y*3:
		print("Algorithm 1: MATCH ! (**) confidence")
	elif a>x+y*2:
		print("Algorithm 1: MATCH ! (*) confidence")
	else:
		print("Algorithm 1: no match")


	if b > w+z*4:
		print("Algorithm 2: MATCH ! (***) confidence")
	elif b>w+z*3:
		print("Algorithm 2: MATCH ! (**) confidence")
	elif b>w+z*2:
		print("Algorithm 2: MATCH ! (*) confidence")
	else:
		print("Algorithm 2: no match")


	if c > x2+y2*4:
		print("Algorithm 3: MATCH ! (***) confidence")
	elif c>x2+y2*3:
		print("Algorithm 3: MATCH ! (**) confidence")
	elif c>x2+y2*2:
		print("Algorithm 3: MATCH ! (*) confidence")
	else:
		print("Algorithm 3: no match")


	if d > w2+z2*4:
		print("Algorithm 4: MATCH ! (***) confidence")
	elif d>w2+z2*3:
		print("Algorithm 4: MATCH ! (**) confidence")
	elif d>w2+z2*2:
		print("Algorithm 4: MATCH ! (*) confidence")
	else:
		print("Algorithm 4: no match\n")


	scores_sorted = [a,b,c,d]
	scores_sorted.sort(reverse=True)#sorting to print the highest score
	print(("highest score => " + str(round(scores_sorted[0],1))))

	print(("ng/mL => " + str(round(ms2.ng,1))))
	print(("ng/mL Corr => " + str(round(corr_ng,1))))

	return round(corr_ng,1)

	#f2.plott()

if __name__=="__main__":
	main(libFile = "massLibrPE.csv",sampleFile = "WW3.csv")