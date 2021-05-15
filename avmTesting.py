#### Internal Libraries
import subprocess
import os
import sys
import argparse
import time


#### User defined Libraries
import wifiConfig
import turnTable
import iperf
import graphs
import logParser
import xlParser
import testLogs


def createDirectory(directory = None):
    if directory == None:
        testLogs.ERROR ("Please provide a directory name to create")
        exit(1)

    testLogs.INFO ("Directory is about to create in : {}".format(directory))
    try:
        if os.path.exists(directory) == False:
            os.mkdir(directory)
            testLogs.SUCCESS ("Directory created")
    except Exception as E:
        testLogs.ERROR (E)
        exit(1)


def createXlFile(xlFile = None, data = [1, 2, 3, 4, 5]):

    testLogs.INFO ("FUNCTION : Creating XL file : {}".format(xlFile))
    if wifiConfig.test == 0:
        label = wifiConfig.graphLegend[wifiConfig.test][wifiConfig.build]
    if wifiConfig.test == 1:
        label = wifiConfig.graphLegend[wifiConfig.test][wifiConfig.ap]
    if wifiConfig.test == 2 or wifiConfig.test == 3:
        label = wifiConfig.graphLegend[wifiConfig.test][wifiConfig.band]
        
    data1 = ['ANGLE'] + list(range(10, (len(data) * 10 + 1), 10)) + ['MIN', 'AVG', 'MAX']
    data2 = [label] + data + [min(data), int(sum(data) / len(data)), max(data)]
    
    xlParser.writeXlFileColums(xlFile, data1, 3, 1)
    xlParser.writeXlFileColums(xlFile, data2, 3, 2)


def createFinalReport():

    testLogs.INFO ("FUNCTION : Generating Final test reports")

    if wifiConfig.test == 0 or wifiConfig.test == 1:        
        log = "{}_{}_{}_{}".format(wifiConfig.streams[wifiConfig.stream],
                                   wifiConfig.bands[wifiConfig.band],
                                   wifiConfig.protocols[wifiConfig.protocol],
                                   wifiConfig.links[wifiConfig.link])
    elif wifiConfig.test == 2 or wifiConfig.test == 3:        
        log = "{}_{}_{}".format(wifiConfig.streams[wifiConfig.stream],
                                   wifiConfig.protocols[wifiConfig.protocol],
                                   wifiConfig.links[wifiConfig.link])
    
    if wifiConfig.test == 0:
       iperfDirectory1 = wifiConfig.outputDirectory + wifiConfig.builds[0] + wifiConfig.pathDivider + log + wifiConfig.pathDivider
       iperfDirectory2 = wifiConfig.outputDirectory + wifiConfig.builds[1] + wifiConfig.pathDivider + log + wifiConfig.pathDivider
    elif wifiConfig.test == 1:
       iperfDirectory1 = wifiConfig.outputDirectory + wifiConfig.aps[0] + wifiConfig.pathDivider + log + wifiConfig.pathDivider
       iperfDirectory2 = wifiConfig.outputDirectory + wifiConfig.aps[1] + wifiConfig.pathDivider + log + wifiConfig.pathDivider
    elif wifiConfig.test == 2:
       iperfDirectory1 = wifiConfig.outputDirectory + wifiConfig.bands[5] + wifiConfig.pathDivider + log + wifiConfig.pathDivider
       iperfDirectory2 = wifiConfig.outputDirectory + wifiConfig.bands[6] + wifiConfig.pathDivider + log + wifiConfig.pathDivider
    elif wifiConfig.test == 3:
       iperfDirectory1 = wifiConfig.outputDirectory + wifiConfig.bands[2] + wifiConfig.pathDivider + log + wifiConfig.pathDivider
       iperfDirectory2 = wifiConfig.outputDirectory + wifiConfig.bands[5] + wifiConfig.pathDivider + log + wifiConfig.pathDivider
    
    testLogs.INFO ("iperfDirectory1 is : {}".format(iperfDirectory1))
    files = logParser.getLogFilesInDirectory(iperfDirectory1)
    throughputs1 = logParser.getTpInLogFiles(files, iperfDirectory1)
    testLogs.INFO("Throuputs1 is : {}".format(throughputs1))
    
    testLogs.INFO ("iperfDirectory2 is : {}".format(iperfDirectory2))
    files = logParser.getLogFilesInDirectory(iperfDirectory2)
    throughputs2 = logParser.getTpInLogFiles(files, iperfDirectory2)
    testLogs.INFO("Throuputs2 is : {}".format(throughputs2))

    #### Graph Generation
    graphName = wifiConfig.baseGraphDirectory + log
    graphs.createMultipleBarGraph([throughputs1, throughputs2],
                                  graphName)
    graphs.createMultipleRadarGraph([throughputs1, throughputs2],
                                    graphName)
    throughputs1 = throughputs1[:-1]
    throughputs2 = throughputs2[:-1]

    #### XL File Generation
    data1 = ['ANGLE'] + list(range(10, (len(throughputs1) * 10 + 1), 10)) + ['MIN', 'AVG', 'MAX']
    if wifiConfig.test == 0:
        heading = [wifiConfig.builds[0], wifiConfig.builds[1]]
    elif wifiConfig.test == 1:
        heading = [wifiConfig.aps[0], wifiConfig.aps[1]]
    elif wifiConfig.test == 2:
        heading = [wifiConfig.bands[5], wifiConfig.bands[6]]
    elif wifiConfig.test == 3:
        heading = [wifiConfig.bands[2], wifiConfig.bands[5]]
        
    data2 = [heading[0]] + throughputs1 + [min(throughputs1), int(sum(throughputs1) / len(throughputs1)), max(throughputs1)]
    data3 = [heading[1]] + throughputs2 + [min(throughputs2), int(sum(throughputs2) / len(throughputs2)), max(throughputs2)]

    xlFileName = wifiConfig.baseXlDirectory + log + '.xlsx'
    xlParser.writeXlFileColums(xlFileName, data1, 3, 1)
    xlParser.writeXlFileColums(xlFileName, data2, 3, 2)
    xlParser.writeXlFileColums(xlFileName, data3, 3, 3)
    xlParser.insertXlImage(xlFileName, graphName + '_RADAR.png', 3, 5)
    xlParser.insertXlImage(xlFileName, graphName + '_BAR.png', 3, 18)


def createFinalReportFromXlFile(xlFile = None):

    testLogs.INFO ("FUNCTION : Generating Final test report from XL file : {}".format(xlFile))

    if wifiConfig.test == 0 or wifiConfig.test == 1:        
        log = "{}_{}_{}_{}".format(wifiConfig.streams[wifiConfig.stream],
                                   wifiConfig.bands[wifiConfig.band],
                                   wifiConfig.protocols[wifiConfig.protocol],
                                   wifiConfig.links[wifiConfig.link])
    elif wifiConfig.test == 2 or wifiConfig.test == 3:        
        log = "{}_{}_{}".format(wifiConfig.streams[wifiConfig.stream],
                                wifiConfig.protocols[wifiConfig.protocol],
                                wifiConfig.links[wifiConfig.link])
    print ("Link 0 Stream 0")
    print (log)
    if wifiConfig.test == 0 or wifiConfig.test == 1:
        if wifiConfig.band == 5:
            if wifiConfig.link == 0 and wifiConfig.stream == 0:
                throughputs1 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart, numberOfRows = wifiConfig.xlTotalRows)
                throughputs2 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 1, numberOfRows = wifiConfig.xlTotalRows)
            if wifiConfig.link == 0 and wifiConfig.stream == 1:
                throughputs1 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 2, numberOfRows = wifiConfig.xlTotalRows)
                throughputs2 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 3, numberOfRows = wifiConfig.xlTotalRows)
            if wifiConfig.link == 1 and wifiConfig.stream == 0:
                throughputs1 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 8, numberOfRows = wifiConfig.xlTotalRows)
                throughputs2 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 9, numberOfRows = wifiConfig.xlTotalRows)
            if wifiConfig.link == 1 and wifiConfig.stream == 1:
                throughputs1 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 10, numberOfRows = wifiConfig.xlTotalRows)
                throughputs2 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 11, numberOfRows = wifiConfig.xlTotalRows)
        if wifiConfig.band == 2:
            if wifiConfig.link == 0 and wifiConfig.stream == 0:
                throughputs1 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 4, numberOfRows = wifiConfig.xlTotalRows)
                throughputs2 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 5, numberOfRows = wifiConfig.xlTotalRows)
            if wifiConfig.link == 0 and wifiConfig.stream == 1:
                throughputs1 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 6, numberOfRows = wifiConfig.xlTotalRows)
                throughputs2 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 7, numberOfRows = wifiConfig.xlTotalRows)
            if wifiConfig.link == 1 and wifiConfig.stream == 0:
                throughputs1 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 12, numberOfRows = wifiConfig.xlTotalRows)
                throughputs2 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 13, numberOfRows = wifiConfig.xlTotalRows)
            if wifiConfig.link == 1 and wifiConfig.stream == 1:
                throughputs1 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 14, numberOfRows = wifiConfig.xlTotalRows)
                throughputs2 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 15, numberOfRows = wifiConfig.xlTotalRows)
    if wifiConfig.test == 2 or wifiConfig.test == 3:
        if wifiConfig.link == 0 and wifiConfig.stream == 0:
            throughputs1 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart, numberOfRows = wifiConfig.xlTotalRows)
            throughputs2 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 1, numberOfRows = wifiConfig.xlTotalRows)
        if wifiConfig.link == 0 and wifiConfig.stream == 1:
            throughputs1 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 2, numberOfRows = wifiConfig.xlTotalRows)
            throughputs2 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 3, numberOfRows = wifiConfig.xlTotalRows)
        if wifiConfig.link == 1 and wifiConfig.stream == 0:
            throughputs1 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 4, numberOfRows = wifiConfig.xlTotalRows)
            throughputs2 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 5, numberOfRows = wifiConfig.xlTotalRows)
        if wifiConfig.link == 1 and wifiConfig.stream == 1:
            throughputs1 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 6, numberOfRows = wifiConfig.xlTotalRows)
            throughputs2 = xlParser.readXlFileColums(xlFile, rowStart = wifiConfig.xlRowStart, colStart = wifiConfig.xlColStart + 7, numberOfRows = wifiConfig.xlTotalRows)
        

    #### Graph Generation
    graphName = wifiConfig.baseGraphDirectory + log
    graphs.createMultipleBarGraph([throughputs1, throughputs2],
                                  graphName)
    graphs.createMultipleRadarGraph([throughputs1, throughputs2],
                                    graphName)
    throughputs1 = throughputs1[:-1]
    throughputs2 = throughputs2[:-1]

    #### XL File Generation
    data1 = ['ANGLE'] + list(range(10, (len(throughputs1) * 10 + 1), 10)) + ['MIN', 'AVG', 'MAX']
    if wifiConfig.test == 0:
        heading = [wifiConfig.builds[0], wifiConfig.builds[1]]
    elif wifiConfig.test == 1:
        heading = [wifiConfig.aps[0], wifiConfig.aps[1]]
    elif wifiConfig.test == 2:
        heading = [wifiConfig.bands[6], wifiConfig.bands[5]]
    elif wifiConfig.test == 3:
        heading = [wifiConfig.bands[5], wifiConfig.bands[2]]
        
    data2 = [heading[0]] + throughputs1 + [min(throughputs1), int(sum(throughputs1) / len(throughputs1)), max(throughputs1)]
    data3 = [heading[1]] + throughputs2 + [min(throughputs2), int(sum(throughputs2) / len(throughputs2)), max(throughputs2)]

    xlFileName = wifiConfig.baseXlDirectory + log + '.xlsx'
    xlParser.writeXlFileColums(xlFileName, data1, 3, 1)
    xlParser.writeXlFileColums(xlFileName, data2, 3, 2)
    xlParser.writeXlFileColums(xlFileName, data3, 3, 3)
    xlParser.insertXlImage(xlFileName, graphName + '_RADAR.png', 3, 5)
    xlParser.insertXlImage(xlFileName, graphName + '_BAR.png', 3, 18)
    


def generateIndividualTestReport():

    testLogs.INFO ("FUNCTION : Generating individual test reports")

    if wifiConfig.test == 0 or wifiConfig.test == 1:        
        log = "{}_{}_{}_{}".format(wifiConfig.streams[wifiConfig.stream],
                                   wifiConfig.bands[wifiConfig.band],
                                   wifiConfig.protocols[wifiConfig.protocol],
                                   wifiConfig.links[wifiConfig.link])
    elif wifiConfig.test == 2 or wifiConfig.test == 3:        
        log = "{}_{}_{}".format(wifiConfig.streams[wifiConfig.stream],
                                   wifiConfig.protocols[wifiConfig.protocol],
                                   wifiConfig.links[wifiConfig.link])

    #### Generating report files from throughput files
    files = logParser.getLogFilesInDirectory(wifiConfig.iperfLogDirectory)
    throughputs = logParser.getTpInLogFiles(files, wifiConfig.iperfLogDirectory)
    logFile = wifiConfig.iperfLogDirectory + "throughputs.txt"
    testLogs.INFO ("Log file is : {}".format(logFile))
    try:
        fd = open(logFile, 'w+')
        fd.write(' '.join([str(tp) for tp in throughputs]))
        fd.close()
    except Exception as E:
        testLogs.ERROR ("Could not write throughputs in throughputs.txt file")
        testLogs.ERROR (E)
        exit(1)
        
    testLogs.INFO("Throughputs : {}".format(throughputs))
    
    graphName = wifiConfig.iperfLogDirectory + log
    graphs.createSingleRadarGraph(throughputs, graphName)
    throughputs = throughputs[:-1]
    graphs.createSingleBarGraph(throughputs, graphName)
    
    xlFileName = graphName + '.xlsx'
    createXlFile(xlFileName, throughputs)
    xlParser.insertXlImage(xlFileName, graphName + '_RADAR.png', 3, 5)
    xlParser.insertXlImage(xlFileName, graphName + '_BAR.png', 3, 15)
    return 0


def runTest():

    testLogs.INFO ("FUNCTION : Run the AVM test")

    if wifiConfig.test == 0 or wifiConfig.test == 1:        
        log = "{}_{}_{}_{}".format(wifiConfig.streams[wifiConfig.stream],
                                   wifiConfig.bands[wifiConfig.band],
                                   wifiConfig.protocols[wifiConfig.protocol],
                                   wifiConfig.links[wifiConfig.link])
    elif wifiConfig.test == 2 or wifiConfig.test == 3:        
        log = "{}_{}_{}".format(wifiConfig.streams[wifiConfig.stream],
                                   wifiConfig.protocols[wifiConfig.protocol],
                                   wifiConfig.links[wifiConfig.link])

    if True:
        #### Terminate the iperf process which is running already in local PC
        status = iperf.killLocalIperf()
        testLogs.STATUS ("Kill iperf in local PC status is : {}".format(status))


        #### Terminate the iperf process which is running already in remote Station
        status = iperf.killRemoteIperf(wifiConfig.remoteIP, wifiConfig.remoteUsername, wifiConfig.remotePassword)
        testLogs.STATUS ("Kill iperf in remote Station status is : {}".format(status))
        

        #### Start the iperf server
        if iperf.runIperfServer() == False:
            testLogs.ERROR("Could not start iperf server")
            exit(1)

        #### Calculating number of times to rotate the Turn table based on the degree per rotation
        steps = int(360/wifiConfig.ttRotateAngle)


        #### Executing a loop for the given number of steps
        for step in range(1, steps + 1):
            testLogs.INFO ("=============== RUNNING TEST IS : {}".format(log))
            #### Deriving log file name from the parameters        
            testLogs.INFO ("Rotate to angle : {}".format(step * wifiConfig.ttRotateAngle))
            iperfLogFile = wifiConfig.iperfLogDirectory + log + '_' + str(step * wifiConfig.ttRotateAngle) + ".txt"
            testLogs.INFO("Iperf Log File : {}".format(iperfLogFile))
                
            #### Rotate turn table to decided angle and wait for turn table to setteld in the position
            if turnTable.rotateTurnTable(wifiConfig.ttRotateAngle) == False:
                exit(1)
            time.sleep((wifiConfig.ttTimePerStep * wifiConfig.ttStepsPerAngle * wifiConfig.ttRotateAngle) + .1)

            #### Run iperf client in local or remote station based on the command line argument
            status = iperf.runIperfClient()
            testLogs.STATUS(status)

            #### Write iperf client output into log file
            if status != False:
                try:
                    fd = open(iperfLogFile, 'w+')
                    fd.close()
                    fd = open(iperfLogFile, 'a')
                    fd.write(status)
                    fd.close()
                except Exception as E:
                    testLogs.ERROR (E)
                    exit(1)
            else:
                testLogs.ERROR ("Could Not get output from iperf client")
                exit(1)


def createDirectories():
    testLogs.INFO ("FUNCTION : Genetaing Iperf directories")
    if wifiConfig.test == 0:
        wifiConfig.iperfDirectory = wifiConfig.outputDirectory + wifiConfig.builds[wifiConfig.build] + wifiConfig.pathDivider
        testLogs.INFO ("Creating Iperf Directory : {}".format(wifiConfig.iperfDirectory))
        createDirectory(wifiConfig.iperfDirectory)
    elif wifiConfig.test == 1:
        wifiConfig.iperfDirectory = wifiConfig.outputDirectory + wifiConfig.aps[wifiConfig.ap] + wifiConfig.pathDivider
        testLogs.INFO ("Creating Iperf Directory : {}".format(wifiConfig.iperfDirectory))
        createDirectory(wifiConfig.iperfDirectory)
    elif wifiConfig.test == 2 or wifiConfig.test == 3:
        wifiConfig.iperfDirectory = wifiConfig.outputDirectory + wifiConfig.bands[wifiConfig.band] + wifiConfig.pathDivider
        testLogs.INFO ("Creating Iperf Directory : {}".format(wifiConfig.iperfDirectory))
        createDirectory(wifiConfig.iperfDirectory)

    if wifiConfig.test == 0 or wifiConfig.test == 1:        
        log = "{}_{}_{}_{}".format(wifiConfig.streams[wifiConfig.stream],
                                   wifiConfig.bands[wifiConfig.band],
                                   wifiConfig.protocols[wifiConfig.protocol],
                                   wifiConfig.links[wifiConfig.link])
    elif wifiConfig.test == 2 or wifiConfig.test == 3:        
        log = "{}_{}_{}".format(wifiConfig.streams[wifiConfig.stream],
                                   wifiConfig.protocols[wifiConfig.protocol],
                                   wifiConfig.links[wifiConfig.link])
    
    wifiConfig.iperfLogDirectory = wifiConfig.iperfDirectory + log + wifiConfig.pathDivider
    testLogs.INFO ("Creating Iperf Log Directory : {}".format(wifiConfig.iperfLogDirectory))
    createDirectory(wifiConfig.iperfLogDirectory)
        
    
if __name__ == "__main__":    
    wifiConfig.parseWifiCommandLineArgs()

    createDirectories()    

    if wifiConfig.modifyReport == 1:
        generateIndividualTestReport()
        exit(0)
        
    if wifiConfig.generateReport == 1 and wifiConfig.xlReportFromXl == 0:
        testLogs.INFO ("Generating reports from Text Files....")
        createFinalReport()
        exit(0)
    elif wifiConfig.generateReport == 1 and wifiConfig.xlReportFromXl == 1:
        testLogs.INFO ("Generating reports from XL File : {}".format(wifiConfig.xlToParse))
        createFinalReportFromXlFile(wifiConfig.xlToParse)
        exit(0)
    else:
        runTest()
        generateIndividualTestReport()
