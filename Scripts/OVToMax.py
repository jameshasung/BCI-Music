import numpy
import argparse
import random
import time

from pythonosc import udp_client


class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.signalHeader = None

    def process(self):
        if __name__ == "__main__":
            parser = argparse.ArgumentParser()
            parser.add_argument("--ip", default="127.0.0.1",
                                help="The ip of the OSC server")
            parser.add_argument("--port", type=int, default=7402,
                                help="The port the OSC server is listening on")
            args = parser.parse_args()

            client = udp_client.SimpleUDPClient(args.ip, args.port)

            for chunkIdx in range(len(self.input[0])):
                if(type(self.input[0][chunkIdx]) == OVSignalHeader):
                    self.signalHeader = self.input[0].pop()

                    outputHeader = OVSignalHeader(self.signalHeader.startTime, self.signalHeader.endTime, [1, self.signalHeader.dimensionSizes[1]], [
                        'Mean']+self.signalHeader.dimensionSizes[1]*[''], self.signalHeader.samplingRate)

                    # self.output[0].append(outputHeader)
                    # print(outputHeader)

                elif(type(self.input[0][chunkIdx]) == OVSignalBuffer):
                    chunk = self.input[0].pop()
                    numpyBuffer = numpy.array(chunk).reshape(
                        tuple(self.signalHeader.dimensionSizes))
                    numpyBuffer = numpyBuffer.mean(axis=0)
                    chunk = OVSignalBuffer(
                        chunk.startTime, chunk.endTime, numpyBuffer.tolist())
                    # self.output[0].append(chunk)
                    client.send_message("electrode", chunk)
                    # print(chunk)

                elif(type(self.input[0][chunkIdx]) == OVSignalEnd):
                    # self.output[0].append(self.input[0].pop())
                    print(self.input[0].pop())


box = MyOVBox()
