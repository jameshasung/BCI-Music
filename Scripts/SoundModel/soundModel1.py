'''
title: sound model test 1
data: meditation
controlled component: tempo(metro) 
description: the tempo of the music will be increased when meditation is low and decreased when vice versa.
openvibe server settings: check 'Esence' in 'Driver properties' / downsampling 512 -> 128
resource: soundModel1.maxpat / soundModel1.xml
'''
import numpy as np
import argparse
import random
import time

from pythonosc import udp_client

global epoch
global meditation
global electrode

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

    def process(self):

        # initialize variables
        epoch = 8
        electrode = 0
        meditation = 2

        for chunkIdx in range(len(self.input[0])):
            if(type(self.input[0][chunkIdx]) == OVSignalHeader):
                self.signalHeader = self.input[0].pop()

                outputHeader = OVSignalHeader(self.signalHeader.startTime, self.signalHeader.endTime, [1, self.signalHeader.dimensionSizes[1]], [
                                              'Mean']+self.signalHeader.dimensionSizes[1]*[''], self.signalHeader.samplingRate)

                # self.output[0].append(outputHeader)
                print(outputHeader)

            elif(type(self.input[0][chunkIdx]) == OVSignalBuffer):
                chunk = self.input[0].pop()

                list_chunked = list_chunk(chunk, epoch)
                # print(list_chunked[meditation])
                note = np.mean(list_chunked[electrode])
                tempo = np.mean(list_chunked[meditation])
                client.send_message("meditation", tempo)
                client.send_message("electrode", note)
                # print(list_chunked[electrode])
                # avg = np.mean(list_chunked[meditation])

            elif(type(self.input[0][chunkIdx]) == OVSignalEnd):
                print(self.input[0].pop())


box = MyOVBox()
