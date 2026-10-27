labelCount = 0
tempCount = 0

def newTemp():    
    global tempCount
    tempCount += 1
    return f't{tempCount}'

def newLabel():
    global labelCount
    labelCount += 1
    return f'L{labelCount}'

