import turtle
import argparse
import time

from pythonosc import udp_client

GMajor = {'G': 67, 'A': 69, 'B': 71, 'C': 72, 'E': 76, 'F#': 78, 'G5': 79}

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
                    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=7402,
                    help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

canvas = turtle.Screen()
canvas.setup(1000, 1000)
turtle.speed(130)
turtle.pensize(1)
turtle.pencolor('white')
turtle.bgcolor('black')

pitch = []
velocity = []


def drawline(length):
    for task in instructions:
        if task == "F":
            turtle.forward(length)
            # print(turtle.pos())
            # client.send_message("pitch", turtle.ycor())
            pitch.append(turtle.ycor())
            velocity.append(turtle.ycor())
            # print("pitch",pitch)
            # print("volumn", velocity)
        elif task == "+":
            turtle.right(60)
        elif task == "-":
            turtle.left(60)


def min_max_normalize(lst):
    normalized = []

    for value in lst:
        normalized_num = (value - min(lst)) / (max(lst) - min(lst))
        normalized.append(normalized_num)

    return normalized


if __name__ == "__main__":
    length = 5
    instructions = "F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F-F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F-F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F-F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F-F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F-F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F-F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F-F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F-F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F-F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F-F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F"

    drawline(length)
    pitch = min_max_normalize(pitch)
    # print(pitch)
    for x in range(len(pitch)):
        idx = int(x)
        print(x)
        # client.send_message("pitch", Gmajor[x])
        # client.send_message("velocity", velocity[x])
        # time.sleep(0.5)

    turtle.done()
