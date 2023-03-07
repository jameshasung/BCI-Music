#Name: Ajay Kristipati
#Andrew ID: akristip

import random
import midi
import pygame

def splitMessage(filename,chainLength):#split input into words
    f = open(filename)
    if chainLength <1: chainLength = 1
    words = []
    lines = f.readlines()
    stopWord = 'X' #used to terminate lines
    for line in lines:
        line += stopWord
        words += line.split()
    f.close()
    global start
    start = tuple(words[0:2])#starting notes
    noteDict = {}
    for i in xrange(len(words)-chainLength-1):
        word = words[i]
        #checks if complete key
        if stopWord not in tuple(words[i:i+chainLength]):#creates dictionary
            if tuple(words[i:i+chainLength]) not in noteDict:#adds key to dict
                noteDict[tuple(words[i:i+chainLength])] = [words[i+chainLength]]
            else:
               noteDict[tuple(words[i:i+chainLength])] += [words[i+chainLength]]
    return noteDict

def getStart(noteDict): #gets a random key from the dictionary
    return random.choice(noteDict.keys())

def generateMusic(filename,length,chainLength): #creates new note pattern
    noteDict = splitMessage(filename,chainLength)
    key = getStart(noteDict)
    notesSeen = []
    for i in xrange(length):
        notesSeen += [key[0]]
        if random.randint(0,10) == 6:
            key = getStart(noteDict)
        if key not in noteDict:
            key  = getStart(noteDict)
        nextWord = random.choice(noteDict[key])

        key = tuple(list(key[1:])+[nextWord])
    return ' '.join(notesSeen)

def tempoConvert(tempo): #converts tempo to format MIDI standard uses
    if tempo < 1:
        tempo = 120
    res = []
    nTempo = (60 * 1000000)/tempo
    for x in xrange(3):
        res = [nTempo%256] + res
        nTempo /= 256
    return res

def outputNotes(trk,outputFile): #outputs notes to file
    noteFile = open(outputFile,'w')
    for event in trk:
        if type(event) == type(midi.NoteOnEvent(tick=479, channel=3, data=[59, 0])):
            noteFile.write(str(event.data[0])+' ')

def generateMidi(noteList,outputPath,instrument=1,tempo=120):
    pattern = midi.Pattern()# create pattern
    track = midi.Track()# create track
    pattern.append(track)# add track to pattern
    track.append(midi.ProgramChangeEvent(tick=0,channel=0,data=[instrument]))
    track.append(midi.SetTempoEvent(tick=0, data=tempoConvert(tempo)))
    for note in noteList:# add notes to track
        rand = random.randint(0,25)
        if rand == 1: #1/25 chance of a rest
            on = midi.NoteOnEvent(tick=0, velocity=0, pitch=int(note))
        else:
            on = midi.NoteOnEvent(tick=0, velocity=random.randint(80,120),\
             pitch=int(note))
        track.append(on)
        notetypes = [tempo/2,tempo,tempo*2,tempo*3]# 8th, 4th , 1/2, dotted half
        off = midi.NoteOffEvent(tick=random.choice(notetypes), pitch=int(note))
        track.append(off)
    eot = midi.EndOfTrackEvent(tick=1)#end of track event
    track.append(eot)
    midi.write_midifile(outputPath, pattern)

def generate(chainLength,length,filename,outputPath,tracknum,instrument,tempo):
    markovSource = 'notes.txt'
    pattern = midi.read_midifile(filename)
    track = pattern[tracknum]
    outputNotes(track,markovSource)
    noteList = generateMusic(markovSource,length,chainLength).split()
    generateMidi(noteList,outputPath,instrument,tempo)
    print 'Song Generated'

def testTempoConvert():
    assert(tempoConvert(120)== [7, 161, 32])
    assert(tempoConvert(-7)== [7, 161, 32])
    assert(tempoConvert(0)== [7, 161, 32])
    assert(tempoConvert(96)== [9, 137, 104])

def testSplitMessage():
    assert(splitMessage('tests/splitmessage1.txt',2) == {('is', 'a'): ['test'], ('This', 'is'): ['a']})
    assert(splitMessage('tests/splitmessage1.txt',3) == {('This', 'is', 'a'): ['test']})
    assert( splitMessage('tests/splitmessage1.txt',0) == {('is',): ['a'], ('This',): ['is'], ('a',): ['test']})
    assert(splitMessage('tests/splitmessage2.txt',2) == {})#empty file

def testGetStart():
    dictionary = {1:2,3:4,5:6}
    assert(getStart(dictionary) in dictionary)

def testOutputNotes():
    testTrack1 = midi.Track()#empty
    outputNotes(testTrack1,'tests/outputTrack1')
    output1 = open('tests/outputTrack1')
    assert(output1.readlines() == [])

    testTrack2 = midi.Track() # 5 notes
    for i in xrange (5):
        testTrack2.append((midi.NoteOnEvent(tick=0, velocity=0, pitch=i)))
    testTrack2.append(midi.EndOfTrackEvent(tick=1))
    outputNotes(testTrack2,'tests/outputTrack2')
    output2 = open('tests/outputTrack2')
    assert(output2.readlines() ==['0 1 2 3 4 '])

def testAll():
    testTempoConvert()
    testSplitMessage()
    testGetStart()
    testOutputNotes()
