#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
File: transactions.py
Author: Julien Raigneau <julien@tifauve.net>
Date: 2009-12-16 20:42:30 CET
Version: 

Description: modele pour les transactions
'''

import web
import category,dbUtils,searchString


def getAllTransactions(orderby="dated"):
    """Retourne tous les transactions présentes dans la base"""
    db = dbUtils.createConnexion()
    if orderby == "dated":
        orderby = "dated DESC"
    else:
         orderby = orderby + " ASC"
    allTransactions = db.select('transactions',order=orderby)

    categoriesList = category.getAllCategories()
    transactions = []
    for transaction in allTransactions:
        myCategory = categoriesList[transaction["categoryID"]]
        transaction["category"]=myCategory
        transactions.append(transaction)
    return transactions

def insertTransactions(fichier):
    """Insère une transaction dans la base"""
    transactions = []
    db = dbUtils.createConnexion()
    searchStrings = searchString.getAllSearchStrings()
    newTrans, existingTrans = 0,0
    #transformation liste pour enlever \n et champs non nécessaires
    newLines = []
    for element in fichier:
        if element in ['\n','^\n','!Type:Bank\n']:
            pass
        else:
            newLines.append(element.decode('iso-8859-1'))

    #boucle sur les lines par groupe de 4
    for i in range(0,len(newLines)-1,4):
        #date: on enleve premier caractère + retour chariot
        dated = newLines[i][1:].replace("\n","").strip()
        dated = "20"+dated[6:] + "-" + dated[3:5] + "-" + dated[0:2]
        #valeur de la transaction
        value = newLines[i+1][1:].replace("\n","").strip()

        #ref de la transaction
        ref1 = newLines[i+2][1:].replace("\n","").strip()

        #traitement des commentaires
        #TODO:penser à rajouter un test sur les index
        comment = newLines[i+3][1:].replace("\n","").strip()
        indexC = comment.find("CONTREVALEUR EN FRANCS      ")
        typeTrans = comment[:indexC]   #type de transaction
        comment = comment[indexC+28:].partition(" ")[2] #commentaire
        if indexC > 0:
            indexC2 = comment.find(" LE ")
            comment = comment[:indexC2].strip()
        if comment == '':
            comment = typeTrans
        comment = comment[:49] #on coupe à 49 caractères


        categoryID=1
        transaction = {"dated":dated,"ref1":ref1,"value":value,"comment":comment, "categoryID":categoryID}
        transaction = searchString.autoCategorize(transaction,searchStrings)
        transactions.append(transaction)
        myvar = {"ref1":ref1,"dated":dated, "value":value, "comment":comment}
        try:#si cela existe déjà alors on ne l'écrit pas dans la base
            checkExisting = db.select('transactions',myvar, where="ref1=$ref1 and dated=$dated and value=$value and comment=$comment")
            if checkExisting[0] != "neant":
                print u"Transaction %s du %s existante" % (ref1,dated)
                existingTrans = existingTrans + 1
        except IndexError:
            db.insert('transactions', dated=transaction["dated"],ref1=transaction["ref1"],value=transaction["value"], comment=transaction["comment"], categoryID=transaction["categoryID"])
            newTrans = newTrans + 1
    return transactions,newTrans,existingTrans


def getTransaction(transactionID):
    """Récupère une transaction dans la base"""
    db = dbUtils.createConnexion()
    myvar = {"id":transactionID}
    checkExisting = db.select('transactions',myvar, where="id=$id")
    try:
        transaction = checkExisting[0]
        categoryID = transaction["categoryID"]
        transaction["category"] = category.getCategory(categoryID)["category"]
        return transaction
    except IndexError:
        print "Transaction %s est introuvable!" % transactionID
        return -1

def updateTransaction(transactionID,comment,categoryID,db=0):
    """Met à jour une transaction dans la base"""
    if db == 0:
        db = dbUtils.createConnexion()
    myvars = {"id":transactionID,"comment":comment,"categoryID":categoryID}
    try:
        db.query("UPDATE transactions SET comment=$comment,categoryID=$categoryID WHERE id=$id", vars=dict(comment=comment,categoryID=categoryID, id=transactionID))
        return True
    except IndexError:
        print "Transaction %s est introuvable!" % transactionID
        return False

def getTransactionsByDate(dateDebut,dateFin):
    """Retourne toutes les transactione entre dateDebut et dateFin"""
    db = dbUtils.createConnexion()
    myvar = {"dateDebut":dateDebut,"dateFin":dateFin}
    transactions = db.select('transactions',myvar, where="dated between $dateDebut and $dateFin")
    return transactions
