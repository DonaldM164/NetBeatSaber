PATH = #Path to NetBeatSaber
SONGS = PATH + r"\data\customLevels"
FORMATTED_DATA_PATH = PATH + r"\data\formattedData"


#Training Hyper Parameters 
n_steps = 10000 #Number of training steps
learning_rate = .001
n_hidden = 50 #Number of hidden layers 

with_dropout = False
keep_probability = 0.9 #Only matters if with_dropout=True