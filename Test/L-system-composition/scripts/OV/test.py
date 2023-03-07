
import numpy as np
import argparse
import random
import time

from pythonosc import udp_client

global epoch

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


class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.signalHeader = None
        self.idx = 0
        self.sum = 0.

    def process(self):
        # initialize variables
        epoch = 8
        for chunkIdx in range(len(self.input[0])):
            if (type(self.input[0][chunkIdx]) == OVSignalHeader):
                self.signalHeader = self.input[0].pop()

                outputHeader = OVSignalHeader(self.signalHeader.startTime, self.signalHeader.endTime, [1, self.signalHeader.dimensionSizes[1]], [
                                              'Mean']+self.signalHeader.dimensionSizes[1]*[''], self.signalHeader.samplingRate)
                print(outputHeader)

            elif(type(self.input[0][chunkIdx]) == OVSignalBuffer):
                chunk = self.input[0].pop()
                list_chunked = list_chunk(chunk, epoch)
                alpha_ratio = list_chunked[0][0]
                client.send_message('Alpha', alpha_ratio)
                self.sum += alpha_ratio
                if self.idx == 30:
                    self.sum /= (self.idx+1)
                    client.send_message("average", self.sum)
                self.idx += 1

            elif(type(self.input[0][chunkIdx]) == OVSignalEnd):
                print(self.input[0].pop())


box = MyOVBox()
