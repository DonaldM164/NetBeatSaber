import os, sys

from os import listdir
from os.path import isfile, join, isdir
from pathlib import Path
import collections 
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import itertools 
import numpy as np

from collections import Iterable
from model.util import secondsPerMeasure


class DataManager():
    def __init__(self, songsPath=None, formattedDataPath=None):
        self.songsPath = songsPath
        self.formattedDataPath = formattedDataPath
     

    def verifyPaths(self):
        if self.songsPath is None:
            self.songsPath = str(Path(os.getcwd() + "/data/customLevels/").resolve())
            print(self.songsPath)
        if self.formattedDataPath is None:
            self.formattedDataPath = str(Path(os.getcwd() + "/data/formattedData/").resolve())
            
    def generateModelData(self):
        self.verifyPaths()
        
        songFolders = [f for f in listdir(self.songsPath) if isdir(join(self.songsPath, f))]
        
        #Make Directories
        formattedFolders = [f for f in listdir(self.formattedDataPath) if isdir(join(self.songsPath, f))]
        if len(formattedFolders) != len(songFolders):
            toAdd = list(filter(lambda x: not x in formattedFolders, songFolders))
            for a in toAdd:
                os.mkdir(self.formattedDataPath + r"\\" + a)
                formattedFolders.append(a)
                
        for folder in songFolders:
            fPath = self.songsPath + r"\\" + folder
            contents = [f for f in listdir(fPath) if isfile(join(fPath, f))]
            dataFiles = list(filter(lambda x: x.split(".")[1] == "dat", contents))
            for d in dataFiles:
                with open(fPath + r"\\" + d, 'r') as f:
                    data = json.loads(f.read())
                    
                    json.dump(data, open(self.formattedDataPath + r"\\" + folder + "\\" + d, "w+"), indent=4)
            
            
            print("Generating for " + folder)
            try:
                self.extractBeatmapData(self.formattedDataPath + r"\\" + folder)
            except:
                print("Error trying to parse data for " + folder + ", moving on..")

    def extractBeatmapData(self, beatmapPath):
        with open(beatmapPath + r"\\modelData.json", "w+") as f:
            dataFiles = [f for f in listdir(beatmapPath) if isfile(join(beatmapPath, f))]
            mData = dict()
            
            infoData = json.load(open(beatmapPath + r"\\info.dat", 'r'), encoding='utf-8')
            infoDict = dict()
            infoDict["_beatsPerMinute"] = infoData["_beatsPerMinute"]
            beatsPerMinute = infoDict["_beatsPerMinute"]
            beatmaps = dict()
            for mSet in infoData["_difficultyBeatmapSets"]:
                for map in mSet["_difficultyBeatmaps"]:
                    difficulty = map["_difficulty"]
                    beatmaps[difficulty] = map
                infoDict["beatmaps"] = beatmaps
                mData["general"] = infoDict
            
            secPerMes = secondsPerMeasure(beatsPerMinute) 
            
            #Let's try 8 measures at a time
            secPerMes = secPerMes * 8
            print("seconds per measure = " + str(secPerMes))
            difficultyDict = dict()
            for d in dataFiles: 
                if d != "modelData.json" and d.lower() != "info.dat":
                    fileData = json.load(open(beatmapPath + r"\\" + d, 'r'), encoding='utf-8')
                    
                    
                    eventData = dict()
                    eventData["total_events"] = len(fileData["_events"])
                        
                    slashData = dict()
                    slashData["total_slashes"] = len(fileData["_notes"])
                        
                    slashVariations = set((x['_lineIndex'],x['_lineLayer'], x['_type'], x['_cutDirection']) for x in fileData["_notes"])
                        
                    variations = set((x['_type'],x['_value']) for x in fileData["_events"])
                        
                    eventTotals = dict()
                    slashTotals = dict()

                    for var in variations:
                        t = var[0]
                        v = var[1]
                        key = str(t) + " " + str(v)
                        eventTotals[key] = len(list(filter(lambda x: x["_type"] == t and x["_value"] == v, fileData["_events"])))
                        
                    for var in slashVariations:
                        index = var[0]
                        layer = var[1]
                        type = var[2]
                        direction = var[3]
                        key = str(index) + " " + str(layer) + " " + str(type) + " " + str(direction)
                        slashTotals[key] = len(list(filter(lambda x: x["_lineIndex"] == index and x["_lineLayer"] == layer and x["_type"] == type and x["_cutDirection"] == direction, fileData["_notes"])))
            

                    measureStart = 0 
                    allMeasures = list()
                    measure = list()
                    for note in fileData["_notes"]:
                        if note["_time"] > measureStart and note["_time"] < measureStart + secPerMes:
                            measure.append(note)
                        
                        else:
                            allMeasures.append(measure[::])
                            measure = list()
                            measureStart += secPerMes
                        
                    eventData["event_sum_by_type_value"] = eventTotals
                    slashData["slash_sum_by_each_variation"] = slashTotals
                        
                    timelineData = dict()
                    timelineData["events"] = eventData
                    timelineData["slashs"] = slashData
                    timelineData["timeline"] = allMeasures
                    difficultyDict[d] = timelineData
            mData["difficulties"] = difficultyDict
            f.write(json.dumps(mData, indent=4))
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
