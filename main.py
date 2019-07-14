import os, sys
sys.path.append(os.getcwd())

#from config import PATH, SONGS, FORMATTED_DATA_PATH
#sys.path.append(PATH)

from netBeatSaber.dataManager import DataManager
from netBeatSaber.songAnalyzer import analyzeBeat, featureExtraction
from netBeatSaber.netBeatModel import NetBeatModel















if __name__ == "__main__":
    #datamanager = DataManager(SONGS, FORMATTED_DATA_PATH)
    datamanager = DataManager()
    datamanager.generateModelData()
    
    #featureExtraction(os.getcwd() + "/data/customLevels/Nuclear Star/NUCLEAR.egg")