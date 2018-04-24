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


class TwoLevelLocalBranchpredictor:

    def __init__(self, name, localTablSize, tableSize, nBitSize, firstN_bitCounter, savingMode):
        self.name = name
        self.tableSize = tableSize
        self.localTableSize = localTablSize
        self.access = 0
        self.predictedTrue = 0
        self.patternHistoryTable = {}
        self.localBranchHistory = {}
        self.Mask = tableSize - 1
        self.localMask = localTablSize - 1
        self.converges = []
        self.savingMode = savingMode
        for i in range(0, self.tableSize):
            n = nBitCounter(nBitSize, firstN_bitCounter, 'sarturated')
            self.patternHistoryTable[i] = n  # PC, nBitCounter
        for i in range(0, self.localTableSize):
            self.localBranchHistory[i] = 0

    def evaluate(self, data):

        tagAddress = data[0]
        actualOutcome = data[1]

        self.access = self.access + 1

        indexLocal = ((tagAddress>>3) & self.localMask)  # To capture basic block changing phase
        
        assert(0<= indexLocal <= self.localMask)
        
        index = self.localBranchHistory[indexLocal]
        
        assert(0<= index <= self.Mask)
        
        predictedTrue = self.patternHistoryTable[index].evaluate(actualOutcome)
        
        self.localBranchHistory[indexLocal] = self.localBranchHistory[indexLocal] << 1

        if actualOutcome == 'T':
            self.localBranchHistory[indexLocal] = self.localBranchHistory[indexLocal] | 1
            
        self.localBranchHistory[indexLocal] = self.localBranchHistory[indexLocal] & self.Mask

        if predictedTrue:
            self.predictedTrue = self.predictedTrue + 1

        if not self.savingMode:
            if not (self.access-1) % 1000:
                self.converges.append(1-(float(self.predictedTrue)/self.access))
        else:
            self.converges = 1 - (float(self.predictedTrue)/self.access)
