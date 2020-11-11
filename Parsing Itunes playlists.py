"""
The main task is to find duplicates within the whole library of music tracks.
Tackles: plistlib, matplotlib, numpy.
"""

import plistlib
from matplotlib import pyplot
import numpy as np
import sys
import re
import argparse


def findDuplicates(fileName):
    """Takes a file and search for duplicates.
    Return whether .txt with duplicates or print that no duplicates was found"""
    print('Finding duplicate tracks in $s...' % fileName)
    # read in a playlist
    plist = plistlib.readPlist(fileName)
    # get the tracks from the Track directory
    tracks = plist['Tracks']
    # create a track name dictionary
    trackNames = {}
    # iterate through tracks
    for trackID, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Duration']
            # look for existing entries
            if name in trackNames:
                # if both a name and duration match, increment the count
                # round the track length to the nearest second
                if duration // 1000 == trackNames[name][0] // 1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                # add dict entry as tuple (duration, entry)
                trackNames[name] = (duration, 1)
        except:
            # ignore
            pass

    # store duplicates as (name, count) tuples
    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))

    # save duplicates to a file
    if len(dups) > 0:
        print('Found %d duplicates. Track names saved to dup.txt' % len(dups))
    else:
        print('No duplicate tracks found')

    f = open('dups.txt', 'w')
    for val in dups:
        f.write("[%d] %s\n" % (val[0], val[1]))
    f.close()


def findCommonTracks(fileNames):
    """Takes several files and looking for intersection of the same tracks.
    Return whether a .txt with intersections or a string with no common tacks info"""
    # a list of sets of track names
    trackNameSets = []
    for fileName in fileNames:
        # create a new set
        trackNames = set()

        # Next two lines contain original code from the book, nonetheless I got an DeprecationError, so I change it
        # read in playlist
        # plist = plistlib.readPlist(fileName)

        # read a playlist v2, where 'rb' stands for 'read binary'
        with open(fileName, 'rb') as f:
            plist = plistlib.load(f)

        # get the tracks
        tracks = plist['Tracks']
        # iterate through the tracks
        for trackID, track in tracks.items():
            try:
                # add the track name to a set
                trackNames.add(track['Name'])
            except:
                pass
        # add to a list
        trackNameSets.append(trackNames)

    # get the set of common tracks
    commonTracks = set.intersection(*trackNameSets)

    # write a file
    if len(commonTracks) > 0:
        # originally: f = open('common.txt', 'w'), besides I got a TypeError, due to the file format is bytes
        f = open('common.txt', 'wb')
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s.encode("UTF-8"))
        f.close()
        print("%d common tracks found!" % len(commonTracks))
    else:
        print('No common tracks found!')


def plotStats(fileName):
    """Takes data and based on it fulfilled graphs"""

    # DeprecationWarning, next two lines from the book, the code after it mine
    # read in a playlist
    # plist = plistlib.readPlist(fileName)

    # read a playlist v2
    with open(fileName, 'rb') as f:
        plist = plistlib.load(f)

    # get the tracks from the playlist
    tracks = plist['Tracks']

    # create lists of song rating and track duration
    ratings = []
    durations = []

    # iterate through the tracks
    for trackID, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            pass

        # ensure that valid data was collected
        if ratings == [] or durations == []:
            print('No valid Album Rating or Total Time data in %s' % fileName)
            return

    # scatter plot
    x = np.array(durations, np.int32)

    # convert to minutes
    x = x/60000.0
    y = np.array(ratings, np.int32)
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x, y, 'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    # plot histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    # show plot
    pyplot.show()

def main():

    # create parser
    descStr = """
    This program analyzes playlist files (.xml) exported from iTunes.
    """
    parser = argparse.ArgumentParser(description=descStr)
    # add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()

    # add expective arguments
    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup', dest='plFileD', required=False)

    # parse arguments
    args = parser.parse_args()

    if args.plFiles:
        # find common tasks
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        # find duplicates
        findDuplicates(args.FileD)
    else:
        print("These are not the tracks you are looking for")


if __name__ == '__main__':
    main()

