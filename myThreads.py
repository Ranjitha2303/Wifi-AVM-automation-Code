import logging
import threading
import time

stopAllThreads = False

class myThreads(object):
    def __init__(self, callBackFunction = None, arguments = None):
        self.callBackFunction = callBackFunction
        self.arguments = arguments

    def __createThread(self):
        self.thread = threading.Thread(target=self.callBackFunction, args = (self.arguments, ))

    def __createDaemon(self):
        self.thread = threading.Thread(target=self.callBackFunction, args = (self.arguments, ), daemon = True)

    def startThread(self):
        self.__createThread()
        self.thread.start()

    def startThreadDaemon(self):
        self.__createDaemon()
        self.thread.start()
        #self.thread.join()


def callBack(count = 0):
    global stopThread
    count = 0
    while True:
        print ("Call Back funtion prints : {}".format(count))
        time.sleep(2)
        count += 1
        if stopAllThreads == True:
            print ("STOPS Thread")
            break


if __name__ == '__main__':
    callBackThread1 = myThreads(callBack, 10)
    print (dir(callBackThread1))
    callBackThread2 = myThreads(callBack, 10)
    callBackThread3 = myThreads(callBack, 10)
    callBackThread1.startThreadDaemon()
    callBackThread2.startThreadDaemon()
    callBackThread3.startThreadDaemon()
    count = 1
    while True:
        print ("Print From Main Fuction : {}".format(count))
        count += 1
        time.sleep(1)
        if count == 10:
            break
    time.sleep(10)
    stopAllThreads = True
    
    print ("END of MAIN Function")
