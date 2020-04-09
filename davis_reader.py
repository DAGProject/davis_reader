# -*- coding: utf-8 -*-
"""
@author: Recep Balbay
"""


import mysql.connector as mariadb
from datetime import datetime
from time import sleep
from os import mkdir, path

startVal = 0
basePath = path.dirname(path.realpath(__file__)) + "\\"
dataFolderPath = basePath + "DATA\\"
downloadFile = basePath + "download.txt"

davisSql = "INSERT INTO `2020`(`Date`, `TempOut`, `HiTemp`, `LowTemp`, `OutHum`, `DewPoint`, `WindSpeed`, `WindDir`," \
           " `WindRun`, `HiSpeed`, `HiDir`, `WindChill`, `HeatIndex`, `THWIndex`, `THWSIndex`, `Bar`, `Rain`," \
           " `RainRate`, `SolarRad`, `SolarEnergy`, `HiSolarRad`, `UVIndex`, `UVDose`, `HiUV`, `HeatDD`, `CoolDD`," \
           " `InTemp`, `InHum`, `InDewpoint`, `InHeat`, `InEMC`, `InAirDensity`, `ET`, `WindSamp`, `WindTx`, `ISSRecept`," \
           " `ArcInt`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
           " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


def UtcNow():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def dataFolder():
    year = datetime.utcnow().strftime('%Y') + "\\"

    if path.isdir(dataFolderPath):
        print(UtcNow() + " | DATA Folder is found.")
    else:
        try:
            print(UtcNow() + " | DATA Folder not found. Creating.")
            mkdir(dataFolderPath)
            sleep(1)
            print(UtcNow() + " | DATA Folder created: " + dataFolderPath)
        except WindowsError as w:
            print(UtcNow() + " | " + w.args[1])

    sleep(1)

    if path.isdir(dataFolderPath + year):
        print(UtcNow() + " | Year Folder is found.")
    else:
        try:
            print(UtcNow() + " | Year Folder not found. Creating.")
            mkdir(dataFolderPath + year)
            sleep(1)
            print(UtcNow() + " | Year Folder created: " + dataFolderPath + year)
        except WindowsError as w:
            print(UtcNow() + " | " + w.args[1])
    sleep(1)


def ReadDownload():
    dates = []
    with open(downloadFile) as f:
        davisData = f.readlines()
        davisData.pop(0)
        davisData.pop(0)
        davisData.pop(0)

        for i in davisData:
            dates.append(i.split()[0])

    return sorted(list(set(dates)))


def SplitDownload(t):
    yesterday = []
    today = []
    with open(downloadFile, 'r') as f:
        davisData = f.readlines()
        davisData.pop(0)
        davisData.pop(0)
        davisData.pop(0)

    for i in davisData:
        if i.split()[0] == t[0]:

            actLine = i.split()
            yy = actLine[0].split('.')[2]
            mo = actLine[0].split('.')[1]
            dd = actLine[0].split('.')[0]
            hh = actLine[1].split(':')[0]
            mn = actLine[1].split(':')[1]

            yy = '20' + yy

            if len(dd) == 1:
                dd = '0' + dd

            if len(hh) == 1:
                hh = '0' + hh

            davisDate = yy + '-' + mo + '-' + dd + ' ' + hh + ':' + mn + ':' + '00'
            todayName = yy + mo + dd + '.txt'
            actLine.pop(1)
            actLine[0] = davisDate  # Date corrections
            davisLine = ','.join(actLine) + "\n"
            today.append(davisLine)

        else:
            actLine = i.split()
            yy = actLine[0].split('.')[2]
            mo = actLine[0].split('.')[1]
            dd = actLine[0].split('.')[0]
            hh = actLine[1].split(':')[0]
            mn = actLine[1].split(':')[1]

            yy = '20' + yy

            if len(dd) == 1:
                dd = '0' + dd

            if len(hh) == 1:
                hh = '0' + hh

            davisDate = yy + '-' + mo + '-' + dd + ' ' + hh + ':' + mn + ':' + '00'
            yesterdayName = yy + mo + dd + '.txt'
            actLine.pop(1)
            actLine[0] = davisDate  # Date corrections
            davisLine = ','.join(actLine) + "\n"
            yesterday.append(davisLine)

    try:
        with open(todayName, 'w') as tmp:
            tmp.write(
                "YYYY-mm-DD HH:MM:SS.SS, TempOut, HiTemp, LowTemp, OutHum, DewPoint, WindSpeed, WindDir, WindRun,"
                "HiSpeed, HiDir, WindChill, HeatIndex, THWIndex, THWSIndex, Bar, Rain, RainRate, SolarRad,"
                "SolarEnergy, HiSolarRad, UVIndex, UVDose, HiUV, HeatDD, CoolDD, InTemp, InHum, InDewp, InHeat,"
                "InEMC, InAirDensity, ET, WindSamp, WindTx, ISSRecept, ArcInt\n")
            for i in today:
                tmp.writelines(i)
    except WindowsError as w:
        print(UtcNow() + " | " + w.args[1])

    sleep(1)

    try:
        with open(yesterdayName, 'w') as tmp:
            tmp.write("YYYY-mm-DD HH:MM:SS.SS, TempOut, HiTemp, LowTemp, OutHum, DewPoint, WindSpeed, WindDir, WindRun,"
                      "HiSpeed, HiDir, WindChill, HeatIndex, THWIndex, THWSIndex, Bar, Rain, RainRate, SolarRad,"
                      "SolarEnergy, HiSolarRad, UVIndex, UVDose, HiUV, HeatDD, CoolDD, InTemp, InHum, InDewp, InHeat,"
                      "InEMC, InAirDensity, ET, WindSamp, WindTx, ISSRecept, ArcInt\n")
            for i in yesterday:
                tmp.writelines(i)
    except WindowsError as w:
        print(UtcNow() + " | " + w.args[1])


def Work(day):
    yy = day.split('.')[2]
    mo = day.split('.')[1]
    dd = day.split('.')[0]
    yy = '20' + yy

    if len(dd) == 1:
        dd = '0' + dd

    year = datetime.utcnow().strftime('%Y') + "\\"
    dayFile = dataFolderPath + year + yy + mo + dd + ".txt"

    TempFile = yy + mo + dd + '.txt'

    if path.exists(dayFile):
        TempHours = []
        OrginalHours = []
        with open(TempFile, 'r') as temp:
            tmp = temp.readlines()
            tmp.pop(0)

            for i in tmp:
                TempHours.append(i.split(",")[0])
        temp.close()

        with open(dayFile, 'r') as dayF:
            dF = dayF.readlines()
            dF.pop(0)

            for i in dF:
                OrginalHours.append(i.split(",")[0])
        dayF.close()

        HoursDiff = sorted(list(set(TempHours) - set(OrginalHours)))

        if len(HoursDiff) >= 1:
            print(UtcNow() + " | Adding Line Length: " + str(len(HoursDiff)))
            sleep(1)
            with open(dayFile, 'a') as DF:
                for ii in range(len(HoursDiff)):
                    AddingLine = tmp[TempHours.index(HoursDiff[ii])]
                    DF.write(AddingLine)

            print(UtcNow() + " | Lines added: " + dayFile)

            sleep(1)

            try:
                AtaDb = mariadb.connect(
                    host="",                    # Server IP Adress
                    user="",                    # Username
                    passwd="",                  # Password
                    database='davis-mam')
                AtaDbCursor = AtaDb.cursor()

                for j in range(len(HoursDiff)):
                    AddingLine = tmp[TempHours.index(HoursDiff[j])].strip().split(",")
                    AtaDbCursor.execute(davisSql, AddingLine)
                    AtaDb.commit()
                    sleep(0.1)

                print(UtcNow() + " | Job is done. Next job is begin in 10s.")

            except Exception as sqlError:
                print(UtcNow() + " | " + getattr(sqlError, 'message', repr(sqlError)))

            sleep(10)

        else:
            print(UtcNow() + " | No lines added. Working file: " + dayFile)
            sleep(1)
            print(UtcNow() + " | Job is done. Next job is begin in 10s.")
            sleep(10)

    else:
        print(UtcNow() + " | DAY file not found. Creating.")
        with open(dayFile, 'w') as day:
            day.write("YYYY-mm-DD HH:MM:SS.SS, TempOut, HiTemp, LowTemp, OutHum, DewPoint, WindSpeed, WindDir, WindRun,"
                      "HiSpeed, HiDir, WindChill, HeatIndex, THWIndex, THWSIndex, Bar, Rain, RainRate, SolarRad,"
                      "SolarEnergy, HiSolarRad, UVIndex, UVDose, HiUV, HeatDD, CoolDD, InTemp, InHum, InDewp, InHeat,"
                      "InEMC, InAirDensity, ET, WindSamp, WindTx, ISSRecept, ArcInt\n")
            sleep(1)

        print(UtcNow() + " | DAY file created: " + dayFile)


while True:
    try:
        if startVal == 0:
            sleep(1)
            print(UtcNow() + " | ------------------------ ATASAM DAVIS PROGRAM v.1.7 --------------------------")
            print(UtcNow() + " |             Program, first check and/or make folders. Please wait.            ")
            print(UtcNow() + " | ------------------------------------------------------------------------------")
            startVal = 1
            sleep(1)
        else:
            dataFolder()
            DAYS = ReadDownload()
            SplitDownload(DAYS)
            for i in DAYS:
                Work(i)
    except Exception as e:
        print(UtcNow() + " | " + getattr(e, 'message', repr(e)))
