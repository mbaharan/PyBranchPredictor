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


class Voter:

    def __init__(self, default_state=1):

        if 0 <= default_state <= 3:
            self.state = default_state
        else:
            self.state = 1

    def evaluate(self, P1_prediction, P2_prediction):

        past = self.state

        if past == 0:
            if P2_prediction and not P1_prediction:
                self.state = 1

        elif past == 1:
            if P2_prediction and not P1_prediction:
                self.state = 2
            elif not P2_prediction and P1_prediction:
                self.state = 0

        elif past == 2:
            if P2_prediction and not P1_prediction:
                self.state = 3
            elif not P2_prediction and P1_prediction:
                self.state = 1
        else:
            if not P2_prediction and P1_prediction:
                self.state = 2

        return past
