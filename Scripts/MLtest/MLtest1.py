'''
How to set buffer size so far
1. see 'signal resampling' box in openvibe
2. set epoch cound from 'sample count per buffer'
3. change the value of 'epoch' in python script
'''
import numpy as np
import argparse
import random
import time
import csv

from pythonosc import udp_client

global epoch
global meditation
global electrode
global duration
global noteNum

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=7402,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]


f = open("C:/Users/seohyunseo/Desktop/BCIMusic/Data/ML/train_set.csv",
         'w', newline='')
wr = csv.writer(f)
wr.writerow(['theta', 'alpha', 'beta', 'gamma', 'label'])


class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.signalHeader = None
        self.sum = 0

    def process(self):
        # initialize variables
        epoch = 250
        electrode = 0

        for chunkIdx in range(len(self.input[0])):
            if (type(self.input[0][chunkIdx]) == OVSignalHeader):
                self.signalHeader = self.input[0].pop()
                outputHeader = OVSignalHeader(self.signalHeader.startTime, self.signalHeader.endTime, [1, self.signalHeader.dimensionSizes[1]], [
                                              'Mean']+self.signalHeader.dimensionSizes[1]*[''], self.signalHeader.samplingRate)

                print(outputHeader)
            elif(type(self.input[0][chunkIdx]) == OVSignalBuffer):
                chunk0 = self.input[0].pop()
                chunk1 = self.input[1].pop()
                chunk2 = self.input[2].pop()
                chunk3 = self.input[3].pop()

                if(type(chunk1) != OVSignalHeader):
                    list_chunked0 = list_chunk(chunk0, epoch)
                    list_chunked1 = list_chunk(chunk1, epoch)
                    list_chunked2 = list_chunk(chunk2, epoch)
                    list_chunked3 = list_chunk(chunk3, epoch)

                    theta = np.mean(list_chunked0[electrode])
                    alpha = np.mean(list_chunked1[electrode])
                    beta = np.mean(list_chunked2[electrode])
                    gamma = np.mean(list_chunked3[electrode])
                    wr.writerow([theta, alpha, beta, gamma])

            elif(type(self.input[0][chunkIdx]) == OVSignalEnd):
                print(self.input[0].pop())
                f.close()


box = MyOVBox()
