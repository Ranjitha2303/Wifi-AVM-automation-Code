import serial
import wifiConfig
import time

import testLogs


currentPosition = 0


def writeIntoTtSerialPort(data=None):
    if data == None:
        testLogs.ERROR ("Please provide data to write into Turn Table's serial port")
        exit(1)
        
    try:
        ser = serial.Serial(wifiConfig.ttPort, wifiConfig.ttBaudrate)
        ser.write(data)
        ser.close()
    except Exception as E:
        testLogs.ERROR ("Could not write into Turn Table's serial port")
        testLogs.ERROR (E)
        exit(1)


def rotateTtClockWise(angle):
    angleToWrite = str(int(wifiConfig.ttStepsPerAngle * angle)) + 's'
    writeIntoTtSerialPort(angleToWrite.encode())
    wifiConfig.currentAngle += int(angle)


def rotateTtAntiClockWise(angle):
    angleToWrite = str(int(wifiConfig.ttStepsPerAngle * angle)) + '-s'
    writeIntoTtSerialPort(angleToWrite.encode())
    wifiConfig.currentAngle -= int(angle)
    

def rotateTurnTable(angle = wifiConfig.anglePerMove):
    #if direction == 0:
    #    rotateTtClockWise(angle)
    #elif direction == 1:
    #    rotateTtAntiClockWise(angle)
    rotateTtClockWise(angle)
    waitTime = angle * wifiConfig.ttStepsPerAngle * wifiConfig.ttTimePerStep
    time.sleep(waitTime + 1)
    testLogs.INFO ("Rotation completed")


if __name__ == '__main__':
    wifiConfig.parseWifiCommandLineArgs()
    #for angle in range(0, 35):
    #    testLogs.INFO ("Moving to angle : {}".format((angle + 1) * 10))
    #    rotateTurnTable(10)
    #    testLogs.INFO ("Moved")
    #time.sleep(5)
    #setTtToInitialPosition()
    rotateTurnTable(wifiConfig.anglePerMove)
