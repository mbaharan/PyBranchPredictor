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
from nBitCounter import nBitCounter

class TwoLevelGlobalBranchPredictor:
    def __init__(self, name, tableSize, nBitSize, firstN_bitCounter, totalAccess, savingMode):
        self.name = name
        self.tableSize = tableSize;
        self.access = 0;
        self.totalAccess = totalAccess
        self.predictedTrue = 0;
        self.patternHistoryTable = {};
        self.Mask = tableSize - 1;
        self.GHR=0;
        self.converges = []
        self.savingMode = savingMode
        for i in range(0, self.tableSize):
            n = nBitCounter(nBitSize, firstN_bitCounter, 'sarturated');
            self.patternHistoryTable[i]=n;#PC, nBitCounter
            
    def evalue(self, data):
        
        actualOutcome = data[1]
        
        self.access = self.access + 1;
        
        predictedTrue = self.patternHistoryTable[self.GHR].evaluate(actualOutcome)
        
        self.GHR = self.GHR << 1
       
        if(actualOutcome == 'T'):
            self.GHR = self.GHR | 1
         
        self.GHR = self.GHR & self.Mask;

        if(predictedTrue):
            self.predictedTrue = self.predictedTrue + 1
        #else:
        #    self.predictedTrue = self.predictedTrue - 1
        #    if(self.predictedTrue <= 0):
        #        self.predictedTrue = 1;

        #self.converges.append(math.log(float(self.predictedTrue)/self.totalAccess))
        if(self.savingMode == 0 ):
            self.converges.append(1-(float(self.predictedTrue)/self.totalAccess))
        else:
            self.converges = 1-(float(self.predictedTrue)/self.totalAccess)