#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
File: stats.py
Author: Julien Raigneau <julien@tifauve.net>
Date: 2010-01-06 23:20:52 CET
Version: 

Description: Statistiques sur les mouvements
'''

import web
import category,transaction, dbUtils
import datetime
from datetime import date

def getCategoriesStats(dateDebut, dateFin):
    """Récupère les stats pour les catégories // calcule la répartition par catégorie"""
    transactions = transaction.getTransactionsByDate(dateDebut, dateFin)
    categoriesList = category.getAllCategories()
    stats = [{},{}]
    for myTransaction in transactions:
        myCategory = categoriesList[myTransaction["categoryID"]]
        value = int(myTransaction["value"])
        if value > 0:
            n = 1
        else:
            value = 0 - value
            n = 0

        if myCategory in stats[n].keys():
            stats[n][myCategory] = stats[n][myCategory] + 1
        else:
            stats[n][myCategory] = 1
    return stats

def getTransactionsStats(dateDebut, dateFin):
    """Récupère les stats pour les transactions // renvoie la répartition par jours des dépenses et des virements"""
    transactions = transaction.getTransactionsByDate(dateDebut, dateFin)
    stats = [{},{}]
    for myTransaction in transactions:
        dated = myTransaction["dated"]
        value = int(myTransaction["value"])
        if value > 0:
            n = 1
        else:
            value = 0 - value
            n = 0

        if dated in stats[n].keys():
            stats[n][dated] = stats[n][dated] + value
        else:
            stats[n][dated] = value
    return stats

def getTransactionsStatsByWeek(dateDebut, dateFin):
    """Récupère les stats pour les transactions // renvoie la répartition par semaine des dépenses et des virements"""
    transactions = transaction.getTransactionsByDate(dateDebut, dateFin)
    stats = [{},{}]
    for myTransaction in transactions:
        myWeek = datetime.datetime.strptime(myTransaction["dated"],"%Y-%m-%d").strftime("%Y.%W")
        value = int(myTransaction["value"])
        if value > 0:
            n = 1
        else:
            value = 0 - value
            n = 0

        if myWeek in stats[n].keys():
            stats[n][myWeek] = stats[n][myWeek] + value
        else:
            stats[n][myWeek] = value
    return stats

def getTransactionsStatsByMonth(dateDebut,dateFin):
    """Récupère les stats pour les transactions // renvoie la répartition par mois des dépenses et des virements"""
    transactions = transaction.getTransactionsByDate(dateDebut, dateFin)
    stats = [{},{}]
    for myTransaction in transactions:
        myMonth = datetime.datetime.strptime(myTransaction["dated"],"%Y-%m-%d").strftime("%Y.%m")
        value = int(myTransaction["value"])
        if value > 0:
            n = 1
        else:
            value = 0 - value
            n = 0

        if myMonth in stats[n].keys():
            stats[n][myMonth] = stats[n][myMonth] + value
        else:
            stats[n][myMonth] = value
    return stats
