import os
import sys
import argparse


import graphs
import testLogs


logDirectory = None
pngFileName = None
linkType = 'D'


def getLogFilesInDirectory(directory=None):

    testLogs.INFO ("FUNCTION : Getting Log files in directory : {}".format(directory))
    
    if directory == None:
        testLogs.ERROR("Kindly provide the directory to get log files")
        exit(1)
    try:
        files = os.listdir(directory)
    except Exception as E:
        testLogs.ERROR("Could not get files from the directory : {}".format(directory))
        testLogs.ERROR(E)
        exit(1)
    filesDict = {}
    for file in files:
        if '_' not in file:
            continue
        angle = file.split('.')[0].split("_")[-1]
        try:
            angle = int(angle)
            filesDict[angle] = file
        except Exception as E:
            testLogs.ERROR ("This file is not is expected format : {}".format(file))
    #for ele in filesDict:
    #    print ("{} : {}".format(ele, filesDict[ele]))
    return filesDict


def getTpInLogFiles(filesDict=None, logFolder=None):

    testLogs.INFO ("FUNCTION : Reading Throughput from many files")
    
    if filesDict == None:
        testLogs.ERROR("Kindly provide data to parse...")
        exit(1)

    if logFolder != None:
        logDirectory = logFolder

    testLogs.INFO("----LOG FOLDER : {}".format(logDirectory))
    testLogs.INFO("----FILES : {}".format(filesDict))
        
    tpts = []
    # testLogs.INFO("File : {}".format(filesDict))
    for ang in range(10, 361, 10):
        file = logDirectory +  filesDict[ang]
        fd = open(file, 'r')
        lines = fd.readlines()
        # prints.INFO("LINES : {}".format(lines))
        tp = int(float(lines[-1].split(' ')[-2]))
        fd.close()    
        tpts.append(tp)

    return tpts


def getTpInLogFile(file=None):

    testLogs.INFO ("FUNCTION : Reading Throughput in from single file : {}".format(file))
    
    if file == None:
        testLogs.ERROR ("Kindly provide file to parse...")
        exit(1)

    tpts = []
    try:
        fd = open(file, 'r')
        lines = fd.readlines()
        for line in lines:
            if "Mbits/sec" in line:
                # print (line)
                tp = int(float(line.split(' ')[-2]))
                fd.close()
                tpts.append(tp)
    except Exception as E:
        testLogs.ERROR ("Could not open given log file to parse")
        exit(1)
            
    return tpts


if __name__ == '__main__':
    parseWifiCommandLineArgs()
    if linkType == 'D':
        files = getLogFilesInDirectory(logDirectory)
        tps = getTpInLogFiles(files)
    elif linkType == 'U':
        tps = getTpInLogFile(logDirectory)
    else:
        print ("Please provide D or U option to draw graph for Downlink or Uplink")
        exit(1)
    print (tps)
    radarGraph.createSingleRadarGraph(tps, pngFileName)
