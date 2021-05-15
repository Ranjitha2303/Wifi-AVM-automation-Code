#### Internal Libraries
import subprocess
import os


#### User defined Libraries
import testLogs
import wifiConfig
import remoteAccess


def killLocalIperf():
    """
    To terminate all the iperf tasks running in backbone PC

    Arguments : None
    
    Returns : True, On successful termination of iperf tasks
              False, On failure of terminating iperf tasks
    """

    testLogs.INFO ("FUNCTION : Terminating Local Iperf tasks")
    # Windows command to get all the running task
    ps = os.popen('wmic process get description').read()
    
    if wifiConfig.iperf in ps:
        # Windows command to kill all the running iperf task
        s = os.system("taskkill /f /im {}".format(wifiConfig.iperf))
        
        if s != 0:
            testLogs.ERROR("Could Not kill {}".format(wifiConfig.iperf))
            return False
        testLogs.SUCCESS("Terminated the process : {}".format(wifiConfig.iperf))
    else:
        testLogs.STATUS ("Process {} Not found".format(wifiConfig.iperf))
    return True


def killRemoteIperf(host=wifiConfig.remoteIP, user=wifiConfig.remoteUsername, password=wifiConfig.remotePassword):
    """
    To terminate all the iperf tasks running in remote station

    Arguments : None
    
    Returns : True, On successful termination of iperf tasks
              False, On failure of terminating iperf tasks
    """

    testLogs.INFO ("FUNCTION : Terminating Remote Iperf tasks")
    station = remoteAccess.remoteAccess(host=host,
                                        user=user,
                                        password=password)
    command = "taskkill /f /im {}".format(wifiConfig.iperf)
    testLogs.INFO (command)
    status = station.executeCommand(command)
    if status != False:
        return str(status)
    return status


def runLocalIperfServer():
    """
    Running iperf server in backbone PC which is connected with AP

    Arguments : None
    
    Returns : True, On successful start of iperf server
              False, On failure in starting iperf server
    """
    
    testLogs.INFO("FUNCTION : Running Local Iperf Server")
    command = wifiConfig.iperfServer
    testLogs.INFO(command)
    try:
        p = subprocess.Popen(command.split(),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        return True
    except Exception as E:
        testLogs.ERROR ("Could not start the {} server...".format(wifiConfig.iperf))
        testLogs.ERROR (E)
        return False


def runRemoteIperfServer(host=wifiConfig.remoteIP, user=wifiConfig.remoteUsername, password=wifiConfig.remotePassword):
    """
    Running iperf server in Station which is connected with AP

    Arguments : host, IP address of Station
                user, User name of station
                password, Password of station
                
    Returns : True, On successful start of iperf server
              False, On failure in starting iperf server
    """
    
    testLogs.INFO("FUNCTION : Running Remote Iperf Server")
    station = remoteAccess.remoteAccess(host=host,
                                        user=user,
                                        password=password)
    command = wifiConfig.iperfServer
    testLogs.INFO(command)
    status = station.executeCommandInBackground(command)
    if status != False:
        return True
    return status


def runIperfServer():
    """
    Running iperf server in Backbone PC or Station based on parameters given by the user

    Arguments: None

    Returns: True, On Success
             Failuer, On Failure
    """

    testLogs.INFO ("FUNCTION : Running iperf server")
    
    if wifiConfig.link == 0:
        return runRemoteIperfServer(wifiConfig.remoteIP, wifiConfig.remoteUsername, wifiConfig.remotePassword)
    elif wifiConfig.link == 1:
        return runLocalIperfServer()

    
def runLocalIperfClient():
    """
    Running iperf client in backbone PC which is connected with AP

    Arguments : None
    
    Returns : True, On successful start of iperf client
              False, On failure in starting iperf client
    """
    
    testLogs.INFO("FUNCTION : Running Local Iperf Client")

    command = "{} -c {} -i 1 -f m -w {} -p {} -t {} ".format(wifiConfig.iperf,
                                                             wifiConfig.remoteIP,
                                                             wifiConfig.windowSize,
                                                             wifiConfig.listeningPort,
                                                             wifiConfig.executionTime)
	
    if wifiConfig.stream == 1:
        command += "-P {}".format(wifiConfig.numberOfStream)
    
    testLogs.INFO(command)
    try:
        p = subprocess.Popen(command.split(),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = str(out)
        err = str(err)
        
        if err == "b''":
            return out
        
        testLogs.ERROR (err)
        return False
    except Exception as E:
        testLogs.ERROR ("Could not start the {} client...".format(wifiConfig.iperf))
        testLogs.ERROR (E)
        return False


def runRemoteIperfClient(host=wifiConfig.remoteIP, user=wifiConfig.remoteUsername, password=wifiConfig.remotePassword):
    """
    Running iperf client in Station which is connected with AP

    Arguments : host, IP address of Station
                user, User name of station
                password, Password of station
                
    Returns : True, On successful start of iperf client
              False, On failure in starting iperf client
    """

    testLogs.INFO ("FUNCTION : Running Remote Iperf Client")
    station = remoteAccess.remoteAccess(host=host,
                                        user=user,
                                        password=password)

    command = "{} -c {} -i 1 -f m -w {} -p {} -t {} ".format(wifiConfig.iperf,
                                                             wifiConfig.localIP,
                                                             wifiConfig.windowSize,
                                                             wifiConfig.listeningPort,
                                                             wifiConfig.executionTime)
	
    if wifiConfig.stream == 1:
        command += "-P {}".format(wifiConfig.numberOfStream)
		
    testLogs.INFO (command)
    
    status = station.executeCommand(command)
    if status != False:
        return str(status)
    return status


def runIperfClient():
    """
    Running iperf client in Backbone PC or Station based on parameters given by the user

    Arguments: None

    Returns: True, On Success
             Failuer, On Failure
    """

    testLogs.INFO ("FUNCTION : Running iperf client")
    testLogs.INFO (wifiConfig.link)
    
    if wifiConfig.link == 0:
        return runLocalIperfClient()
    elif wifiConfig.link == 1:
        return runRemoteIperfClient(wifiConfig.remoteIP, wifiConfig.remoteUsername, wifiConfig.remotePassword)


if __name__ == '__main__':
    wifiConfig.parseWifiCommandLineArgs()
    runIperfClient()
