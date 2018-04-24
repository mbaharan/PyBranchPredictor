#!/usr/bin/python3.5


"""
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
"""

from OLBP import OneLevelBranchPredictor
from TLGBP import TwoLevelGlobalBranchPredictor
from Gshare import Gshare 
from TLLBP import TwoLevelLocalBranchpredictor

import gzip


def simulate(predictors, fileName):
    i = 0
    with gzip.open(fileName, 'rt') as f:
        for line in f:
            if line.startswith('@#'):
                data = line.replace('@# ', '').split(',')
                i = i + 1
                if data[1].rstrip("\r\n") == '1':
                    val = 'T'
                else:
                    val = 'N'

                if not (i - 1) % 100000:
                    import os
                    os.system('clear')

                for predictor in predictors:
                    predictor.evaluate([int(data[0], 10), val])

                    if not (i-1) % 100000:
                        print(predictor.name + " simulation completed for: {}, error: {:.2f}"
                              .format(i, (predictor.converges[-1])*100), end='\n', flush=True)

    for j in range(0, 4):
        print(float(predictors[i].predictedTrue)/predictors[i].access)

    return i
    

if __name__ == '__main__':
    tableSize = 1024
    nBitSize = 2
    localHistoryTableSize = 128
    fileName = './perlbench_branch.gz'

    p1 = OneLevelBranchPredictor(name='1-level', tableSize=tableSize, nBitSize=nBitSize, firstN_bitCounter='T',
                                 savingmode=0)

    p2 = TwoLevelGlobalBranchPredictor(name='2-level global', tableSize=tableSize, nBitSize=nBitSize,
                                       firstN_bitCounter='T',  savingMode=0)

    p3 = Gshare(name='G-share', tableSize=tableSize, nBitSize=nBitSize, firstN_bitCounter='T', savingMode=0)

    p4 = TwoLevelLocalBranchpredictor(name='2-level local', localTablSize=localHistoryTableSize, tableSize=tableSize,
                                      nBitSize=nBitSize, firstN_bitCounter='T', savingMode=0)

    simulate([p1, p2, p3, p4], fileName)
