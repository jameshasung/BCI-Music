#Name: Ajay Kristipati
#Andrew ID: akristip

import random
import math
import pygame

def createAlbumArt(filepath):
    filename= open(filepath)
    notes= filename.readlines()
    notes= notes[0].split() # split notes into list of strings
    notes= [int(i) for i in notes] #converts from strings to ints
    notes= normalizeValues(notes) #distibutes notes more evenly
    notes= pad(notes) #pads notes so they can be converted to colors
    colors= []
    (colors, artSize)= notesToColors(notes,colors)
    surf= pygame.Surface((artSize,artSize))
    colorizeSurface(surf,colors,artSize)
    surf= pygame.transform.scale(surf,(200,200))
    pygame.image.save(surf,'art.png')
    print 'Generated Image'

def normalizeValues(notes):
    if len(notes) < 2: return notes
    maxNote= float(max(notes))
    minNote= float(min(notes))
    if minNote == maxNote: maxNote += 1
    notes= [int(((i-minNote)/(maxNote-minNote)*255)) for i in notes]
    return notes

def pad(notes):
    while len(notes)%3: #pad with zeroes
        notes += [random.randint(0,255)]
    return notes

def notesToColors(notes,colors):
    for x in xrange(0,len(notes),3): #creates list of colors
        colors += [tuple(notes[x:x+3])]
    artSize= int(math.ceil(len(colors)**0.5))#calculates size of art
    while len(colors) < artSize**2: #loops colors to fill image
        colors += colors
        #print len(colors) > artSize**2
    return (colors,artSize)

def colorizeSurface(surf,colors,artSize):#adds colors to surface
    for x in xrange(artSize):
        for y in xrange(artSize):
            color= colors.pop()
            surf.set_at((x,y),color)
    return artSize


def testNormalizeValues():
    assert(normalizeValues([0,0,0,0,0]) == [0, 0, 0, 0, 0]) #all same
    assert(normalizeValues([]) == [])#empty
    assert (normalizeValues(range(5)) == [0, 63, 127, 191, 255]) #normal case

def testPad():
    assert(pad([]) == []) # empty list
    assert(len(pad(['x'])) == 3) #size 1 list
    assert(pad([1,2,3]) == [1,2,3]) # size 3 list

def testNotesToColors():
    assert(notesToColors([12,34,67],[]) == ([(12, 34, 67)], 1))
    assert(notesToColors([12,34,67,89,10,11],[]) == ([(12, 34, 67), (89, 10, 11)\
    , (12, 34, 67), (89, 10, 11)], 2))
    assert(notesToColors([],[]) == ([],0))

def testAll():
    testNormalizeValues()
    testPad()
    testNotesToColors()
