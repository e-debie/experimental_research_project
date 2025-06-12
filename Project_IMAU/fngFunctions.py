#!/usr/bin/python

#to be used as packedge
#included quatifiction
#last update 8.8.2019

rAlg1 = [] #used to store the results of the mathc for each algorithm
rAlg2 = []
rAlg3 = []
rAlg4 = []
quant_ng = 0.0
quantC_ng = 0.0

def matchFingerprint (libFN,sampleFN,noIons,noSyntetic,mzToler):
	from FngClass import massSpec
	import numpy as np
	from FngClass import Fingeprint
	import random

	libFile = libFN
	sampleFile = sampleFN
	
	global quant_ng
	global quantC_ng

	tolerance = mzToler 		 #tolerance in m/z 0.005
	ranged = noIons				#how many ions to consider 10, 20 or 40
	loops = noSyntetic			#number of sintettic spectra 1000
	array1 = []
	array2 = []
	array3 = []
	array4 = []
	

	msL = massSpec()
	msL.toleranceMZ = tolerance
	msL.set (libFile)
	msL.subset(100, 1000)#should be 100-1000
	msL.highestN(msL.mzSub, msL.specSub, ranged)
	msL.normalise(msL.mzH, msL.specH)

	maxima = np.mean(msL.specH)#takes the mean for the log random sepctra


	for i in range (loops):
		ms = []
		ms2 = []
		ms1 =[]
		#new implementation to follow lognorm
		#for x in range(ranged):
			#x = random.randint(0,100)
			#simulating 5% detection limit
			#if x < 10: #does not change the result
			#	x = 0
			#ms.append(x)

		#generating random numbers (lognormal distributed)
		ms = np.random.lognormal(np.log(maxima),1,ranged)

		f = Fingeprint()
		f.tol1 = tolerance
		
		#normalise to the highest 
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
	ms2.subset(100, 1000)#100-1000
	ms2.match(msL.mzH)#changed to matchS instead for strict results
	#ms2.highestN(ms2.mzSub, ms2.specSub, 40)
	#ms2.quantify()#flow [l/min], integration time [min], load [mL] ... return in the massSpec.ng
	ms2.quant(0.06,10,1)#Sonnblick (0.06,8,0.1.5)
	quant_ng = ms2.ng
	ms2.normalise(ms2.mzSub2, ms2.specSub2)

	f2 = Fingeprint()
	f2.calculate(msL.mzNhigh, msL.specNhigh, ms2.mzNhigh, ms2.specNhigh)
	
	#corrected quantificaiton
	f2.quant(0.06,10,1, ms2.specSub2, ms2.mzSub2)#f2.quant(0.06,10,1, ms2.specSub2, ms2.mzSub2) for SLU samples
	quantC_ng = f2.ng 	
		
	a = f2.match
	b = f2.match2
	
	

	
	#f2.plott()

	print("Alg. 1 " , a)
	print("Alg. 2 " , b)

	f2.calculate(msL.mzNsum, msL.specNsum, ms2.mzNsum, ms2.specNsum)
	c = f2.match
	d = f2.match2

	print("Alg. 3 " , c)
	print("Alg. 4 " , d)

	print("\n")
	if a > x+y*4:
		print("Algorithm 1: MATCH ! (***) confidence")
		rAlg1.append("***,")
	elif a>x+y*3:
		print("Algorithm 1: MATCH ! (**) confidence")
		rAlg1.append("**,")
	elif a>x+y*2:
		print("Algorithm 1: MATCH ! (*) confidence")
		rAlg1.append("*,")
	else:
		print("Algorithm 1: no match")
		rAlg1.append("-,")
		
			
	if b > w+z*4:
		print("Algorithm 2: MATCH ! (***) confidence")
		rAlg2.append("***,")
	elif b>w+z*3:
		print("Algorithm 2: MATCH ! (**) confidence")
		rAlg2.append("**,")
	elif b>w+z*2:
		print("Algorithm 2: MATCH ! (*) confidence")
		rAlg2.append("*,")
	else:
		print("Algorithm 2: no match")
		rAlg2.append("-,")


	if c > x2+y2*4:
		print("Algorithm 3: MATCH ! (***) confidence")
		rAlg3.append("***,")
	elif c>x2+y2*3:
		print("Algorithm 3: MATCH ! (**) confidence")
		rAlg3.append("**,")
	elif c>x2+y2*2:
		print("Algorithm 3: MATCH ! (*) confidence")
		rAlg3.append("*,")
	else:
		print("Algorithm 3: no match")
		rAlg3.append("-,")
		
			
	if d > w2+z2*4:
		print("Algorithm 4: MATCH ! (***) confidence")
		rAlg4.append("***,")
	elif d>w2+z2*3:
		print("Algorithm 4: MATCH ! (**) confidence")
		rAlg4.append("**,")
	elif d>w2+z2*2:
		print("Algorithm 4: MATCH ! (*) confidence")
		rAlg4.append("*,")
	else:
		print("Algorithm 4: no match")
		rAlg4.append("-,")
	
	
	rAlg1.append(str(a))
	rAlg2.append(str(b))
	rAlg3.append(str(c))
	rAlg4.append(str(d))

def clearAll():
	del rAlg1[:]
	del rAlg2[:]
	del rAlg3[:]
	del rAlg4[:]
	
