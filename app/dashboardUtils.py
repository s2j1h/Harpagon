#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
File: dashboardUtils.py
Author: Julien Raigneau <julien@tifauve.net>
Date: 2010-02-27 15:24:38 CET
Description:Quelques utilitaires pour le dashboard
'''
import datetime
from datetime import date,timedelta
import calendar

def makePieChartStatsURL(stats,cht,chtt):
    """Crée l'url pour l'API Google Chart -- Camenbert"""
    chd =""
    chl=""
    statsList = stats.items() #permet de faire des tris
    statsList.sort(key=lambda x: x[1],reverse=True)

    for stat,value in statsList:
        if chd =="":
            chd = "%s" % stats[stat]
            chl = stat
        else:
            chd = chd + ",%s" % stats[stat]
            chl = chl+"|"+stat
    graph = "chs=600x350&chd=t:%s&cht=%s&chdl=%s&chtt=%s&chf=bg,s,EEEEEE&chco=ff3d00,b8FF00,00ffab,007dff,FF9900" % (chd,cht,chl,chtt)
    return graph

def makeLineChartStatsURL(stats,cht,chtt):
    """Crée l'url pour l'API Google Chart -- Simple ligne"""
    chd =""
    chl=""
    maxValue = 0
    statsList = stats.keys()
    statsList.sort()
    oldKeyX2 = "0"
    for stat in statsList:
        if stat.find("-") > -1: #gérer les dates "YY-MM-DD" ou y.xxx
            key = datetime.datetime.strptime(stat,"%Y-%m-%d").strftime("%d-%B")
            keyX = key[0:2] #premiere ligne
            keyX2 = key[3:] #deuxieme ligne: mois / année
        elif stat.find(".") > -1:
            keyX = stat[5:]
            keyX2 = stat[0:4]
        else:
            keyX = stat
        
        #seconde ligne X 
        if oldKeyX2 == keyX2:
            keyX2 = " "
        else:
            oldKeyX2 = keyX2

        if chd =="":
            chd = u"%s" % stats[stat]
            chl = "0:|" + keyX
            chl2 = "|2:|" + keyX2
            maxValue = stats[stat]
        else:
            chd = chd + u",%s" % stats[stat]
            chl = chl+"|"+keyX
            chl2 = chl2+"|"+keyX2
            if stats[stat] > maxValue:
                maxValue = stats[stat]
    chl = "%s%s" % (chl,chl2) #on concatene les X
    if cht == "bvs":
         graph = u"chs=600x350&chd=t:%s&cht=%s&chxl=%s&chtt=%s&chbh=a&chds=0,%s&chxt=x,y,x&chxr=1,0,%s&chf=bg,s,EEEEEE" % (chd,cht,chl.decode("utf-8"),chtt,maxValue,maxValue)
    else:
        graph = u"chs=600x350&chd=t:%s&cht=%s&chxl=%s&chtt=%s&chm=B,F7C478,0,0,0&chds=0,%s&chxt=x,y,x&chxr=1,0,%s&chf=bg,s,EEEEEE" % (chd,cht,chl.decode("utf-8"),chtt,maxValue,maxValue)
    return graph

def makeBarChartStatsURL(thisMonthSum,allMonthsMean,allMonthsProrata):
    """Crée l'url pour l'API -- barres"""
    return u"cht=bhs&chco=0000FF&chs=600x350&chd=t:%s,%s,%s&chxt=y&chxl=0:|Moy.+total+Mois|Moy.+au+prorata|Dépenses&chm=r,EEEEEE,0,-0.01,0.01,1|R,EEEEEE,0,1.01,0.96,1&chf=bg,s,EEEEEE&chds=0,6000&chbh=a&chco=ff3d00|b8FF00|00A5C6&chem=y;s=bubble_icon_text_small;d=euro,bbT,%s,ff3d00,000;ds=0;dp=0;py=1;of=-40,-10|y;s=bubble_icon_text_small;d=euro,bbT,%s,b8FF00,000;ds=0;dp=1;py=1;of=-40,-10|y;s=bubble_icon_text_small;d=euro,bbT,%s,00A5C6,000;ds=0;dp=2;py=1;of=-50,-10" % (thisMonthSum,allMonthsProrata,allMonthsMean,thisMonthSum,allMonthsProrata,allMonthsMean)


def monthlyStatsProrata(thisMonth,allMonths,today):
    """Renvoie la somme des dépenses du mois courant, la moyenn des mois passés et la moyenne des mois passés au prorata du nombre de jour du mois courant"""
    nbDays = today.day
    nbDaysInMonth = calendar.mdays[today.month]
    thisMonthSum = computeStats(thisMonth)
    allMonthsMean = computeStats(allMonths) / len(allMonths)
    allMonthsProrata = int(allMonthsMean * float(nbDays)/nbDaysInMonth)
    return thisMonthSum,allMonthsMean,allMonthsProrata

def computeStats(stats):
    """Renvoie la somme des montants des transactions du tableau stats donné en entrée, que cela soit des jours, semaines ou mois"""
    sum = 0
    statsList = stats.keys()
    statsList.sort()
    for stat in statsList:
        if stat.find("-") > -1: #gérer les dates "YY-MM-DD" ou y.xxx
            key = datetime.datetime.strptime(stat,"%Y-%m-%d").strftime("%d-%B")
            keyX = key[0:2] #premiere ligne
        elif stat.find(".") > -1:
            keyX = stat[5:]
        else:
            keyX = stat

        sum = sum + stats[stat]
    return sum

