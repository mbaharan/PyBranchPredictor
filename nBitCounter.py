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

class nBitCounter:
    def __init__(self, nSize, firstPrediction, model):
        self.nSize = nSize;
        self.Max = 2**(nSize)-1;
        self.model = model
        if(firstPrediction == "T"):
            self.counter = self.Max;
        else:
            self.counter = 0;
            
    def evaluate(self, actualResult):
        res = True;
        assert (self.counter <= self.Max)
        assert (self.counter >= 0)
        
        if(self.model == 'hysteresis'):
            if(actualResult == "T"):
                if(self.counter >= (self.Max)/2 + 1):
                    if(self.counter < (self.Max)):
                        self.counter = self.counter + 1
                else:
                    if(self.counter == (self.Max)/2):
                        self.counter = self.Max
                    else:
                        self.counter = self.counter + 1
                        res = False
            else:
                if(self.counter <= (self.Max)/2):
                    if(self.counter > 0):
                        self.counter = self.counter - 1
                else:
                    if(self.counter == (self.Max)/2 + 1):
                        self.counter = 0
                    else:
                        self.counter = self.counter - 1
                        res = False
        else:
            if(actualResult == "T"):
                if(self.counter >= (self.Max)/2 + 1):
                    if(self.counter < (self.Max)):
                        self.counter = self.counter + 1
                else:
                    self.counter = self.counter + 1
                    res = False
            else:
                if(self.counter <= (self.Max)/2):
                    if(self.counter > 0):
                        self.counter = self.counter - 1
                else:
                    self.counter = self.counter - 1
                    res = False
        return res