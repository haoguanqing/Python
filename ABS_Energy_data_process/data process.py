## Guanqing Hao

def readFromFile(path):
    '''Read a file and store each non-empty line in a list'''
    fileList=[]
    try:
        with open(path) as f:
            content = f.readlines()
        for line in content:
            line = line.strip()
            if line != '':
                fileList.append(line)
        f.close()
    except RuntimeError:
        print "Bad bad!"
        
    return fileList

def createName(path):
    i=0
    j=0
    for char in path:
        if char == "\\":
            j=i
        i+=1
    resultName = "ABS_Energy_"+path[j+1:]
    return resultName
    
def isData(line):
    '''check if the line contains data we desire'''
    lst = line.split()
    if ((lst[0] == '1') and (len(lst)>=12)):
        return True
    return False
                
def absEnergy(line):
    lst = line.split()
    return float(lst[11])

def writeResults(fileName, dataList):
    f = open(fileName, 'w')
    f.write("sum: " + str(sum(dataList)))
    f.write("\n\nABS-Energy:\n")
    for data in dataList:
        f.write(str(data)+"\n")
    f.close() 

# ===== main function =====
def main():
    repeat = 'y'
    while repeat != 'n':
        path = raw_input('___________________________________________________________\nPlease drag your original txt file here: ')
        fileList = readFromFile(path)
        print "Grabing data..."
        dataList = []
        for line in fileList:
            if isData(line):
                dataList.append(absEnergy(line))
        resultFileName = createName(path)
        writeResults(resultFileName, dataList)
        print "Data are successfully saved in <"+resultFileName+">!"
        repeat = raw_input('continue? (y/n) ')
        
    fileName = 'Cu_40W_6mTorr_60min.txt'
    
    
    
    
if __name__ == '__main__':
    main()


    
