'''
Test to send note and duration for controling the metro in Max/MSP
This code use OSC Client and Server at the same code
This code use Multithreading between Server and Client
This code use EEG information for controling the music parameters
'''
import sys
import turtle
import argparse
import math
import random
import time

from pythonosc import dispatcher
from pythonosc import osc_server

from pythonosc import udp_client
from multiprocessing import Process, Value

SYSTEM_RULES = {}  # generator system rules for l-system

Cmajor_pentatonic = [36, 38, 40, 43, 45, 48, 50, 52, 55, 57, 60, 62, 64, 67, 69, 72, 74, 76,
                     79, 81, 84, 86, 88, 91, 93, 96, 98, 100, 103, 105, 108, 110, 112, 115, 117]

Cminor_pentatonic = [36, 39, 41, 43, 46, 48, 51, 53, 55, 58, 60, 63, 65, 67, 70, 72, 75,
                     77, 79, 82, 84, 87, 89, 91, 94, 96, 99, 101, 103, 106, 108, 111, 113, 115, 118]

scales = [Cmajor_pentatonic, Cminor_pentatonic]

durations = [2, 4, 8, 16, 32]

velocities = [0, 127, 107, 87]

colors = ['red', 'blue', 'green']

total_iteration = 3

lsystems = [{'rule_num': 1, 'rule': "F->FF+F-F+F+FF", 'axiom': "F+F+F+F",
             'segment_length': 5, 'alpha_zero': 0.0, 'angle': 90.0},
            {'rule_num': 1, 'rule': "F->F-F+F+FF-F-F+F", 'axiom': "F-F-F-F",
             'segment_length': 5, 'alpha_zero': 0.0, 'angle': 90.0},
            {'rule_num': 1, 'rule': "F->F+F-F-F+F", 'axiom': "-F",
             'segment_length': 5, 'alpha_zero': 90.0, 'angle': 90.0},
            {'rule_num': 2, 'rule': ["L->L+R++R-L--LL-R+", "R->-L+RR++R+L--L-R"], 'axiom': "L",
             'segment_length': 5, 'alpha_zero': 60.0, 'angle': 60.0},
            {'rule_num': 2, 'rule': ["X->F-[[X]+X]+F[+FX]-X", "F->FF"], 'axiom': "X",
             'segment_length': 5, 'alpha_zero': 90.0, 'angle': 22.5},
            {'rule_num': 2, 'rule': ["X->F[+X][-X]FX", "F->FF"], 'axiom': "X",
             'segment_length': 5, 'alpha_zero': 90.0, 'angle': 45.0}]


def initiate_max(client):
    client.send_message('initiation', 'bang')


def bang_handler(unused_addr, args, volume):
    args[0].value = 1


def scale_handler(unused_addr, args, alpha_average):
    print("Alpha average: ", alpha_average)

    if alpha_average >= 50.0:
        args[0].value = 0
        print("Major Scale selected!")
    else:
        args[0].value = 1
        print("Minor Scale selected!")


def server_func(toggle, scale):
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
    dispatcher.map("/filter", bang_handler, toggle)
    dispatcher.map("/average", scale_handler, scale)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))

    server.serve_forever()


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


def draw_l_system(turtle, model, seg_length, angle, toggle, client, scale):
    stack = []
    pitch_stack = []
    midiout = []
    play = [1, 0, 0, 0]
    currentDuration = 1
    currentPitch = 5
    currentVelocity = 1
    currentPlay = 0
    initialPitch = 0

    for idx in range(0, total_iteration):
        i = 0
        client.send_message("record"+str(idx+1), 1)
        client.send_message("channel", idx)
        client.send_message("play", play)
        initialPitch = currentPitch
        print("Play loop:", idx+1)

        SYSTEM_RULES = model[idx][-1]
        turtle.color(colors[idx])

        for command in SYSTEM_RULES:
            turtle.pd()

            if command in ["F", "G", "R", "L"]:
                while toggle.value == 0:
                    continue
                toggle.value = 0

                if i+1 == len(SYSTEM_RULES):
                    break

                elif SYSTEM_RULES[i+1] is not 'F':
                    currentVelocity = idx+1

                elif SYSTEM_RULES[i+1] is 'F':
                    currentVelocity = 0

                midiout = [scales[scale.value][currentPitch],
                           durations[currentDuration], velocities[currentVelocity]]
                client.send_message("midiout", midiout)

                turtle.forward(seg_length)

            elif command == "f":
                turtle.pu()  # pen up - not drawing
                turtle.forward(seg_length)
            elif command == "+":
                turtle.right(angle)

                currentPitch += 1
                if currentPitch+1 > len(scales[scale.value]):
                    currentPitch = initialPitch

            elif command == "-":
                turtle.left(angle)

                currentPitch -= 1
                if currentPitch < 0:
                    currentPitch = initialPitch

            elif command == "[":
                stack.append((turtle.position(), turtle.heading()))
                pitch_stack.append(currentPitch)
            elif command == "]":
                turtle.pu()  # pen up - not drawing
                position, heading = stack.pop()
                currentPitch = pitch_stack.pop()
                turtle.goto(position)
                turtle.setheading(heading)

            i += 1

        currentPitch += 10
        currentDuration += 1
        currentVelocity += 1
        currentPlay += 1
        play[currentPlay] = 1

        client.send_message("mainplay", 'bang')
        client.send_message("loopset", 'bang')
        time.sleep(1)
        client.send_message("record"+str(idx+1), 0)

    client.send_message("play", play)
    return


def set_turtle(alpha_zero):
    r_turtle = turtle.Turtle()  # recursive turtle
    r_turtle.screen.title("L-System Music Playing")
    r_turtle.speed(0)  # adjust as needed (0 = fastest)
    r_turtle.setheading(alpha_zero)  # initial heading
    return r_turtle


def drawing_macro(toggle, client, scale, lsys):

    lsys_idx = lsys - 1

    if lsystems[lsys_idx]['rule_num'] > 1:
        for i in range(0, lsystems[lsys_idx]['rule_num']):
            rule = lsystems[lsys_idx]['rule'][i]
            key, value = rule.split("->")
            SYSTEM_RULES[key] = value
    else:
        rule = lsystems[lsys_idx]['rule']
        key, value = rule.split("->")
        SYSTEM_RULES[key] = value

    axiom = lsystems[lsys_idx]['axiom']
    segment_length = lsystems[lsys_idx]['segment_length']
    alpha_zero = lsystems[lsys_idx]['alpha_zero']
    angle = lsystems[lsys_idx]['angle']

    model = []
    for i in range(0, total_iteration):
        model.append(derivation(axiom, i+1))

    # Set turtle parameters and draw L-System
    r_turtle = set_turtle(alpha_zero)  # create turtle object
    turtle_screen = turtle.Screen()  # create graphics window
    turtle_screen.screensize(1500, 1500)
    turtle_screen.bgcolor('black')
    draw_l_system(r_turtle, model,
                  segment_length, angle, toggle, client, scale)  # draw model
    client.send_message("mainplay", 'bang')
    turtle_screen.exitonclick()
    return


def main(toggle, scale, mode, lsys):
    # OSC Client Setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=7402,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    initiate_max(client)

    drawing_macro(toggle, client, scale, lsys)
    return


if __name__ == "__main__":
    toggle = Value('i', 0)
    scale = Value('i', 3)
    p = Process(target=server_func, args=(toggle, scale,))
    p.start()
    time.sleep(1)

    try:
        print("\nWhich mode do you want to play?")
        print("1. Alpha Feedback mode")
        print("2. Music only mode")

        mode = input("==> Choose a mode above(1 or 2, q to quit) : ")
        if mode is "1":
            print("Please turn the OpenVibe on")
            while scale.value == 3:
                time.sleep(1)
                continue
        elif mode is "2":
            print("\nWhich scale do you want to play?")
            print("1. Major")
            print("2. Minor")
            s = input("==> Choose a scale above(1 or 2) : ")
            if s is "1":
                scale.value = 0
            elif s is "2":
                scale.value = 1
        elif mode is "q":
            print("Good Bye!")
            p.kill()
            sys.exit(0)

        print("\nWhich lsystem do you want to play?")
        lsys = int(input("==> Choose from 1 to 6 : "))

        c = Process(target=main, args=(toggle, scale, mode, lsys))
        c.start()
        c.join()
        c.kill()
        p.kill()
        sys.exit(0)
    except BaseException:
        sys.exit(0)
