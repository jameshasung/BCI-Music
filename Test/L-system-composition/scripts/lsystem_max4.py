'''
Test to send note and duration for controling the metro in Max/MSP
This code use OSC Client and Server at the same code
'''
import sys
import turtle
import argparse
import random
import time

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

SYSTEM_RULES = {}  # generator system rules for l-system

# toggle = 0


def bang_handler(unused_addr, args):
    # toggle = 1
    client.send_message("note", 100)
    print("bang")


# OSC Client Setting
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
                    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=7402,
                    help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

# OSC Server Setting
parser = argparse.ArgumentParser()
parser.add_argument("--ip",
                    default="127.0.0.1", help="The ip to listen on")
parser.add_argument("--port",
                    type=int, default=5005, help="The port to listen on")
args = parser.parse_args()

# Server dispatcher
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/filter", bang_handler)

server = osc_server.ThreadingOSCUDPServer(
    (args.ip, args.port), dispatcher)
print("Serving on {}".format(server.server_address))

notes = [36, 38, 40, 43, 45, 48, 50, 52, 55, 57, 60, 62, 64, 67, 69, 72, 74, 76,
         79, 81, 84, 86, 88, 91, 93, 96, 98, 100, 103, 105, 108, 110, 112, 115, 117]


def derivation(axiom, steps):
    derived = [axiom]  # seed
    for _ in range(steps):
        next_seq = derived[-1]
        next_axiom = [rule(char) for char in next_seq]
        derived.append(''.join(next_axiom))
    return derived


def rule(sequence):
    if sequence in SYSTEM_RULES:
        return SYSTEM_RULES[sequence]
    return sequence


def draw_l_system(turtle, SYSTEM_RULES, seg_length, angle):
    stack = []
    message = []
    duration = 16
    currentPitch = 15
    i = 0
    for command in SYSTEM_RULES:
        turtle.pd()
        if command in ["F", "G", "R", "L"]:
            if SYSTEM_RULES[i+1] is not 'F':
                message = [notes[currentPitch], duration]
                client.send_message("message", message)
                duration = 16
            else:
                if duration >= 2:
                    duration /= 2
            turtle.forward(seg_length)

        elif command == "f":
            turtle.pu()  # pen up - not drawing
            turtle.forward(seg_length)
        elif command == "+":
            turtle.right(angle)
            # max
            currentPitch += 1
            # max
        elif command == "-":
            turtle.left(angle)
            # max
            currentPitch -= 1
            # max
        elif command == "[":
            stack.append((turtle.position(), turtle.heading()))
        elif command == "]":
            turtle.pu()  # pen up - not drawing
            position, heading = stack.pop()
            turtle.goto(position)
            turtle.setheading(heading)
        i += 1


def set_turtle(alpha_zero):
    r_turtle = turtle.Turtle()  # recursive turtle
    r_turtle.screen.title("L-System Derivation")
    r_turtle.speed(0)  # adjust as needed (0 = fastest)
    r_turtle.setheading(alpha_zero)  # initial heading
    return r_turtle


def drawing_macro():
    rule = "F->F-F+F+FF-F-F+F"
    key, value = rule.split("->")
    SYSTEM_RULES[key] = value

    axiom = "F-F-F-F"
    iterations = 3
    model = derivation(axiom, iterations)

    # rule = "X->F[+X][-X]FX"
    # key, value = rule.split("->")
    # SYSTEM_RULES[key] = value
    # rule = "F->FF"
    # key, value = rule.split("->")
    # SYSTEM_RULES[key] = value

    # axiom = "X"
    # iterations = 6
    # model = derivation(axiom, iterations)

    segment_length = 5
    alpha_zero = 90.0
    angle = 90.0

    # Set turtle parameters and draw L-System
    r_turtle = set_turtle(alpha_zero)  # create turtle object
    turtle_screen = turtle.Screen()  # create graphics window
    turtle_screen.screensize(1500, 1500)
    draw_l_system(r_turtle, model[-1], segment_length, angle)  # draw model
    turtle_screen.exitonclick()


def main():
    drawing_macro()


if __name__ == "__main__":
    try:
        main()
        server.serve_forever()
    except BaseException:
        sys.exit(0)
