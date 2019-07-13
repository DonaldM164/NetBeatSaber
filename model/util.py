




def secondsPerMeasure(bpm, timeSignature=4):
    bps = bpm / 60 #Beats Per Second
    
    #Beats In One Time Measure(Typically 4) = bps * x (x = seconds)
    return timeSignature / bps 
    
