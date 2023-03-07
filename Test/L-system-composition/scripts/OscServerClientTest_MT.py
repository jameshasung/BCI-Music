"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

from pythonosc import udp_client
from multiprocessing import Process, Value

import time


def bang_handler(unused_addr, args, volume):
    # client.send_message("test", 100)
    args[0].value = 100
    print("bang: ", args[0].value)


def server_func(num):
    # OSC Server Setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    # Server dispatcher
    global dispatcher
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/filter", bang_handler, num)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))

    server.serve_forever()


def main(num):
    # OSC Client Setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=7402,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    for i in range(0, 100):
        print("[", i, "]: ", num.value)
        if num.value == 100:
            client.send_message("test", 100)
            num.value = 0
        else:
            client.send_message("test", i)
        time.sleep(1)
        i += 1


if __name__ == "__main__":
    num = Value('i', 0)
    p = Process(target=server_func, args=(num,))
    c = Process(target=main, args=(num,))
    p.start()
    # p.join()
    c.start()
    # c.join()
