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

from Gshare import Gshare
from OLBP import OneLevelBranchPredictor
from voter import Voter

class Tournament:

    def __init__(self, name, tableSize, nBitSize, firstN_bitCounter, savingMode):

        self.name = name
        self.access = 0
        self.predictedTrue = 0
        self.converges = []

        self.one_level_prediction = OneLevelBranchPredictor(name='T_1-level', tableSize=tableSize, nBitSize=nBitSize,
                                                            firstN_bitCounter=firstN_bitCounter, savingmode=1)
        self.gshare = Gshare(name='T_G-share', tableSize=tableSize, nBitSize=nBitSize,
                             firstN_bitCounter=firstN_bitCounter, savingMode=1)

        self.voter = Voter()

        self.savingMode = savingMode

    def evaluate(self, data):

        self.access = self.access + 1

        p1_prediction = self.one_level_prediction.evaluate(data)
        p2_prediction = self.gshare.evaluate(data)

        which_one = self.voter.evaluate(P1_prediction=p1_prediction, P2_prediction=p2_prediction)

        if 0 <= which_one <= 1:
            if p1_prediction:
                self.predictedTrue = self.predictedTrue + 1
        else:
            if p2_prediction:
                self.predictedTrue = self.predictedTrue + 1

        if not self.savingMode:
            if not (self.access-1) % 1000:
                self.converges.append(1-(float(self.predictedTrue)/self.access))
        else:
            self.converges = 1 - (float(self.predictedTrue)/self.access)
