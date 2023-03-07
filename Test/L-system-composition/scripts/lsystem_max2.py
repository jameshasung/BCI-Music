import sys
import turtle
import argparse
import random
import time

from pythonosc import udp_client

SYSTEM_RULES = {}  # generator system rules for l-system
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
                    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=7402,
                    help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)

GMajor = {'G': 67, 'A': 69, 'B': 71, 'C': 72, 'E': 76, 'F#': 78, 'G5': 79}


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
    for command in SYSTEM_RULES:
        turtle.pd()
        # max
        # print("command: " + command)  # display each command
        # max
        if command in ["F", "G", "R", "L"]:
            turtle.forward(seg_length)
            # max
            # print(turtle.pos())
            # print(int(turtle.ycor()/35))
            idx = int(turtle.ycor()/35)
            client.send_message("note", list(GMajor.values())[idx])
            time.sleep(0.5)
            # max
        elif command == "f":
            turtle.pu()  # pen up - not drawing
            turtle.forward(seg_length)
        elif command == "+":
            turtle.right(angle)
        elif command == "-":
            turtle.left(angle)
        elif command == "[":
            stack.append((turtle.position(), turtle.heading()))
        elif command == "]":
            turtle.pu()  # pen up - not drawing
            position, heading = stack.pop()
            turtle.goto(position)
            turtle.setheading(heading)


def set_turtle(alpha_zero):
    r_turtle = turtle.Turtle()  # recursive turtle
    r_turtle.screen.title("L-System Derivation")
    r_turtle.speed(0)  # adjust as needed (0 = fastest)
    r_turtle.setheading(alpha_zero)  # initial heading
    return r_turtle


def drawing_macro():
    # rule = "F->F-F+F+F-F-FF+F+FF-F-F+F+F-F"
    # key, value = rule.split("->")
    # SYSTEM_RULES[key] = value
    rule = "F->F+F-FF+FF-F+F"
    key, value = rule.split("->")
    SYSTEM_RULES[key] = value

    axiom = "F"
    iterations = 1
    model = derivation(axiom, iterations)

    segment_length = 50
    alpha_zero = 45.0
    angle = 90.0

    # Set turtle parameters and draw L-System
    r_turtle = set_turtle(alpha_zero)  # create turtle object
    turtle_screen = turtle.Screen()  # create graphics window
    turtle_screen.screensize(1500, 1500)
    draw_l_system(r_turtle, model[-1], segment_length, angle)  # draw model
    turtle_screen.exitonclick()


def main():
    # rule_num = 1
    # while True:
    #     rule = input("Enter rule[%d]:rewrite term (0 when done): " % rule_num)
    #     if rule == '0':
    #         break
    #     key, value = rule.split("->")
    #     SYSTEM_RULES[key] = value
    #     rule_num += 1

    # axiom = input("Enter axiom (w): ")
    # iterations = int(input("Enter number of iterations (n): "))

    # # axiom (initial string), nth iterations
    # model = derivation(axiom, iterations)

    # segment_length = int(input("Enter step size (segment length): "))
    # alpha_zero = float(input("Enter initial heading (alpha-0): "))
    # angle = float(input("Enter angle increment (i): "))

    # # Set turtle parameters and draw L-System
    # r_turtle = set_turtle(alpha_zero)  # create turtle object
    # turtle_screen = turtle.Screen()  # create graphics window
    # turtle_screen.screensize(1500, 1500)
    # draw_l_system(r_turtle, model[-1], segment_length, angle)  # draw model
    # turtle_screen.exitonclick()
    drawing_macro()


if __name__ == "__main__":
    try:
        main()
    except BaseException:
        sys.exit(0)
