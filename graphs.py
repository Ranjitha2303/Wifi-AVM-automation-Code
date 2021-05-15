import matplotlib.pyplot as plt
import numpy as np


import testLogs
import wifiConfig


def createSingleRadarGraph(listValue=[5, 6, 7, 6, 5, 10, 2], fileName="radarChart"):
    
    testLogs.INFO ("FUNCTION : Creating Single Radar Graph")
    
    fig = plt.figure()
    po = fig.add_subplot(111, polar=True)
    po.grid(True)

    
    anglePerValue = int(360 / len(listValue))
    namesOfEachValue = [anglePerValue * ele for ele in range(1, len(listValue) + 1)]
    
    N = len(listValue)  # Number of values
    testLogs.INFO ("length of the list is : {}".format(N))
    
    listValue += listValue[:1] # Repeat first value to close the circle
    testLogs.INFO ("listValuse after alter : {}".format(listValue))

    angles = [n / float(N) * 2 * np.pi for n in range(N)] # Calculate angle for each value
    angles += angles[:1]
    testLogs.INFO ("Angles calculated : {}".format(angles))

    listValue = [int(float(i)) for i in listValue]; po.plot(angles, listValue)
    po.set_theta_direction(-1)
    po.set_theta_offset(np.pi/2.0)
    
    plt.xticks(angles[:-1], namesOfEachValue)
    if wifiConfig.test == 0:
        label = wifiConfig.graphLegend[wifiConfig.test][wifiConfig.build]
    if wifiConfig.test == 1:
        label = wifiConfig.graphLegend[wifiConfig.test][wifiConfig.ap]
    if wifiConfig.test == 2 or wifiConfig.test == 3:
        label = wifiConfig.graphLegend[wifiConfig.test][wifiConfig.band]
        
    plt.legend(labels=[label,], loc='upper right', bbox_to_anchor=(wifiConfig.legendXpos, wifiConfig.legendYpos), ncol=2, fancybox=True, shadow=True)
    plt.xlabel(wifiConfig.labelXname)
    plt.ylabel(wifiConfig.labelYname)
    plt.title(wifiConfig.graphTitle)
    
    #graphDirectory = "{}\\output\\{}_{}_{}\\graphs\\".format(wifiConfig.baseDirectory, wifiConfig.tests[wifiConfig.test], wifiConfig.aps[wifiConfig.ap], wifiConfig.builds[wifiConfig.build])
    #plt.savefig(graphDirectory + fileName + '_RADAR.png')
    plt.savefig(fileName + '_RADAR.png')



def createMultipleRadarGraph(listValue=[[5, 6, 7, 6, 5, 10, 2], [2, 7, 5, 10, 6, 5, 5]],
                                        fileName="testGraph"):
    
    testLogs.INFO ("FUNCTION : Creating Multiple Radar Graph")
    fig = plt.figure()
    po = fig.add_subplot(111, polar=True)
    po.grid(True)
    
    if 360 % len(listValue[0]) == 0:
        anglePerValue = int(360 / len(listValue[0]))
    else:
        anglePerValue = 360 / len(listValue[0])
    namesOfEachValue = [int(float(anglePerValue * ele)) for ele in range(1, len(listValue[0]) + 1)]
    N = len(listValue[0])  # Number of values

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    colors = ['g', 'y', 'b', 'r', 'm', 'c', 'k', 'w']
    for index, l in enumerate(listValue):
        l += l[:1] # Repeat first value to close the circle
        l = [int(float(i)) for i in l]
        po.plot(angles, l)

    po.set_theta_direction(-1)
    po.set_theta_offset(np.pi/2.0)
    plt.xticks(angles[:-1], namesOfEachValue)
    plt.legend(labels=wifiConfig.graphLegend[wifiConfig.test], loc='upper right', bbox_to_anchor=(wifiConfig.legendXpos, wifiConfig.legendYpos), ncol=2, fancybox=True, shadow=True, prop={'size': 8})
    plt.xlabel(wifiConfig.labelXname)
    plt.ylabel(wifiConfig.labelYname)
    plt.title(wifiConfig.graphTitle)
    
    #graphDirectory = "{}\\output\\{}_{}_{}\\graphs\\".format(wifiConfig.baseDirectory, wifiConfig.tests[wifiConfig.test], wifiConfig.aps[wifiConfig.ap], wifiConfig.builds[wifiConfig.build])
    #plt.savefig(graphDirectory + fileName + '_RADAR.png')
    plt.savefig(fileName + '_RADAR.png')
    #plt.show()

def createSingleBarGraph(listValue=[5, 6, 7, 6, 5, 10, 2],
                         fileName="avmGraph"):
    
    testLogs.INFO ("FUNCTION : Creating Single Bar Graph")
    # Bar chart
    list1 = [int(float(i)) for i in listValue]
    minValue1 = min(list1)
    avgValuse1 = int(sum(list1) / len(list1))
    maxValue1 = max(list1)

    values1 = [minValue1, avgValuse1, maxValue1]
    
    N = len(values1)
    indentation = np.arange(N)

    fig, ax = plt.subplots()
    ax.bar(indentation, values1, width=wifiConfig.barWidth)

    for index,data in enumerate(values1):
        plt.text(x=index , y =data+1 , s=f"{data}" , fontdict=dict(fontsize=12))
        
    # plt.tight_layout()
    plt.xticks(indentation + wifiConfig.barWidth / 2, wifiConfig.barXticks[0])
    if wifiConfig.test == 0:
        label = wifiConfig.graphLegend[wifiConfig.test][wifiConfig.build]
    if wifiConfig.test == 1:
        label = wifiConfig.graphLegend[wifiConfig.test][wifiConfig.ap]
    if wifiConfig.test == 2 or wifiConfig.test == 3:
        label = wifiConfig.graphLegend[wifiConfig.test][wifiConfig.band]
        
    ax.legend(labels=[label,], loc='upper right', bbox_to_anchor=(wifiConfig.legendXpos, wifiConfig.legendYpos), ncol=2, fancybox=True, shadow=True, prop={'size': 8})
    plt.xlabel(wifiConfig.labelXname)
    plt.ylabel(wifiConfig.labelYname)
    plt.title(wifiConfig.graphTitle)
    
    #graphDirectory = "{}\\output\\{}_{}_{}\\graphs\\".format(wifiConfig.baseDirectory, wifiConfig.tests[wifiConfig.test], wifiConfig.aps[wifiConfig.ap], wifiConfig.builds[wifiConfig.build])
    #plt.savefig(graphDirectory + fileName + '_BAR.png')
    plt.savefig(fileName + '_BAR.png')


def createMultipleBarGraph(listValue=[[5, 6, 7, 6, 5, 10],
                                      [2, 7, 5, 10, 6, 5]],
                                      fileName="avmGraph"):
    
    testLogs.INFO ("FUNCTION : Creating Multiple Bar Graph")

    fig, ax = plt.subplots()

    for index, lst in enumerate(listValue):
        if wifiConfig.test in [0, 1, 2, 3]:
            data = [min(lst), int(sum(lst) / len(lst)), max(lst)]
        else:
            data = lst
        testLogs.INFO("data is : {}".format(data))
        N = len(data)
        indentation = np.arange(N)
        ax.bar(indentation + (index * wifiConfig.barWidth), data, width = wifiConfig.barWidth)
        for ind, dat in enumerate(data):
            testLogs.INFO("dat is : {}".format(dat))
            plt.text(x = ind + (index * wifiConfig.barWidth), y = dat + 1, s=f"{dat}", fontdict=dict(fontsize=12))
    # plt.tight_layout()
    plt.xticks(indentation + wifiConfig.barWidth / 2, wifiConfig.barXticks[0])
    ax.legend(labels=wifiConfig.graphLegend[wifiConfig.test], loc='upper right', bbox_to_anchor=(wifiConfig.legendXpos, wifiConfig.legendYpos), ncol=2, fancybox=True, shadow=True, prop={'size': 8})
    plt.xlabel(wifiConfig.labelXname)
    plt.ylabel(wifiConfig.labelYname)
    plt.title(wifiConfig.graphTitle)
    
    #graphDirectory = "{}\\output\\{}_{}_{}\\graphs\\".format(wifiConfig.baseDirectory, wifiConfig.tests[wifiConfig.test], wifiConfig.aps[wifiConfig.ap], wifiConfig.builds[wifiConfig.build])
    #plt.savefig(graphDirectory + fileName + '_BAR.png')
    plt.savefig(fileName + '_BAR.png')


if __name__ == '__main__':
    wifiConfig.parseWifiCommandLineArgs()
    createMultipleBarGraph(fileName = '{}_{}_{}_{}'.format(wifiConfig.streams[wifiConfig.stream],
                                                           wifiConfig.bands[wifiConfig.band],
                                                           wifiConfig.protocols[wifiConfig.protocol],
                                                           wifiConfig.links[wifiConfig.link]))
