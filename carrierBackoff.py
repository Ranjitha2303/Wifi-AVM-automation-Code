import subprocess
import os
import sys
import argparse
import time

import wifiConfig
import testLogs
import xlParser


clientPosition = {1 : 14, 2 : 19, 3 : 24, 4 : 29}
clientColumn = 16
aggregateColumn = 9
directory = None
data = None


def getValues(row, col):
    try:        
        return data[row].split(',')[col]
    except Exception as E:
        testLogs.ERROR("Could not get value from ROW : {}, COL : {}".format(row, col))
        testLogs.ERROR(E)
        exit(1)

def getValueFromClient(client = 1):
    values = []
    for row in range(clientPosition[client], clientPosition[client] + 5):
        value = getValues(row, clientColumn)
        if value != '':
            values.append(float(value))
    return values


def getAggregateValue():
    try:
        return data[-1].split(',')[aggregateColumn]
    except Exception as E:
        testLogs.ERROR("Could not get AGGREGATE value")
        testLogs.ERROR(E)
        exit(1)

def readDataFromFile(file = None):
    if file == None:
        testLogs.ERROR ("Kindly provide a file to read")
        exit(1)
        
    global data
    try:
        fd = open(file, 'r')
        data = fd.readlines()
        fd.close()
    except Exception as E:
        testLogs.ERROR("Could not open and read from file : {}".format(file))
        testLogs.ERROR(E)
        exit(1)


def main():
    fileName = "test_Position_{}.csv"
    global directory
    directory += wifiConfig.pathDivider
    xlFileName = directory + "averageValues.xlsx"
    xlParser.writeXlFileRows(xlFileName, ["Position"] + wifiConfig.cbClients + ["Aggregate"], 2, 1)
    for i in range(1, 37):
        row = i + 2
        xlParser.writeXlFileRows(xlFileName, [i, ], row, 1)
        fileToOpen = directory + fileName.format(i)
        testLogs.INFO ("File Name is : {}".format(fileToOpen))
        readDataFromFile(fileToOpen)
        avgValue = ''
        for index, client in enumerate(clientPosition.keys()):
            clientValues = getValueFromClient(client)
            testLogs.INFO ("client {} values are : {}".format(client, clientValues))            
            if clientValues != []:
                avgValue = sum(clientValues) / len(clientValues)
            else:
                avgValue = 0
            testLogs.INFO ("Average value is : {}".format(avgValue))
            xlParser.writeXlFileRows(xlFileName, [avgValue, ], row, index + 2)
            
        aggregateValue = getAggregateValue()
        if aggregateValue != '':
            aggregateValue = float(aggregateValue)
        else:
            aggregateValue = 0
        testLogs.INFO ("Aggregate value is : {}".format(aggregateValue))
        xlParser.writeXlFileRows(xlFileName, [aggregateValue, ], row, 6)

    # Write average values
    for col in range(2, 7):
        values = xlParser.readXlFileColums(xlFileName, 3, col, 36)
        print (values)
        average = round(sum(values) / len(values), 3)
        xlParser.writeXlFileRows(xlFileName, [average, ], 39, col)

    xlParser.writeXlFileRows(xlFileName, ["AVERAGE", ], 39, 1)


def generateReport():
    testLogs.INFO ("QAC Report Directory is : {}".format(wifiConfig.cbQacDirectory))
    testLogs.INFO ("Competitor Report Directory is : {}".format(wifiConfig.cbCompDirectory))
    log = "{}_{}_{}_{}".format(wifiConfig.streams[wifiConfig.stream],
                               wifiConfig.bands[wifiConfig.band],
                               wifiConfig.protocols[wifiConfig.protocol],
                               wifiConfig.links[wifiConfig.link])
    outputXlFile = wifiConfig.baseXlDirectory + log + '.xlsx'
    qacXlFile = wifiConfig.cbQacDirectory + wifiConfig.pathDivider + "averageValues.xlsx"
    compXlFile = wifiConfig.cbCompDirectory + wifiConfig.pathDivider + "averageValues.xlsx"
    testLogs.INFO ("QAC XL file is : {}".format(qacXlFile))
    testLogs.INFO ("Competitor XL file is : {}".format(compXlFile))
    testLogs.INFO ("Output XL file is : {}".format(outputXlFile))

    # Get QAC's Values
    qacClientsValues = xlParser.readXlFileRows(qacXlFile, 39, 2, 4)
    qacAggValues = xlParser.readXlFileColums(qacXlFile, 3, 6, 36)
    qacAggAverage = xlParser.readXlFileColums(qacXlFile, 39, 6, 1)

    # Get Competitor's values
    compClientsValues = xlParser.readXlFileRows(compXlFile, 39, 2, 4)
    compAggValues = xlParser.readXlFileColums(compXlFile, 3, 6, 36)
    compAggAverage = xlParser.readXlFileColums(compXlFile, 39, 6, 1)

    
    testLogs.INFO ("QAC's Client Values are : {}".format(qacClientsValues))
    testLogs.INFO ("QAC's Aggregate Values are : {}".format(qacAggValues))
    testLogs.INFO ("QAC's Average of Aggregate Values are : {}".format(qacAggAverage))
    testLogs.INFO ("Competitors's Client Values are : {}".format(compClientsValues))
    testLogs.INFO ("Competitors's Aggregate Values are : {}".format(compAggValues))
    testLogs.INFO ("Competitors's Average of Aggregate Values are : {}".format(compAggAverage))

    #Writing Clients Values
    xlParser.writeXlFileRows(outputXlFile, ["AP"] + wifiConfig.cbClients, 2, 1)
    xlParser.writeXlFileRows(outputXlFile, [wifiConfig.aps[0]] + qacClientsValues, 3, 1)
    xlParser.writeXlFileRows(outputXlFile, [wifiConfig.aps[1]] + compClientsValues, 4, 1)

    #Writing Average Aggregate values
    xlParser.writeXlFileColums(outputXlFile, ["AP", "AGGREGATE"], 7, 1)
    xlParser.writeXlFileColums(outputXlFile, [wifiConfig.aps[0]] + qacAggAverage, 7, 2)
    xlParser.writeXlFileColums(outputXlFile, [wifiConfig.aps[1]] + compAggAverage, 7, 3)

    #Writing Aggregate values
    xlParser.writeXlFileColums(outputXlFile, ["POSITION"] + list(range(1, 37)), 11, 1)
    xlParser.writeXlFileColums(outputXlFile, [wifiConfig.aps[0]] + qacAggValues, 11, 2)
    xlParser.writeXlFileColums(outputXlFile, [wifiConfig.aps[1]] + compAggValues, 11, 3)

    #Generate Graphs
    
        
        
def parseCommandLineArgs():

    testLogs.INFO ("FUNCTION : Parsing Command line arguments")
    myParser = argparse.ArgumentParser(description='Getting Command line arguments from tester for WiFi Testing...')
    
    myParser.add_argument('directory',
                          type=str,
                          help="Provide the dirctory which contains the ixChariot report files")
    
    args = myParser.parse_args()

    global directory

    directory = args.directory
    testLogs.INFO ("Directory is : {}".format(directory))


if __name__ == '__main__':
    wifiConfig.parseWifiCommandLineArgs()
    if wifiConfig.generateReport == 0:
        if wifiConfig.cbQacDirectory != None:
            directory = wifiConfig.cbQacDirectory
            main()
        if wifiConfig.cbCompDirectory != None:
            directory = wifiConfig.cbCompDirectory
            main()

    elif wifiConfig.generateReport == 1:
        generateReport()
