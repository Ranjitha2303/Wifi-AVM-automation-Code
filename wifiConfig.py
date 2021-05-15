import os
import argparse
import inspect
import platform

import testLogs


####-------------------
#### Values based on PC
####-------------------

if platform.system() == 'Windows':
	pathDivider = '\\'

baseDirectory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
outputDirectory = baseDirectory + pathDivider + "output" + pathDivider
baseGraphDirectory = outputDirectory + "graphs" + pathDivider
baseXlDirectory = outputDirectory + "xl" + pathDivider
iperfDirectory = None
iperfLogDirectory = None


####---------------------
#### NAMING CONFIGURATION
####---------------------


generateReport = 0
modifyReport = 0


tests = {0 : "buildTest",
         1 : "apTest",
         2 : "bandTest5g6g",
         3 : "bandTest2g5g"}

test = 0


aps = {0 : 'QCA_AP',
       1 : 'COMP_AP'}
ap = 0


builds = {0 : 'HK_PROP',
          1 : 'ATH11K'}
build = 0


bands = {2 : '2G',
         5 : '5G',
         6 : '6G'}
band = 2


graphLegend = {0 : [builds[0], builds[1]],
               1 : [aps[0], aps[1]],
               2 : [bands[6], bands[5]],
               3 : [bands[5], bands[2]],}


links = {0 : 'DL',
         1 : 'UL'}
link = 0


streams = {0 : 'SS',
           1 : 'MS'}
stream = 0


protocols = {0 : 'TCP',
             1 : 'UDP'}
protocol = 0


graphs = {0 : 'RADAR',
          1 : 'BAR'}
graph = 0


####----------------------
#### XL FILE CONFIGURATION
####----------------------

xlToParse = None
xlToCreate = None
xlTotalRows = 36
xlTotalCols = 8
xlRowStart = 1
xlColStart = 1
xlReportFromXl = 0



####----------------------
#### GRAPH CONFIGURATION
####----------------------

barWidth = 0.25
legendXpos = 0.25
legendYpos = 1.1
labelXname = None
labelYname = None
graphTitle = None

barXticks = {0 : ['MIN', 'AVG', 'MAX']}


####-------------------------
#### TURN TABLE CONFIGURATION
####-------------------------

#### Parameters of Turn Table
ttPort = 'COM6'                    # COM port of the Turn Table
ttBaudrate = 9600                  # Baudrate in which Turn Table operates
ttTotalSteps = 28800               # Total number of steps to complete rotation of 360 degree
ttTotalTurnTime = 40               # Approximate time taken to complete rotation of 360 degree
ttTimePerStep = float(ttTotalTurnTime/ttTotalSteps) # Time taken to rotate per step
ttStepsPerAngle = int(28800/360)   # Number of steps to rotating to 1 degree
ttRotateAngle = 10                 # Angle to which we rotate the turn table periodically for testing
anglePerMove = 1
currentAngle = 0



####--------------------
#### IPERF CONFIGURATION
####--------------------

#### IP of backbone connected with AP
localIP = '192.168.4.177'

#### Details of station connected with AP
remoteIP = '192.168.4.133'
remoteUsername = 'zilogic'
remotePassword = 'user'

#### iperf command and options
iperf = "iperf-1-7-0.exe"     # iperf command to execute
windowSize = '256k'           # set window size / socket buffer size
listeningPort = 9002          # server port to listen on/connect to
executionTime = 20            # time in seconds to transmit
numberOfStream = 7            # number of parallel client streams to run

#### Derived iperf commands to execute finally in both AP and Station, based on the parameters given by the user
iperfServer = "{} -s -p {}".format(iperf, listeningPort)
iperfServer = iperfServer.encode()


####-------------------------
#### AVM Carrier Backoff Test
####-------------------------
cbQacDirectory = None
cbCompDirectory = None
cbClients = ["iPhone11", "IntelAC9260", "HSP", "MacbookPro"]

def parseWifiCommandLineArgs():

    testLogs.INFO ("FUNCTION : Parsing Command line arguments")
    myParser = argparse.ArgumentParser(description='Getting Command line arguments from tester for WiFi Testing...')
    
    myParser.add_argument('--test',
                          type=int,
                          choices=list(tests.keys()),
                          help="Select the type of TEST\nAvailable TEST types are : {}".format(tests))
    
    myParser.add_argument('--ap',
                          type=int,
                          choices=list(aps.keys()),
                          help="Select the AP in which the testing is about to Run\n Available AP types are : {}".format(aps))
    
    myParser.add_argument('--build',
                          type=int,
                          choices=list(builds.keys()),
                          help="Select the BUILD in which the testing is about to Run\n Available BUILDS types are : {}".format(builds))
    
    myParser.add_argument('--band',
                          type=int,
                          choices=list(bands.keys()),
                          help="Select the BAND in which the testing is about to Run\n Available BANDS types are : {}".format(bands))
    
    myParser.add_argument('--link',
                          type=int,
                          choices=list(links.keys()),
                          help="Select the LINK in which the testing is about to Run\n Available LINKS types are : {}".format(links))
    
    myParser.add_argument('--stream',
                          type=int,
                          choices=list(streams.keys()),
                          help="Select the STREAM in which the testing is about to Run\n Available STREAMS types are : {}".format(streams))
    
    myParser.add_argument('--protocol',
                          type=int,
                          choices=list(protocols.keys()),
                          help="Select the PROTOCOL in which the testing is about to Run\n Available PROTOCOLS types are : {}".format(protocols))
    
    myParser.add_argument('--graph',
                          type=int,
                          choices=list(graphs.keys()),
                          help="Select the type of GRAPH\nAvailable GRAPHS types are : {}".format(graphs))
    
    myParser.add_argument('--barwidth',
                          type=int,
                          help="Select the Bar width of the BAR chart")
    
    myParser.add_argument('--legendx',
                          type=float,
                          help="Place the legends of a graph in X position")
    
    myParser.add_argument('--legendy',
                          type=float,
                          help="Place the legends of a graph in Y position")
    
    myParser.add_argument('--labelx',
                          type=str,
                          help="To give a name to X label")
    
    myParser.add_argument('--labely',
                          type=str,
                          help="To give a name to Y label")
    
    myParser.add_argument('--gtitle',
                          type=str,
                          help="To give a Title to a Graph")
    
    myParser.add_argument('--xlin',
                          type=str,
                          help="To give XL file name from which the datas retrived to generate graphs")
    
    myParser.add_argument('--xlout',
                          type=str,
                          help="To give XL file name in which the datas are about to saved")
    
    myParser.add_argument('--xlrows',
                          type=int,
                          help="To give total numbers of ROWS to get data from")
    
    myParser.add_argument('--xlcols',
                          type=int,
                          help="To give total numbers of COLUMS to get data from")
    
    myParser.add_argument('--xlrowstart',
                          type=int,
                          help="To identify where the ROWS starts to get data")
    
    myParser.add_argument('--xlcolstart',
                          type=int,
                          help="To identify where the COLUMS starts to get data")
    
    myParser.add_argument('--xlreportfromxl',
                          type=int,
                          choices = [0, 1],
                          help="To select whether the final report generated from a XL file or individual test file")
    
    myParser.add_argument('--ttport',
                          type=str,
                          help="To identify serial port in which the Turn Table connected. Values given must be 'COMx' -> x is number of the COM port")
    
    myParser.add_argument('--angle',
                          type=int,
                          help="To Rotate the Turn Table into given angle")
    
    myParser.add_argument('--generatereport',
                          type=int,
                          choices = [0, 1],
                          help="To decide whether Reports are needs to be generated or not")
    
    myParser.add_argument('--modifyreport',
                          type=int,
                          choices = [0, 1],
                          help="To decide whether modified reports are needs to be generated or not")
    
    myParser.add_argument('--lip',
                          type=str,
                          help="To provide Local IP address")
    
    myParser.add_argument('--rip',
                          type=str,
                          help="To provide Remote IP address")
    
    myParser.add_argument('--rusername',
                          type=str,
                          help="To provide Remote User name")
    
    myParser.add_argument('--rpassword',
                          type=str,
                          help="To provide Remote Password")
    
    myParser.add_argument('--cbqacdirectory',
                          type=str,
                          help="To provide report directory of Carrier backoff test for Qualcom AP")
    
    myParser.add_argument('--cbcompdirectory',
                          type=str,
                          help="To provide report directory of Carrier backoff test for Competitor AP")

    args = myParser.parse_args()


    global ap
    global build
    global band
    global link
    global stream
    global protocol
    global graph
    global test
    global generateReport
    global modifyReport

    global localIP
    global remoteIP
    global remoteUsername
    global remotePassword
    
    global ttPort
    global anglePerMove
    
    global barWidth
    global legendXpos
    global legendYpos
    global labelXname
    global labelYname
    global graphTitle
    
    global xlToParse
    global xlToCreate
    global xlTotalRows
    global xlTotalCols
    global xlRowStart
    global xlColStart
    global xlReportFromXl

    global cbQacDirectory
    global cbCompDirectory
    
    if args.ap != None:
        ap = args.ap
    if args.build != None:
        build = args.build
    if args.band != None:
        band = args.band
    if args.link != None:
        link = args.link
    if args.stream != None:
        stream = args.stream
    if args.protocol != None:
        protocol = args.protocol
    if args.graph != None:
        graph = args.graph
    if args.test != None:
        test = args.test
    if args.barwidth != None:
        barWidth = args.barwidth
    if args.legendx != None:
        legendXpos = args.legendx
    if args.legendy != None:
        legendYpos = args.legendy
    if args.labelx != None:
        labelXname = args.labelx
    if args.labely != None:
        labelYname = args.labely
    if args.gtitle != None:
        graphTitle = args.gtitle
    if args.xlin != None:
        xlToParse = args.xlin
    if args.xlout != None:
        xlToCreate = args.xlout
    if args.xlrows != None:
        xlTotalRows = args.xlrows
    if args.xlcols != None:
        xlTotalCols = args.xlcols
    if args.xlrowstart != None:
        xlRowStart = args.xlrowstart
    if args.xlcolstart != None:
        xlColStart = args.xlcolstart
    if args.ttport != None:
        ttPort = args.ttport
    if args.generatereport != None:
        generateReport = args.generatereport
    if args.modifyreport != None:
        modifyReport = args.modifyreport
    if args.lip != None:
        localIP = args.lip
    if args.rip != None:
        remoteIP = args.rip
    if args.rusername != None:
        remoteUsername = args.rusername
    if args.rpassword != None:
        remotePassword = args.rpassword
    if args.angle != None:
        anglePerMove = args.angle
    if args.cbqacdirectory != None:
        cbQacDirectory = args.cbqacdirectory
    if args.cbcompdirectory != None:
        cbCompDirectory = args.cbcompdirectory
    if args.xlreportfromxl != None:
        xlReportFromXl = args.xlreportfromxl


if __name__ == '__main__':
    parseWifiCommandLineArgs()
    testLogs.INFO("Base Directory : {}".format(baseDirectory))
    testLogs.INFO("Graph Directory : {}".format(graphDirectory))
    testLogs.INFO("XL Directory : {}".format(xlDirectory))
    testLogs.INFO("Iperf Directory : {}".format(iperfDirectory))
