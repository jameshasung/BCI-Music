import numpy as np


def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]


class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.signalHeader = None

    def process(self):
        for chunkIdx in range(len(self.input[0])):
            if(type(self.input[0][chunkIdx]) == OVSignalHeader):
                self.signalHeader = self.input[0].pop()

                outputHeader = OVSignalHeader(self.signalHeader.startTime, self.signalHeader.endTime, [1, self.signalHeader.dimensionSizes[1]], [
                                              'Mean']+self.signalHeader.dimensionSizes[1]*[''], self.signalHeader.samplingRate)

                # self.output[0].append(outputHeader)
                print(outputHeader)

            elif(type(self.input[0][chunkIdx]) == OVSignalBuffer):
                chunk = self.input[0].pop()

                list_chunked = list_chunk(chunk, 8)
                avg = np.mean(list_chunked[0])
                print(avg)

            elif(type(self.input[0][chunkIdx]) == OVSignalEnd):
                print(self.input[0].pop())


box = MyOVBox()
