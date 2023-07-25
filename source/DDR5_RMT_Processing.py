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
# import tkinter as tk
from sklearn.utils import resample


# def openWindow():
#     frame = tk.Tk()
#     frame.title("Input")
#     frame.geometry('400x200')
#     compare = tk.Text(frame, height=5, width=20)
#     btn = tk.Button(frame, text='Enter', bd='5', command=frame.destroy)
#     btn.pack(side='bottom')
#     frame.mainloop()


def askInput():
    valid = False
    print("How many sets of data do you want to graph?")
    numData = input("Please enter a number between 1 and 3: ")
    while not valid:
        try:
            numData = int(numData)
        except ValueError:
            print(numData, "is not valid")
            numData = input("Please enter a number between 1 and 3: ")
        else:
            if numData < 1 or numData > 3:
                print(numData, "is not in the range [1,3]")
                numData = input("Please enter a number between 1 and 3: ")
            else:
                valid = True
    folders = []
    vendorNames = []
    for i in range(0, numData):
        folder = selectFolder()
        folders.append(folder)
        name = folder[folder.rfind("\\")+1:folder.rfind("_")]
        name = name[name.find("_")+1:name.rfind("_")]
        name = name[name.find("_")+1:]
        vendorNames.append(name)

    processData(folders, vendorNames)


def selectFolder():
    path = input("Enter the folder path and name: ")
    while not os.path.exists(path):
        print("The entered folder does not exist")
        path = input("Enter the folder path and name: ")
    return path


def processData(folders, vendorNames):
    print("Do you want to include the vertical margin line?")
    includeLine = input("Enter 'Y' or 'N': ")
    while includeLine != "Y" and includeLine != "N":
        print(includeLine, "is not valid")
        includeLine = input("Enter 'Y' or 'N': ")

    print("Do you want to use the bootstrapping method?")
    bootstrap = input("Enter 'Y' or 'N': ")
    while bootstrap != "Y" and bootstrap != "N":
        print(bootstrap, "is not valid")
        bootstrap = input("Enter 'Y' or 'N': ")

    allRankMarginCPU0, allLaneMarginCPU0 = [None] * len(folders), [None] * len(folders)
    allRankMarginCPU1, allLaneMarginCPU1, variableList = [None] * len(folders), [None] * len(folders), [None] * len(folders)
    for i in range(0, len(folders)):
        allRankMarginCPU0[i], allLaneMarginCPU0[i], allRankMarginCPU1[i], allLaneMarginCPU1[i], variableList = readData(os.listdir(folders[i]), folders[i])

    makeGraphs(allRankMarginCPU0, variableList, vendorNames, includeLine, bootstrap, "CPU0 Rank Margin")
    makeGraphs(allLaneMarginCPU0, variableList, includeLine, bootstrap, "CPU0 Lane Margin")
    
    makeGraphs(allRankMarginCPU1, variableList, includeLine, bootstrap, "CPU1 Rank Margin")
    makeGraphs(allLaneMarginCPU1, variableList, includeLine, bootstrap, "CPU1 Lane Margin")

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
    histFig, histAxs = plt.subplots(2, 4)
    boxFig, boxAxs = plt.subplots(2, 4)
    bitMargFig, bitMargAxs = plt.subplots(2, 4)

    allMean = []
    allMedian = []
    allSD = []
    allIQR = []
    allMeanSD1 = []
    allMeanSD2 = []
    allMeanSD3 = []

    for i in range(1, 9):
        columns, x, y, mean, median, sd, iqr, meanSD1, meanSD2, meanSD3 = makeHistogram(allMarginList, vendorNames, variableList[i - 1], i,
                                                                                        histAxs, includeLine, bootstrap)
        makeBoxPlot(columns, vendorNames, variableList[i - 1], x, y, boxAxs, includeLine)
        makeBitMargin(columns, vendorNames, variableList[i - 1], x, y, bitMargAxs, includeLine)

        allMean.append(mean)
        allMedian.append(median)
        allSD.append(sd)
        allIQR.append(iqr)
        allMeanSD1.append(meanSD1)
        allMeanSD2.append(meanSD2)
        allMeanSD3.append(meanSD3)

    histFig.subplots_adjust(top=0.9, bottom=0.18, wspace=0.3, hspace=0.75)
    boxFig.subplots_adjust(top=0.85, bottom=0.05, wspace=0.3, hspace=0.3)
    bitMargFig.subplots_adjust(top=0.85, bottom=0.05, wspace=0.3, hspace=0.3)

    histFig.suptitle(marginType)
    boxFig.suptitle(marginType)
    bitMargFig.suptitle(marginType)

    makeTable(variableList, vendorNames, allMean, allMedian, allSD, allIQR, allMeanSD1, allMeanSD2, allMeanSD3, marginType)

    histFig.savefig(marginType.replace(" ", "") + "Histogram.pdf")
    boxFig.savefig(marginType.replace(" ", "") + "BoxPlot.pdf")
    bitMargFig.savefig(marginType.replace(" ", "") + "BitMargin.pdf")


def createCSVFile(fileName, variableList, rankMarginData):
    variableList.insert(0, "")
    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(variableList)
        writer.writerows(rankMarginData)
    variableList.pop(0)


def makeBitMargin(columns, vendorNames, variableList, x, y, axs, includeLine):
    for i in range(0, len(columns)):
        axs[x, y].scatter(range(0, len(columns[i])), columns[i], label=vendorNames[i], alpha=0.5, edgecolor='black')

    axs[x, y].legend(fontsize='5', loc='upper left')
    axs[x, y].set_title(variableList)

    if includeLine == "Y":
        axs[x, y].axhline(y=6, linestyle='dotted')

    axs[x, y].plot()


def makeBoxPlot(columns, vendorNames, variableList, x, y, axs, includeLine):
    axs[x, y].boxplot(columns, labels=vendorNames)

    axs[x, y].tick_params(axis='both', which='major', labelsize=5)
    axs[x, y].set_title(variableList)

    if includeLine == "Y":
        axs[x, y].axhline(y=6, linestyle='dotted')
    axs[x, y].plot()


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
    tableFig.savefig(marginType.replace(" ", "") + "DataTable.pdf", bbox_inches='tight')


def makeHistogram(rankMarginList, vendorNames, variableList, graphNum, axs, includeLine, bootstrap):
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

        axs[x, y].hist(columns[i], bins[i], label=vendorNames[i], alpha=0.5, edgecolor='black')
        axs[x, y].legend(fontsize='5', loc='upper left')

        mean.append(round(stats.mean(columns[i]), 4))
        median.append(round(stats.median(columns[i]), 4))
        stdev.append(round(stats.stdev(columns[i]), 4))
        iqr.append(round(np.subtract(*np.percentile(columns[i], [75, 25])), 4))
        meanSD1.append(round(mean[i] - stdev[i], 4))
        meanSD2.append(round(mean[i] - (2 * stdev[i]), 4))
        meanSD3.append(round(mean[i] - (3 * stdev[i]), 4))

    axs[x, y].tick_params(axis='both', which='major', labelsize=5)
    axs[x, y].grid(linestyle='dotted')
    axs[x, y].set_title(variableList)

    if includeLine == "Y":
        axs[x, y].axvline(x=6, linestyle='dotted')
    axs[x, y].plot()

    row_labels = ['mean', 'standard\ndeviation']
    table_vals = [mean, stdev]
    table = axs[x, y].table(cellText=table_vals, rowLabels=row_labels, colLabels=vendorNames,
                            bbox=[0.15, -0.5, 0.85, 0.35])
    table.auto_set_font_size(False)
    table.set_fontsize(4.5)

    return columns, x, y, mean, median, stdev, iqr, meanSD1, meanSD2, meanSD3


if __name__ == "__main__":
    # openWindow()
    askInput()
