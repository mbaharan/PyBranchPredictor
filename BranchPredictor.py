#!/usr/bin/python

'''
Copyright (c) <2018> <Mohammadreza Baharani>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from OLBP import OneLevelBranchPredictor
from TLGBP import TwoLevelGlobalBranchPredictor
from Gshare import Gshare 
from TLLBP import TwoLevelLocalBranchpredictor

import sys
import matplotlib.pyplot as plt

def readFile(fileName, limit):
	dataArr=[]
	with open(fileName) as f:
		lines = f.readlines()
		if (limit > 0):
			rng = limit
		else:
			rng = len(lines)
		
		for line in lines[0:rng]:
			data = line.split(' ')
			addr = int(data[0],  16)# >> 5
			actualRes = data[1].rstrip("\r\n")
			dataArr.append([addr, actualRes])
	return dataArr


def	simulate(predictor, data):
	i=0
	length = len(data)
	for val in data:
		i = i + 1;
		predictor.evalue(val)
		sys.stdout.write(predictor.name + " simulation completed: {0:.2f}%, convergence: {1:.2f}\r".format(float(i)*100/length, predictor.converges[i-1]))
		sys.stdout.flush()
	print
	print float(predictor.predictedTrue)/predictor.access
	
	
def simulateAllType(predictors, data):
	i=0
	for val in data:
		i = i + 1;
		for j in range(0, 4):
			predictors[j].evalue(val)
				#sys.stdout.write(predictor.name + " simulation completed: {0:.2f}%, convergence: {1:.2f}\r".format(float(i)*100/length, predictor.converges[i-1]))	
if __name__ =='__main__':
	predictor = '2level-global'#'1level'
	tableSize = 1024
	nBitSize = 3
	localHistoryTableSize = 128
	fileName = './branch-trace-gcc.trace'
	limit = 0
	data = readFile(fileName ,limit)
	simulationMode = 3

	fig = plt.figure()
	ax  = fig.add_subplot(111)

	
	if(simulationMode == 1):
		p1 = OneLevelBranchPredictor('1-level', tableSize, nBitSize, 'N', len(data), 0)
		simulate(p1, data)
	
		p2 = TwoLevelGlobalBranchPredictor('2-level global', tableSize, nBitSize, 'N', len(data), 0)
		simulate(p2, data)
	
		p3 = Gshare('G-share', tableSize, nBitSize, 'N', len(data), 0)
		simulate(p3, data)
	
		p4 = TwoLevelLocalBranchpredictor('2-level local', localHistoryTableSize, tableSize, nBitSize, 'N', len(data), 0)
		simulate(p4, data)
		
		ax.plot(range(1,len(data)+1), p1.converges, c='b', label=p1.name,linewidth=0.3, linestyle='-.')
		ax.plot(range(1,len(data)+1), p2.converges, c='r', label=p2.name,linewidth=0.3, linestyle='--')
		ax.plot(range(1,len(data)+1), p3.converges, c='g', label=p3.name,linewidth=0.3, linestyle='-')
		ax.plot(range(1,len(data)+1), p4.converges, c='k', label=p4.name,linewidth=0.3, linestyle=':')
		ax.set_yscale('log')

		ax.set_xlabel('Number of branches')
		ax.set_ylabel('Wrong prediction')
		

	elif(simulationMode == 2):
		bitSize = range(2, 12, 2)
		predictors = [[0 for x in range(len(bitSize))] for y in range(4)]
		
		counter = 0;
		for j in range(0, len(bitSize)):
			sys.stdout.write("{0:.2f}%\r".format(float(j)*100/len(bitSize)))
			sys.stdout.flush()
			bit = bitSize[j]
			predictors[0][j] =  OneLevelBranchPredictor('1-level'.format(bit), tableSize, bit, 'N', len(data), 1)
			predictors[1][j] =  TwoLevelGlobalBranchPredictor('2-level global'.format(bit), tableSize, bit, 'N', len(data), 1)
			predictors[2][j] = Gshare('G-share'.format(bit), tableSize, bit, 'N', len(data), 1)
			predictors[3][j] = TwoLevelLocalBranchpredictor('2-level local'.format(bit), localHistoryTableSize, tableSize, bit, 'N', len(data), 1)
			simulateAllType([row[j] for row in predictors], data)
			counter = counter + 1;
			

		ax.set_xlabel('Bit size')
		ax.set_ylabel('Wrong prediction(%)')
		ax.yaxis.set_ticks(range(5, 25, 5))
		misRate = [];
		color = {0:'b', 1:'r', 2:'g', 3:'k'}
		ls = {0:'-.', 1:'--', 2:'-', 3:':'}
		for i in range(0, 4):
			for j in range(0, len(bitSize)):
				misRate.append((1 - (float(predictors[i][j].predictedTrue)/predictors[i][j].access)) * 100)
			ax.plot(bitSize, misRate, c=color[i], label=predictors[i][0].name,linewidth=0.3, linestyle=ls[i])
			misRate = []
	else:
		from myprediction import myPrediction
		mp = myPrediction('myprediction', tableSize, nBitSize, 'N', len(data), 0)
		i=0
		length = len(data)
		for val in data:
			i = i + 1;
			mp.evalue(val)
			sys.stdout.write(mp.name + " simulation completed: {0:.2f}%, convergence: {1:.2f}\r".format(float(i)*100/length, mp.converges[i-1]))
			sys.stdout.flush()
		print
		print mp.name + " : " + str(float(mp.predictedTrue)/mp.oneLevel.totalAccess)
		print mp.gShare.name + " : " +  str(float(mp.gShare.predictedTrue)/mp.oneLevel.totalAccess)
		print mp.oneLevel.name + " : " +  str(float(mp.oneLevel.predictedTrue)/mp.oneLevel.totalAccess)
			
		ax.plot(range(1,len(data)+1), mp.gShare.converges, c='b', label=mp.gShare.name,linewidth=0.3, linestyle='-.')
		ax.plot(range(1,len(data)+1), mp.oneLevel.converges, c='r', label=mp.oneLevel.name,linewidth=0.3, linestyle='--')
		ax.plot(range(1,len(data)+1), mp.converges, c='g', label=mp.name,linewidth=0.3, linestyle='-')
		ax.set_yscale('log')
		ax.set_xlabel('Number of branches')
		ax.set_ylabel('Wrong prediction')
		
			
	leg = plt.legend()
	plt.show()
	
