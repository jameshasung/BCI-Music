import pysynth as ps
from pprint import pprint
import mido
import string
import numpy as np
import argparse
import random
import time
from src.MarkovMusic_hyunseo import MusicMatrix
from pythonosc import udp_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--ip", default="172.17.216.246",
    #                     help="The ip of the OSC server")
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=7402,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

mid = mido.MidiFile('./midi/sonata1.mid', clip=True)


def msg2dict(msg):
    result = dict()
    if 'note_on' in msg:
        on_ = True
    elif 'note_off' in msg:
        on_ = False
    else:
        on_ = None
    result['time'] = int(msg[msg.rfind('time'):].split(' ')[0].split('=')[1].translate(
        str.maketrans({a: None for a in string.punctuation})))

    if on_ is not None:
        for k in ['note', 'velocity']:
            result[k] = int(msg[msg.rfind(k):].split(' ')[0].split('=')[1].translate(
                str.maketrans({a: None for a in string.punctuation})))
    return [result, on_]


def switch_note(last_state, note, velocity, on_=True):
    # piano has 88 notes, corresponding to note id 21 to 108, any note out of this range will be ignored
    result = [0] * 88 if last_state is None else last_state.copy()
    if 21 <= note <= 108:
        result[note-21] = velocity if on_ else 0
    return result


def get_new_state(new_msg):
    new_msg, on_ = msg2dict(str(new_msg))
#     new_state = switch_note(last_state, note=new_msg['note'], velocity=new_msg['velocity'], on_=on_) if on_ is not None else last_state
#     return [new_state, new_msg['time']]
#     print(new_msg)
    return new_msg


def track2seq(track):
    # piano has 88 notes, corresponding to note id 21 to 108, any note out of the id range will be ignored
    result = []
    for i in range(1, len(track)):
        new_msg = get_new_state(track[i])
        result.append(new_msg)
    return result


def mid2arry(mid, min_msg_pct=0.1):
    tracks_len = [len(tr) for tr in mid.tracks]
    min_n_msg = max(tracks_len) * min_msg_pct
    # convert each track to nested list
    all_arys = []
    for i in range(len(mid.tracks)):
        if len(mid.tracks[i]) > min_n_msg:
            ary_i = track2seq(mid.tracks[i])
            all_arys.append(ary_i)
    return all_arys


# result_array = mid2arry(mid)
# song = []
# note_list = []
# buffer = []
# msg_idx = 0

# # track1
# for i in range(len(result_array[0])):
#     if 'note' in result_array[0][i]:
#         if result_array[0][i]['time'] == 0:
#             buffer.append(i)
#         else:
#             if buffer:
#                 for idx in buffer:
#                     note_list.append(result_array[0][idx]['note'])
#                 buffer.clear()
#             note_list.append(result_array[0][i]['note'])
#             note_list.insert(0, result_array[0][i]['time'])

#             song.append(list(note_list))
#             note_list.clear()


# for i in range(len(song)):
#     # client.send_message("note", song[i])
#     client.send_message("note", song[i])
#     time.sleep(song[i][0]/700)

result_array = mid2arry(mid)
song = []

# track1
for i in range(len(result_array[0])):
    if 'note' in result_array[0][i] and result_array[0][i]['time'] > 0:
        song.append([result_array[0][i]['note'], result_array[0]
                    [i]['time'], result_array[0][i]['velocity']])

# for i in range(0, 1000):
#     client.send_message("note", song[i])
#     # print(song[i])
#     time.sleep(song[i][1]/500)

start_note = song[0]

matrix = MusicMatrix(song)

for i in range(0, 1000):
    start_note = matrix.next_note(start_note)
    client.send_message("note", start_note[0])
    print(start_note)
    time.sleep(start_note[1]/500)
