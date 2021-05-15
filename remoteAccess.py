import paramiko
import socket
import scp
import time
import getopt
import sys
#from ath10kDebug import *
#import ath10kConfig


LOG_FILE = "iperf_test_report.txt"


def ERROR(E):
    print ("ERROR : {}".format(E))

def FAIL(E):
    print ("FAIL : {}".format(E))

def INFO(E):
    print ("INFO : {}".format(E))

def SUCCESS(E):
    print ("SUCCESS : {}".format(E))


class remoteAccess(object):
    def __init__(self, host="192.168.2.8", user="zslab", password="labieee80211"):
        self.host = host
        self.user = user
        self.password = password
        self.client = None
        

    def establishConnection(self):
        try:
            self.client = paramiko.SSHClient()
        except Exception as E:
            print ("Opening SSHClient Got failed")
            ERROR(E)
            return False
            
        try:
            self.client.load_system_host_keys()
        except Exception as E:
            print ("Loading system host key Got failed")
            ERROR(E)
            return False
            
        try:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        except Exception as E:
            print ("Setting missing host key policy Got failed")
            ERROR(E)
            return False
            
        try:
            INFO("Try to establish connection with client: {}, username: {}, password: {}".format(self.host, self.user, self.password))
            self.client.connect(self.host, username=self.user, password=self.password, timeout=30)
            return True
        except socket.error as E:
            print ("Socket Error occurred")
            ERROR(E)
        except paramiko.AuthenticationException as E:
            print ("Authentication Failed")
            ERROR(E)
        except Exception as E:
            ERROR(E)
            
        return False

    def checkClientActive(self):
        try:
            INFO("Check whether client is alive")
            stdin,stdout,stderr = self.client.exec_command("ls", timeout=10)
            SUCCESS("Connection is alive")
            return True
        except Exception as e:
            ERROR(e)
            return False
            

    def executeCommand(self, command=None):
        if self.client == None:
            self.establishConnection()
            
        if self.checkClientActive() == False:
            ERROR("client not in active state")
            return False
        
        if command != None:
            try:
                INFO("Try to execute command : {}".format(command))
                stdin,stdout,stderr = self.client.exec_command(command, timeout=120)
                out = stdout.read()
                err = stderr.read()
                exec_status = stdout.channel.recv_exit_status()
                if exec_status == 0:
                    return out
                else:
                    FAIL(err)
                    return False
            except Exception as E:
                ERROR("Command execution Failed")
                ERROR(E)
                return False
        else:
            ERROR("Command is empty")
            return False


    def executeCommandInBackground(self, command=None):
        if self.client == None:
            self.establishConnection()
            
        if self.checkClientActive() == False:
            ERROR("client not in active state")
            return False
        
        if command != None:
            try:
                INFO("Try to execute command in background : {}".format(command))
                t = self.client.get_transport()
                ch = t.open_session()
                ch.exec_command(command)
                time.sleep(5)
                if ch.exit_status_ready():
                    INFO("Exit status is ready...")
                    status = ch.recv_exit_status()
                    INFO("Exit status is : {}".format(status))
                    if status == 0:
                        return True
                    return False
                return True
            except Exception as E:
                print ("Command execution Failed")
                ERROR(E)
                return False
        else:
            ERROR("Command is empty")
            return False


    def checkClientConnectedWithInternet(self):
        if self.client == None:
            self.establishConnection()
            
        if self.checkClientActive() == False:
            ERROR("client not in active state")
            return False
        
        try:
            INFO("Check whether client is connected with internet")
            stdin,stdout,stderr = self.client.exec_command("ping -c 3 8.8.8.8", timeout=30)
            exec_status = stdout.channel.recv_exit_status()
            if exec_status == 0:
                return True
            else:
                return False
        except Exception as e:
            ERROR(e)
            return False


    def copyToClient(self, source=None, destination=None):
        if self.client == None:
            self.establishConnection()
            
        if self.checkClientActive() == False:
            ERROR("client not in active state")
            return False
        
        try:
            INFO("Try to get transport from client for SCP")
            s = scp.SCPClient(self.client.get_transport())
        except Exception as E:
            ERROR(E)
            return False

        try:
            INFO("Try to copy '{}' to '{}'".format(source, destination))
            s.put(source, destination, recursive=True)
        except Exception as E:
            s.close()
            ERROR(E)
            return False
        
        s.close()
        return True


    def copyFromClient(self, source=None, destination=None):
        if self.client == None:
            self.establishConnection()
            
        if self.checkClientActive() == False:
            ERROR("client not in active state")
            return False
        
        try:
            INFO("Try to get transport from client for SCP")
            s = scp.SCPClient(self.client.get_transport())
        except Exception as E:
            ERROR(E)
            return False

        try:
            INFO("Try to copy '{}' to '{}'".format(source, destination))
            s.get(source, destination, recursive=True)
        except Exception as E:
            s.close()
            ERROR(E)
            return False
        
        s.close()
        return True
        
def parse_arguments():
    try:
        options, arguments = getopt.getopt(sys.argv[1:], "t:f:a:", ["logduration=", "logfile=", "applicationname="])
    except getopt.GetoptError:
        print ("ipcamd_thread_details.py -f <logfile>")
        exit(2)

    global LOG_FILE

    for opt, arg in options:
        if opt in ('-f', '--logfile'):
            LOG_FILE = arg
    pass
            

if __name__ == "__main__":
    # c = remoteAccess()
    # status = c.executeCommand("ls -l /tmp")
    # print (status)
    # status = c.executeCommandInBackground("iperf3 -s")
    # print (status)
    # status = c.checkClientConnectedWithInternet()
    # print (status)
    # status = c.copyToClient("/home/user/script.sh", "/tmp")
    # print (status)
    # status = c.copyFromClient("/tmp/script.sh", "/tmp")
    # print (status)
    
    # internet_throughput_test()

    client1 = wifiClient1()
    client2 = wifiClient2()
    status = client1.client1ConnectWithAp("corono_5g")
    print ("-------------------------> STATUS : {}".format(status))
    status = client2.client2ConnectWithAp("corono_5g")
    print ("-------------------------> STATUS : {}".format(status))
    status = client2.client2ExportFileInBackground()
    print ("-------------------------> STATUS : {}".format(status))
