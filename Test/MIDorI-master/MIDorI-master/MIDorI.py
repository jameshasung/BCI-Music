#Name: Ajay Kristipati
#Andrew ID: akristip

import sys, pygame
from Tkinter import *
import tkFileDialog as filedialog
import random
import midi
import generator
import albumArt
from PIL import Image, ImageTk
import os

def findFirstNonEmptyTrack(): #finds the first track with notes in it
    pat = midi.read_midifile(c.d.inputFile.get())
    for track in xrange(len(pat)):
        if not isEmptyTrack(track,pat):
            return track
    else: return -1

#checks if track is empty
def isEmptyTrack(track, pat):
    for event in pat[track]:
        if type(event) == type(midi.NoteOnEvent(tick=0, channel=0,\
        data=[0, 0])):
            return False
    return True

def getInputFile(): #gets the file to seed markov chain
    fpath=filedialog.askopenfilename(filetypes = (("MIDI Files", "*.mid")\
    ,("All files", "*.*") ))
    #replaces text
    c.d.inputPathEntry.delete(0,END)
    c.d.inputPathEntry.insert(0,fpath)
    c.d.inputFile.set(fpath)
    #resets track number
    if(fpath != ''):
        c.d.track.set(findFirstNonEmptyTrack())

def getOutputFile(): #gets file to output music to
    fpath=filedialog.asksaveasfilename(defaultextension='.mid', filetypes =\
     (("MIDI Files","*.mid"),("All Files","*.*")))
    c.d.outputPathEntry.delete(0,END)
    c.d.outputPathEntry.insert(0,fpath)
    c.d.outputFile.set(fpath)

def initVariables(root):
    c.d.inputFile=StringVar() #input Filename
    c.d.outputFile=StringVar() #output Filename
    #list of instruments
    c.d.instruments={'Piano':1,'Glockenspiel':10,'Music Box':11,'Organ':17,\
     'Acoustic Guitar':25,'Distortion Guitar':31,'Harp':46,\
     'Violin':41,'Trumpet':57}
    c.d.instrumentName=StringVar() #name of instrument
    c.d.instrumentName.set('Harp')
    c.d.instrument=IntVar() #instrument number
    c.d.instrument.set(46) #Harp
    c.d.chainLength=IntVar()#length of markov chain
    c.d.chainLength.set(4)
    c.d.songLength=IntVar()#length of output
    c.d.defaultSongLength=200
    c.d.songLength.set(c.d.defaultSongLength)
    c.d.tempo=IntVar()#tempo
    c.d.tempo.set(120)#midi standard tempo defaults at 120
    c.d.track=IntVar() #track to input notes from
    c.d.track.set(1)

def init(root): #Sets up UI and global vars
    initVariables(root) #sets up variables
    #sets up gui
    Label(root, text="Input Path: ").grid(row=0)
    Label(root, text="Output Path: ").grid(row=1)
    c.d.inputPathEntry=Entry(root,textvariable=c.d.inputFile)
    c.d.outputPathEntry=Entry(root,textvariable=c.d.outputFile)
    c.d.inputPathEntry.grid(row=0, column=1)
    c.d.outputPathEntry.grid(row=1, column=1)
    inFileGetButton=Button(root, text="Open MIDI File", command=getInputFile)
    inFileGetButton.grid(row=0,column=2)
    outFileGetButton=Button(root, text="Save Path", command=getOutputFile)
    outFileGetButton.grid(row=1,column=2)
    c.d.inputPlayButton=Button(root, text="Play", command=playInput)
    c.d.inputPlayButton.grid(row=0,column=3)
    c.d.outputPlayButton=Button(root, text="Play", command=playOutput)
    c.d.outputPlayButton.grid(row=1,column=3)
    c.d.optionsButton=Button(root, text='Options', command=openOptions)
    c.d.optionsButton.grid(row=2,column=2,columnspan=2)
    c.d.generateButton=Button(root, text='Generate', command=generate)
    c.d.generateButton.grid(row=2,columnspan=2)

def generate():
    chainLength=c.d.chainLength.get() #Get variables
    songLength=c.d.songLength.get()
    filename=c.d.inputFile.get()
    outputPath=c.d.outputFile.get()
    tracknum=c.d.track.get()
    instrument=c.d.instrument.get()
    tempo=c.d.tempo.get()
    inPattern=midi.read_midifile(filename) #check if track is empty
    if isEmptyTrack(tracknum,inPattern):
        tracknum = findFirstNonEmptyTrack()
        c.d.track.set(tracknum)
    generator.generate(chainLength,songLength,filename,outputPath,tracknum,\
    instrument,tempo) #generate song
    outPattern=midi.read_midifile(outputPath) #generate Art
    trk=outPattern[0]
    generator.outputNotes(trk,'Onotes.txt')
    albumArt.createAlbumArt('Onotes.txt')
    pic=Image.open('art.png')
    art=ImageTk.PhotoImage(pic)
    c.d.artWindow=Label(image=art)
    c.d.artWindow.grid(row=3,columnspan=4)
    c.d.artWindow.image=art

def openOptions(): #Options window UI
    top=Toplevel()
    Label(top, text="Chain Length: ").grid(row=0)
    Label(top, text="Instrument: ").grid(row=1)
    Label(top, text="Song Length: ").grid(row=2)
    Label(top, text="Tempo: ").grid(row=3)
    Label(top, text="Input Track: ").grid(row=4)
    lengths=range(2,10) #possible chain lengths
    c.d.chainLengthPicker=apply(OptionMenu,(top,c.d.chainLength)+tuple(lengths))
    c.d.chainLengthPicker.grid(row=0,column=1)
    instruments=c.d.instruments.keys()
    c.d.instrumentPicker=OptionMenu(top,c.d.instrumentName,*instruments,\
    command=setInstrument)
    c.d.instrumentPicker.grid(row=1,column=1)
    c.d.songLengthPicker=Entry(top,textvariable=c.d.songLength,\
    validatecommand=validateLength)
    c.d.songLengthPicker.grid(row=2,column=1)
    c.d.tempoPicker=Entry(top,textvariable=c.d.tempo,\
    validatecommand=validateTempo)
    c.d.tempoPicker.grid(row=3,column=1)
    tracks=[1] #default track
    if(c.d.inputFile.get() !=''):
        pat=midi.read_midifile(c.d.inputFile.get())
        tracks=range(len(pat))
    c.d.trackPicker=apply(OptionMenu,(top,c.d.track)+tuple(tracks))
    c.d.trackPicker.grid(row=4,column=1)

def setInstrument(instrument):#called by options menu
    c.d.instrument.set(c.d.instruments[instrument])

def validateLength(): #restricts song length
    if c.d.songLength.get() not in range(16,2048):
        c.d.songLength.set((c.d.defaultSongLength)) #default song length
        return False
    return True

def validateTempo(): #restrics tempo
    if c.d.tempo.get() not in range(16,1024):
        c.d.tempo.set(120)# default tempo
        return False
    return True

def playInput(): #plays the input midi
    fpath=c.d.inputFile.get()
    if not fpath=='' and ('.mid' in fpath): #makes sure file is valid
        pygame.mixer.music.load(fpath)
        pygame.mixer.music.play()
        c.d.inputPlayButton['text']="Stop"
        c.d.inputPlayButton['command']=stopInput
def stopInput(): #stops playing input midi
    pygame.mixer.music.stop()
    c.d.inputPlayButton['text']="Play"
    c.d.inputPlayButton['command']=playInput

def playOutput(): #plays output midi
    fpath=c.d.outputFile.get()
    if not fpath=='' and ('.mid' in fpath): #makes sure file is chosen
        pygame.mixer.music.load(fpath)
        pygame.mixer.music.play()
        c.d.outputPlayButton['text']="Stop"
        c.d.outputPlayButton['command']=stopOutput
def stopOutput(): #stops playing output midi
    pygame.mixer.music.stop()
    c.d.outputPlayButton['text']="Play"
    c.d.outputPlayButton['command']=playOutput

def run():
    # create the root and the canvas
    global c
    root=Tk()
    c=Canvas(root, width=600, height=400)
    # Set up c data and call init
    class Struct: pass
    c.d=Struct()
    init(root)
    # set up events
    c.d.root=root
    # and launch the app
    root.mainloop()
    pygame.mixer.music.stop()
def cleanUp():
    if os.path.isfile('art.png'):
        os.remove('art.png')
    if os.path.isfile('notes.txt'):
        os.remove('notes.txt')
    if os.path.isfile('Onotes.txt'):
        os.remove('Onotes.txt')

def testIsEmptyTrack():
    pat1 = midi.read_midifile('tests/trk15empty.mid')
    assert(isEmptyTrack(15,pat1) == True)
    pat2 =  midi.read_midifile('tests/empty.mid')
    assert(isEmptyTrack(0,pat2) == True)
    pat3 = midi.read_midifile('tests/notEmpty.mid')
    assert(isEmptyTrack(1,pat3)== False)
def testFindFirstNonEmptyTrack():
    c.d.inputFile.set('tests/trk15empty.mid')
    assert(findFirstNonEmptyTrack() == 1)
    c.d.inputFile.set('tests/empty.mid')
    assert(findFirstNonEmptyTrack() == -1)
    c.d.inputFile.set('tests/noTempo.mid')
    assert(findFirstNonEmptyTrack() == 0)
def testAll():
    testIsEmptyTrack()
    testFindFirstNonEmptyTrack()
pygame.init()
run()
cleanUp()
