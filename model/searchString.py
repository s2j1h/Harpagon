#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
File: searchString.py
Author: Julien Raigneau <julien@tifauve.net>
Date: 2009-12-31 20:02:32 CET
Version: 

Description: modele pour les règles
'''

import web
import dbUtils
import category
import transaction

def getAllSearchStrings():
    """Retourne tous les cas de catégorisation automatique"""
    db = dbUtils.createConnexion()
    allSearchStrings = db.select('searchStrings')
    searchStrings = {}
    for mySearch in allSearchStrings:
        searchString = {}
        searchString["id"]=mySearch["id"]
        searchString["searchString"]=mySearch["searchString"]
        searchString["categoryID"]=mySearch["categoryID"]
        searchString["category"]=category.getCategory(int(searchString["categoryID"]))["category"]
        searchStrings[searchString["id"]]=searchString
    return searchStrings

def autoCategorize(transaction,searchStrings):
    """Effectue l'autocatégorisation sur transaction et le renvoie modifié"""
    for searchStringID in searchStrings.keys():
        searchString = searchStrings[searchStringID]["searchString"]
        if transaction["comment"].find(searchString) > -1:
           transaction["categoryID"] = searchStrings[searchStringID]["categoryID"]
    return transaction

def commitRules():
    """Rejoue toutes les règles"""
    db = dbUtils.createConnexion()
    transactions = transaction.getAllTransactions()
    searchStrings = getAllSearchStrings()
    for myTransaction in transactions:
        categoryID = myTransaction["categoryID"]
        autoCategorize(myTransaction,searchStrings)
        if myTransaction["categoryID"] != categoryID:
            transaction.updateTransaction(myTransaction["id"],myTransaction["comment"],myTransaction["categoryID"],db)
    return True


def getSearchString(searchStringID):
    """Récupère une règle dans la base"""
    db = dbUtils.createConnexion()
    myvar = {"id":searchStringID}
    checkExisting = db.select('searchstrings',myvar, where="id=$id")
    try:
        searchString = checkExisting[0]
        categoryID = searchString["categoryID"]
        searchString["category"] = category.getCategory(categoryID)["category"]
        return searchString
    except IndexError:
        print "Règle %s est introuvable!" % searchStringID
        return -1

def updateSearchString(searchStringID,searchString,categoryID):
    """Met à jour une règle dans la base"""
    db = dbUtils.createConnexion()
    try:
        db.query("UPDATE searchstrings SET searchString=$searchString,categoryID=$categoryID WHERE id=$id", vars=dict(searchString=searchString,categoryID=categoryID, id=searchStringID))
        return True
    except IndexError:
        print "Règle %s est introuvable!" % transactionID
        return False

def deleteSearchString(searchStringID):
    """Supprime la règle dans la base en mettant par défaut les transactions à l'ID=1"""
    db = dbUtils.createConnexion()
    try:
        db.query("DELETE FROM searchstrings WHERE id=$id", vars=dict(id=searchStringID))
        return True
    except IndexError:
        print "La régle %s est introuvable!" % categoryID
        return False


def addSearchString(searchString,categoryID):
    """Ajouter une nouvelle règle"""
    try:
        db = dbUtils.createConnexion()
        db.insert('searchstrings', categoryID=categoryID, searchString=searchString)
        return 0
    except IndexError:
        return -1
