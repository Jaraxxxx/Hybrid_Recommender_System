import numpy as np 
import pandas as pd
from web.models import Myrating
import scipy.optimize 


def Myrecommend():
	def normalizeRatings(myY, myR):
    	# The mean is only counting movies that were rated
		# print(np.sum(myY,axis=1)) #MovieId sum from Y Matrix
		# print(np.sum(myR,axis=1)) #1 sum from R Matrix
		# print(np.sum(myY,axis=1)/np.sum(myR,axis=1))
		print(np.sum(myY,axis=1))
		print(np.average(myR,axis=1))
		Ymean = np.sum(myY,axis=1)/np.average(myR,axis=1)
		Ymean = Ymean.reshape((Ymean.shape[0],1)) # 1d array reshaping I guess
		print(myY-Ymean)
		return myY-Ymean, Ymean
	
	def flattenParams(myX, myTheta):
		return np.concatenate((myX.flatten(),myTheta.flatten()))
    
	def reshapeParams(flattened_XandTheta, mynm, mynu, mynf):
		assert flattened_XandTheta.shape[0] == int(mynm*mynf+mynu*mynf)
		reX = flattened_XandTheta[:int(mynm*mynf)].reshape((mynm,mynf))
		reTheta = flattened_XandTheta[int(mynm*mynf):].reshape((mynu,mynf))
		return reX, reTheta

	def cofiCostFunc(myparams, myY, myR, mynu, mynm, mynf, mylambda = 0.):
		myX, myTheta = reshapeParams(myparams, mynm, mynu, mynf)
		term1 = myX.dot(myTheta.T)
		term1 = np.multiply(term1,myR)
		cost = 0.5 * np.sum( np.square(term1-myY) )
    	# for regularization
		cost += (mylambda/2.) * np.sum(np.square(myTheta))
		cost += (mylambda/2.) * np.sum(np.square(myX))
		return cost

	def cofiGrad(myparams, myY, myR, mynu, mynm, mynf, mylambda = 0.):
		myX, myTheta = reshapeParams(myparams, mynm, mynu, mynf)
		term1 = myX.dot(myTheta.T)
		term1 = np.multiply(term1,myR)
		term1 -= myY
		Xgrad = term1.dot(myTheta)
		Thetagrad = term1.T.dot(myX)
    	# Adding Regularization
		Xgrad += mylambda * myX
		Thetagrad += mylambda * myTheta
		return flattenParams(Xgrad, Thetagrad)

	df=pd.DataFrame(list(Myrating.objects.all().values()))
	print(df)
	mynu=df.user_id.unique().shape[0]
	mynm=df.movie_id.unique().shape[0]
	mynf=10
	Y=np.zeros((mynm,mynu))
	# print(Y)
	for row in df.itertuples():
		# print(row[2],end = ' ') ##UserId
		# print(row[3],end = ' ') ##MovieID
		# print(row[4],end = ' ') ##Ratings
		# print(Y[row[2]-1,row[4]-1])
		Y[row[2]-1, row[4]-1] = row[3]   
		### UId,MId,Ratings(Y Matrix) => UId,1,Ratings (R Matrix) (No Significance of Letters L & R)
		# 	 R1  R2				R1  R2
		# U1 M1  0		==>  U1  1   0
		# U2 0   M2			 U2  0   1
		### 
	R=np.zeros((mynm,mynu))
	print(Y.shape[0])
	print(Y.shape[1])
	for i in range(Y.shape[0]):
		for j in range(Y.shape[1]):
			# print(Y[i][j], end =" ")
			if Y[i][j]!=0:
				R[i][j]=1
	print()

	Ynorm, Ymean = normalizeRatings(Y,R)
	X = np.random.rand(mynm,mynf)
	Theta = np.random.rand(mynu,mynf)
	myflat = flattenParams(X, Theta)
	mylambda = 12.2
	result = scipy.optimize.fmin_cg(cofiCostFunc,x0=myflat,fprime=cofiGrad,args=(Y,R,mynu,mynm,mynf,mylambda),maxiter=40,disp=True,full_output=True)
	resX, resTheta = reshapeParams(result[0], mynm, mynu, mynf)
	prediction_matrix = resX.dot(resTheta.T)
	return prediction_matrix,Ymean
	







