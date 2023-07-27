# ----------------------------------------------
# File name: RMT_Processing.py
# Author: Jean Mattekatt
# Date: 7/11/2023

# Description: This code reads DDR5 data and converts it into a histogram, table, boxplot, and bit margin (scatterplot)
# ----------------------------------------------

# pip install matplotlib
# pip install scikit-learn

import os
import numpy as np
import matplotlib.pyplot as plt
import statistics as stats
import csv
from sklearn.utils import resample


def processData(folders, vendorNames, bootstrap, includeLine):
    allRankMarginCPU0, allLaneMarginCPU0 = [None] * len(folders), [None] * len(folders)
    allRankMarginCPU1, allLaneMarginCPU1, variableList = [None] * len(folders), [None] * len(folders), [None] * len(folders)
    for i in range(0, len(folders)):
        allRankMarginCPU0[i], allLaneMarginCPU0[i], allRankMarginCPU1[i], allLaneMarginCPU1[i], variableList = readData(os.listdir(folders[i]), folders[i])

    makeGraphs(allRankMarginCPU0, variableList, vendorNames, includeLine, bootstrap, "CPU0 Rank Margin")
    # makeGraphs(allLaneMarginCPU0, variableList, vendorNames, includeLine, bootstrap, "CPU0 Lane Margin")
    
    # makeGraphs(allRankMarginCPU1, variableList, vendorNames, includeLine, bootstrap, "CPU1 Rank Margin")
    # makeGraphs(allLaneMarginCPU1, variableList, vendorNames, includeLine, bootstrap, "CPU1 Lane Margin")

    plt.show()


def readData(folder, folderPath):
    allRankMarginCPU0 = []
    allLaneMarginCPU0 = []

    allRankMarginCPU1 = []
    allLaneMarginCPU1 = []

    variableListCPU0 = ""

    for fileName in folder:
        file = open(folderPath + "\\" + fileName, "r")
        text = file.readlines()
        dataCPU0 = ""
        dataCPU1 = ""
        recordCPU0Data = False
        recordCPU1Data = False
        for line in text:
            if line.find("START_RMT_N0") != -1:
                recordCPU0Data = True
            if line.find("STOP_RMT_N0") != -1:
                recordCPU0Data = False
            if recordCPU0Data:
                dataCPU0 = dataCPU0 + line
            if line.find("START_RMT_N1") != -1:
                recordCPU1Data = True
            if line.find("STOP_RMT_N1") != -1:
                recordCPU1Data = False
            if recordCPU1Data:
                dataCPU1 = dataCPU1 + line
        file.close()

        rankMarginCPU0, laneMarginCPU0, variableListCPU0 = separateCPU(dataCPU0, fileName, str(0))
        rankMarginCPU1, laneMarginCPU1, variableListCPU1 = separateCPU(dataCPU1, fileName, str(1))

        allRankMarginCPU0.extend(rankMarginCPU0)
        allLaneMarginCPU0.extend(laneMarginCPU0)

        allRankMarginCPU1.extend(rankMarginCPU1)
        allLaneMarginCPU1.extend(laneMarginCPU1)

    return allRankMarginCPU0, allLaneMarginCPU0, allRankMarginCPU1, allLaneMarginCPU1, variableListCPU0


def separateCPU(data, filePath, cpuNum):
    rankMargin = data[data.find("Rank Margin"):data.find("Lane Margin")]
    laneMargin = data[data.find("Lane Margin"):data.find("CA Lane Margin")]

    variableList = rankMargin[rankMargin.find("RxDqs-"):rankMargin.find("\nN" + cpuNum)]
    variableList = list(filter(None, variableList.split(" ")))

    rankMargin = separateMarginData(rankMargin, variableList, filePath, "CPU" + cpuNum + "RankMargin")
    laneMargin = separateMarginData(laneMargin, variableList, filePath, "CPU" + cpuNum + "LaneMargin")

    return rankMargin, laneMargin, variableList


def separateMarginData(data, variableList, filePath, marginType):
    data = data[data.find("N" + marginType[3]):data.rfind("\nIoLevel")]
    data = data.splitlines()
    for i in range(0, len(data)):
        data[i] = list(filter(None, data[i].split(" ")))
    createCSVFile(filePath[:filePath.rfind(".")] + marginType + '.csv', variableList, data)
    return data


def makeGraphs(allMarginList, variableList, vendorNames, includeLine, bootstrap, marginType):
    boxFig, boxAxs = plt.subplots(2, 4)
    bitMargFig, bitMargAxs = plt.subplots(2, 4)
    tableFig, tableAxs = plt.subplots(2, 4)

    allMean = []
    allMedian = []
    allSD = []
    allIQR = []
    allMeanSD1 = []
    allMeanSD2 = []
    allMeanSD3 = []

    for i in range(0, len(vendorNames)):
        histFig, histAxs = plt.subplots(2, 4)

        for j in range(1, 9):
            makeHistogram(allMarginList[i], variableList[j - 1], j, histAxs, includeLine, bootstrap)

        histFig.subplots_adjust(top=0.9, bottom=0.18, wspace=0.3, hspace=0.75)
        histFig.suptitle(vendorNames[i] + " " + marginType)
        histFig.savefig(vendorNames[i] + marginType.replace(" ", "") + "Histogram.pdf")


    for i in range(1, 9):
        columns, x, y, mean, median, sd, iqr, meanSD1, meanSD2, meanSD3 = calculateStats(allMarginList, i, bootstrap)
        makeBoxPlot(columns, vendorNames, variableList[i - 1], boxAxs[x, y], includeLine)
        makeBitMargin(columns, vendorNames, variableList[i - 1], bitMargAxs[x, y], includeLine)
        makeVarTable(mean, median, sd, iqr, meanSD1, meanSD2, meanSD3, vendorNames, variableList[i-1], tableAxs[x, y])

        allMean.append(mean)
        allMedian.append(median)
        allSD.append(sd)
        allIQR.append(iqr)
        allMeanSD1.append(meanSD1)
        allMeanSD2.append(meanSD2)
        allMeanSD3.append(meanSD3)

    boxFig.subplots_adjust(top=0.85, bottom=0.05, wspace=0.3, hspace=0.3)
    bitMargFig.subplots_adjust(top=0.85, bottom=0.05, wspace=0.3, hspace=0.3)
    tableFig.subplots_adjust(top=0.85, bottom=0.05, wspace=0.63)

    boxFig.suptitle(marginType)
    bitMargFig.suptitle(marginType)
    tableFig.suptitle(marginType)

    makeTable(variableList, vendorNames, allMean, allMedian, allSD, allIQR, allMeanSD1, allMeanSD2, allMeanSD3, marginType)

    boxFig.savefig(marginType.replace(" ", "") + "BoxPlot.pdf")
    bitMargFig.savefig(marginType.replace(" ", "") + "BitMargin.pdf")
    tableFig.savefig(marginType.replace(" ", "") + "VarTable.pdf", bbox_inches='tight')


def createCSVFile(fileName, variableList, rankMarginData):
    variableList.insert(0, "")
    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(variableList)
        writer.writerows(rankMarginData)
    variableList.pop(0)


def makeVarTable(mean, median, sd, iqr, meanSD1, meanSD2, meanSD3, vendorNames, variable, axs):
    axs.axis('tight')
    axs.axis('off')

    row = ["Mean", "Median", "SD", "IQR", "Mean-1SD", "Mean-2SD", "Mean-3SD"]
    axs.table(cellText=[mean, median, sd, iqr, meanSD1, meanSD2, meanSD3], rowLabels=row, colLabels=vendorNames, loc='center')
    axs.set_title(variable)

def makeBitMargin(columns, vendorNames, variable, axs, includeLine):
    for i in range(0, len(columns)):
        axs.scatter(range(0, len(columns[i])), columns[i], label=vendorNames[i], alpha=0.5)

    axs.legend(fontsize='5', loc='upper left')
    axs.set_title(variable)

    if includeLine == "Y":
        axs.axhline(y=6, linestyle='dotted')

    axs.plot()


def makeBoxPlot(columns, vendorNames, variable, axs, includeLine):
    axs.boxplot(columns, labels=vendorNames)

    axs.tick_params(axis='both', which='major', labelsize=5)
    axs.set_title(variable)

    if includeLine == "Y":
        axs.axhline(y=6, linestyle='dotted')
    axs.plot()


def makeTable(variableList, vendorNames, allMean, allMedian, allSD, allIQR, allMeanSD1, allMeanSD2, allMeanSD3, marginType):
    dataNum = len(allMean[0])
    rowTot, colTot = dataNum, 1

    if dataNum > 2:
        rowTot, colTot = 2, 2
    tableFig, tableAx = plt.subplots(rowTot, colTot, squeeze=False)
    for col in range(0, colTot):
        for row in range(0, rowTot):
            tableAx[row, col].axis('tight')
            tableAx[row, col].axis('off')

    rows = ["Mean", "Median", "SD", "IQR", "Mean-1SD", "Mean-2SD", "Mean-3SD"]
    for tableNum in range(0, dataNum):
        col = 0
        row = tableNum
        if tableNum + 1 > 2:
            col = 1
            row = tableNum % 2

        meanRow, medianRow, sdRow, iqrRow, meanSD1Row, meanSD2Row, meanSD3Row = [], [], [], [], [], [], []
        for colNum in range(0, len(allMean)):
            meanRow.append(allMean[colNum][tableNum])
            medianRow.append(allMedian[colNum][tableNum])
            sdRow.append(allSD[colNum][tableNum])
            iqrRow.append(allIQR[colNum][tableNum])
            meanSD1Row.append(allMeanSD1[colNum][tableNum])
            meanSD2Row.append(allMeanSD2[colNum][tableNum])
            meanSD3Row.append(allMeanSD3[colNum][tableNum])
        tableAx[row, col].table(cellText=[meanRow, medianRow, sdRow, iqrRow, meanSD1Row, meanSD2Row, meanSD3Row],
                                rowLabels=rows, colLabels=variableList, loc='center')
        tableAx[row, col].set_title(vendorNames[tableNum])

    tableFig.suptitle(marginType)
    tableFig.subplots_adjust(top=0.85, bottom=0.04, hspace=0.75)
    tableFig.savefig(marginType.replace(" ", "") + "VendorTable.pdf", bbox_inches='tight')

def calculateStats(rankMarginList, graphNum, bootstrap):
    x = 0
    y = graphNum - 1
    if graphNum > 4:
        x = 1
        y = (graphNum - 1) % 4
    
    columns, bins = [], []
    mean, median, stdev, iqr, meanSD1, meanSD2, meanSD3 = [], [], [], [], [], [], []

    for i in range(0, len(rankMarginList)):

        columns.append([])
        for j in range(0, len(rankMarginList[i])):
            columns[i].append(abs(int(rankMarginList[i][j][graphNum])))

        if bootstrap == "Y":
            columns[i] = resample(columns[i], replace=True, n_samples=1000, random_state=1)

        bins.append(range(min(columns[i]), max(columns[i]) + 2))

        mean.append(round(stats.mean(columns[i]), 4))
        median.append(round(stats.median(columns[i]), 4))
        stdev.append(round(stats.stdev(columns[i]), 4))
        iqr.append(round(np.subtract(*np.percentile(columns[i], [75, 25])), 4))
        meanSD1.append(round(mean[i] - stdev[i], 4))
        meanSD2.append(round(mean[i] - (2 * stdev[i]), 4))
        meanSD3.append(round(mean[i] - (3 * stdev[i]), 4))

    return columns, x, y, mean, median, stdev, iqr, meanSD1, meanSD2, meanSD3

def makeHistogram(rankMarginList, variable, graphNum, axs, includeLine, bootstrap):    
    x = 0
    y = graphNum - 1
    if graphNum > 4:
        x = 1
        y = (graphNum - 1) % 4

    columns = []

    for i in range(0, len(rankMarginList)):
        columns.append(abs(int(rankMarginList[i][graphNum])))

    if bootstrap == "Y":
        columns = resample(columns, replace=True, n_samples=1000, random_state=1)

    bins = range(min(columns), max(columns) + 2)

    axs[x, y].hist(columns, bins, edgecolor='black')

    mean = round(stats.mean(columns), 4)
    stdev = round(stats.stdev(columns), 4)

    axs[x, y].tick_params(axis='both', which='major', labelsize=5)
    axs[x, y].grid(linestyle='dotted')
    axs[x, y].set_title(variable)

    if includeLine == "Y":
        axs[x, y].axvline(x=6, linestyle='dotted')
    axs[x, y].plot()

    col_labels = ['mean', 'standard\ndeviation']
    table_vals = [mean, stdev]
    axs[x, y].table(cellText=[table_vals], colLabels=col_labels, bbox=[0, -0.5, 1, 0.35])
