# FngClass
# Created by Dusan on 24/02/2019.
#last update 19.11.2019
#solved the issues of devison by zero: in normalise ()

#optimising quantification for reducing the overestimation 7/8/2019

#class works fine

class massSpec:
		global mz 
		global spec
		global filename
		global mzSub #subset of the array 
		global specSub
		global mzSub2 #subset of the array 
		global specSub2
		global mzH
		global specH
		global mzNsum
		global mzNhigh
		global specNsum
		global specNhigh
		global toleranceMZ
		global ng
		
		
		def __init__(self):
			self.mz = []
			self.spec = []
			self.mzSub = []
			self.specSub = []
			self.mzSub2 = []
			self.specSub2 = []
			self.mzH = []
			self.specH = []
			self.mzNhigh = []
			self.mzNsum = []
			self.specNhigh = []
			self.specNsum = []
			self.toleranceMZ = 0.005
			self.ng = 0.0
			
				
		def inputFile (self, filename):
			self.filename = filename
			
		def msLoad(self):	
			with open(self.filename,"r") as f:
				for line in f:
					line = line.replace("\r", '')
					line = line.replace("\n", '')
					#gsub("\r?\n|\r", "", line)
					array1 = line.rsplit(',', 2)
					#print '    ' , array1
							
					self.mz.append(float(array1[0]))  
					self.spec.append(float(array1[1]))  
		#print "mz",mz		
		
		def set (self,fname):
			self.inputFile(fname)
			self.msLoad()
		
		def subset (self, start, untill):
			i = 0
			for mass in self.mz:
				if (mass>=start and mass<=untill):
					self.mzSub.append(self.mz[i])
					self.specSub.append(self.spec[i])
				i=i+1
				
		def match (self, mzL):
			i=0
			j=0
			for mass in mzL:
				mass = float(mass)
				j=0
				for massFile in self.mzSub:
					massFile = float(massFile)
					if (abs(mass-massFile)<self.toleranceMZ):
						
						self.mzSub2.append(massFile)
						self.specSub2.append(self.specSub[j])	
					j=j+1
					#print j,"\n"
				i=i+1
		
		#a new function added 13/5/2019 to quantify the ions
		def quantify (self):#takes the argumetns stored in mzSub2 and specSub2 so must coll match() before this
			for p in range(len(self.specSub2)):
				#print (str(p) + str(specSub2[p]))
				self.ng += self.specSub2[p]*self.mzSub2[p]*0.05*10/24.45
		
		def quant (self,flow,time,load):#takes the argumetns stored in mzSub2 and specSub2 so must coll match() before this
			for p in range(len(self.specSub2)):
				#print (str(p) + str(specSub2[p]))
				self.ng += self.specSub2[p]*self.mzSub2[p]*flow*time/(24.45*load)
		
		def quant2 (self,flow,time,load,correction):#takes the argumetns stored in mzSub2 and specSub2 so must coll match() before this
			for p in range(len(self.specSub2)):
				#print (str(p) + str(specSub2[p]))
				self.ng += self.specSub2[p]*correction[p]*self.mzSub2[p]*flow*time/(24.45*load)

		
		def matchS (self, mzL):#mIN PTOGRESS -- atch and substitute if there is no ions from the library 
			i=0
			j=0
			
			for mass in mzL:#looping the library m/z
				mass = float(mass)
				mathc_found = 0
				j=0
				for massFile in self.mzSub:# looping through long sample subset m/z 100 - 1000
					massFile = float(massFile)
					if (abs(mass-massFile)<self.toleranceMZ):
						self.mzSub2.append(massFile)
						self.specSub2.append(self.specSub[j])	
						mathc_found = 1
					j=j+1
				if (mathc_found==0):
					self.mzSub2.append(mass)
					self.specSub2.append(0.0)
					#print j,"\n"
					
				i=i+1

					
				
		def highestN (self, ms, spec, N): #sorting the library file to select the highest N
			for i in range(0, N):  
				max1 = 0
				max2 = 0
				for j in range(len(spec)):      
					if spec[j] > max1: 
						max1 = spec[j]
						max2 = ms[j]
				spec.remove(max1)
				self.specH.append(max1) 
				ms.remove(max2)
				self.mzH.append(max2)
		
		def normalise (self,  ms, spec):#call aftrer selecting highest or directlry in non-library mass spectra
			maximum = max(spec)
			sumary = sum(spec)
			i = 0
			for num in spec:
				if (maximum>0):
					self.specNhigh.append(num*100/maximum)
				else:
					self.specNhigh.append(0)
				if (sumary>0):
					self.specNsum.append(num*100/sumary)
				else:
					self.specNsum.append(0)
				self.mzNsum.append(ms[i])
				self.mzNhigh.append(ms[i])
				i=i+1
			
			
		def getMz (self):
			return self.mz
			
		def getSpec (self):
			return self.spec
		
class Fingeprint:
		global tol1
		global mz
		global diff
		global averageDif
		global mzL
		global specL
		global mzN
		global specN
		global match
		global match2
		global ng_corr_fact
		global ng
		
		def __init__(self):
			self.tol1 = 0.005
			self.mz = []
			self.diff = []
			self.averageDif = 0.0
			self.mzL = []
			self.mzN = []
			self.specL = []
			self.specN = []
			self.match = 0 #to be used as final result
			self.match2 = 0
			self.ng_corr_fact = []
			self.ng = 0.0
		
		def calculate (self,mzL,specL,mzN, specN):
			self.mzL = mzL
			self.specL = specL
			self.mzN = mzN
			self.specN = specN
			self.ng = 0.0
			self.ng_corr_fact = []
			i = 0
			j = 0
			difference = 0
			difN = 0 #normalised differece
			difN2 = 0
			difT = 0 #absolute difference
			difT2 = 0
			difOVER = 0
			difOVER2 = 0
			difNORM = 0 # normalised difference to the total mass spectra
			difNORM2 = 0
			difNORMover = 0
			difNORMover2 = 0
			difMAX = 0
			difMAX2 = 0
			difMAX_i = 0
			difMAX_i2 = 0
			difPLOT = []
			difPLOT_N = []

			for mass in mzL:
				mass = float(mass)
				#print mass,"<-\n"
				#print "i = ", i
				found = 0
				j=0
				for massFile in mzN:
					massFile = float(massFile)
					if (abs(mass-massFile) < self.tol1):
						found = 1
						#print "found ", mass, " j: ",j, " i: ",i, "\n"
						difference = (float(specN[j])-float(specL[i]))	
						difPLOT.append(difference)
						
						#quantification corretion
						if (difference>=0):
							self.ng_corr_fact.append(float(specL[i])/float(specN[j]))#presentage of difference as correction factor
						else:
							self.ng_corr_fact.append(float(1))
						
						difN = abs(difference)/(100/float(specL[i]))#compenzating to higher peaks
						difN2 = abs(difference)#all peaks treated the same
						#difN = abs(difference)
						difPLOT_N.append((difference)/(100/float(specL[i])))
						#limit to maximum 100% more signal
						difMAX_i = specL[i]*specL[i]/100
						difMAX_i2 = specL[i]
						difMAX += difMAX_i
						difMAX2 += difMAX_i2

						if difN<=difMAX_i:
							difT += difN 	
						else:
							difN = difMAX_i
							difT += difN

						#this is considering all peaks the same
						if difN2<=difMAX_i2:
							difT2 += difN2 	
						else:
							difN2 = difMAX_i2
							difT2 += difN2

							
						#difMAX += specL[i]
						
						#print "calculation:"
						#print float(specN[j]) ,'-' , float(specL[i])
						#print "abs difference ", difference
						#print "norm difference: ", difN2, '%', "of maximal ", difMAX_i2 , "\n"
						if difference < 0: #perhaps exclude
							difOVER += difN
							difOVER2 += difN2
					
					j=j+1
					#print j,"\n"
					#next; #to avoid multiple match
				if (found == 0):
					difPLOT.append(float(specL[i])*(-1))
				i=i+1
				found = 0
				
			#function line
			difNORM = difT*100/difMAX
			difNORMover = difOVER*100/difMAX
			difNORM2 = difT2*100/difMAX2
			difNORMover2 = difOVER2*100/difMAX2
			
			self.mz = mzL
			self.diff = difPLOT
			self.match = 100-difNORM
			self.match2 = 100-difNORM2
			
			#print "\n"
			#print "Maximal difference: ", difMAX
			#print "Total difference " , difT
			#print "Total normalised difference %" , difNORM
			#print "\n"
			if specN.__len__()>specL.__len__():
				print("WARNING! found more masses then expected from the library: ", specN.__len__()-specL.__len__(), "\n")

			#PRINTING VALUES
			#print "Total match: ", 100-difNORM, "%"
			#print "Total match overshut ignored: ", 100-difNORMover, "%"
			#print "Total match2: ", 100-difNORM2, "%"
			#print "Total match2 overshut ignored: ", 100-difNORMover2, "%"
			
			
			import numpy as np

			self.averageDif = np.mean([100-difNORM,100-difNORMover,100-difNORM2,100-difNORMover2])
			
			#print "AVERAGE: ", self.averageDif
			
		def quant (self,flow,time,load,spec,mz):#takes the argumetns stored in f.mzSub2 and f.specSub2 so must coll match() before this
			for p in range(len(spec)):
				#print (str(p) + str(specSub2[p]))
				self.ng += spec[p]*self.ng_corr_fact[p]*mz[p]*flow*time/(24.45*load) 				

		def plott (self):#might result in different size of strings
			import matplotlib.pyplot as plt
			
			plt.subplot(3,1,1)
			plt.bar (self.mzL, self.specL, width=0.25)
			plt.grid(True)
			plt.ylim(-110 , 110)
			#plt.ylim(-50 , 50)
			plt.xlim(100,200)
			#plt.xlabel("m/z")
			plt.ylabel('Library')
			
			plt.subplot(3,1,2)
			plt.bar (self.mzN, self.specN, width=0.25)
			plt.grid(True)
			plt.ylim(-110 , 110)
			#plt.ylim(-50 , 50)
			plt.xlim(100,200)
			#plt.xlabel("m/z")
			plt.ylabel('Sample')

			plt.subplot(3,1,3)
			plt.bar (self.mz, self.diff, width=0.25)
			plt.grid(True)
			plt.ylim(-110 , 110)
			#plt.ylim(-50 , 50)
			plt.xlim(100,200)
			plt.xlabel("m/z")
			plt.ylabel('Difference')
			plt.savefig('Figure.png', dpi=300)
			plt.show()
