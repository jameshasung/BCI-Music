'''
title: sound model test 2
data: meditation / electrode
controlled component: duration  
description: the duration of a note will be increased when meditation is high and decreased when vice versa. range is from 16 to 2
openvibe server settings: check 'Esence' in 'Driver properties' / downsampling 512 -> 128
resource: soundModel2.maxpat / soundModel2.xml
'''
import numpy as np
import argparse
import random
import time

from pythonosc import udp_client

global epoch
global meditation
global electrode
global duration

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
        duration = 0.0

        for chunkIdx in range(len(self.input[0])):
            if(type(self.input[0][chunkIdx]) == OVSignalHeader):
                self.signalHeader = self.input[0].pop()

                outputHeader = OVSignalHeader(self.signalHeader.startTime, self.signalHeader.endTime, [1, self.signalHeader.dimensionSizes[1]], [
                                              'Mean']+self.signalHeader.dimensionSizes[1]*[''], self.signalHeader.samplingRate)

                print(outputHeader)

            elif(type(self.input[0][chunkIdx]) == OVSignalBuffer):
                chunk = self.input[0].pop()

                list_chunked = list_chunk(chunk, epoch)
                note = np.mean(list_chunked[electrode])
                medi = np.mean(list_chunked[meditation])

                # duration setting with meditation
                if(0 < medi and medi <= 25):
                    duration = 0.0625  # 16th note
                elif(25 < medi and medi <= 50):
                    duration = 0.125  # 8th note
                elif(50 < medi and medi <= 75):
                    duration = 0.25  # 4th note
                elif(75 < medi and medi <= 100):
                    duration = 0.5  # 2nd note

                client.send_message("duration", duration)
                client.send_message("electrode", note)

            elif(type(self.input[0][chunkIdx]) == OVSignalEnd):
                print(self.input[0].pop())


box = MyOVBox()
