import os, sys
sys.path.append(os.getcwd())

#from config import PATH, SONGS, FORMATTED_DATA_PATH
#sys.path.append(PATH)

from model.dataManager import DataManager

















if __name__ == "__main__":
    #datamanager = DataManager(SONGS, FORMATTED_DATA_PATH)
    datamanager = DataManager()
    datamanager.generateModelData()