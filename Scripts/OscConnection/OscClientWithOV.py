"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import udp_client


class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)

    def initialize(self):
        print('Initialize Hello World Script')
        # nop
        return

    def process(self):
        # print the string specified in the box configuration.
        # 'Message' is the name of the config entry.
        # print(self.setting['Message'])
        if __name__ == "__main__":
            parser = argparse.ArgumentParser()
            parser.add_argument("--ip", default="127.0.0.1",
                                help="The ip of the OSC server")
            parser.add_argument("--port", type=int, default=7402,
                                help="The port the OSC server is listening on")
            args = parser.parse_args()

            client = udp_client.SimpleUDPClient(args.ip, args.port)

            client.send_message("/filter", "Osc testing with OV")

    def uninitialize(self):
        print('Uninitialize Hello World Script')
        # nop
        return


box = MyOVBox()
