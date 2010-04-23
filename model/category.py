#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
File: category.py
Author: Julien Raigneau <julien@tifauve.net>
Date: 2009-12-31 20:02:32 CET
Version: 

Description: modele pour les categories
'''

import web
import dbUtils

def getAllCategories():
    """Retourne toutes les catégories existantes dans la base"""
    db = dbUtils.createConnexion()
    allCategories = db.select('categories',order="category")
    categories = {}
    for category in allCategories:
        categories[category["id"]]=category["category"]
    return categories

def getCategory(categoryID):
    """Retourne la catégorie categoryID ou -1 si non existante"""
    db = dbUtils.createConnexion()
    myvar = {"id":categoryID}
    checkExisting = db.select('categories',myvar, where="id=$id")
    try:
        return checkExisting[0]
    except IndexError:
        return -1

def updateCategory(categoryID,category):
    """Met à jour la catégorie dans la base"""
    db = dbUtils.createConnexion()
    try:
        db.query("UPDATE categories SET category=$category WHERE id=$id", vars=dict(category=category, id=categoryID))
        return True
    except IndexError:
        print "La Categorie %s est introuvable!" % categoryID
        return False

def deleteCategory(categoryID):
    """Supprime la catégorie dans la base en mettant par défaut les transactions à l'ID=1"""
    db = dbUtils.createConnexion()
    try:
        db.query("UPDATE transactions SET categoryID=1 WHERE categoryID=$id", vars=dict(id=categoryID))
        db.query("UPDATE searchStrings SET categoryID=1 WHERE categoryID=$id", vars=dict(id=categoryID))
        db.query("DELETE FROM categories WHERE id=$id", vars=dict(id=categoryID))
        return True
    except IndexError:
        print "La Categorie %s est introuvable!" % categoryID
        return False

def addCategory(category):
    """Ajouter une nouvelle catégorie"""
    try:
        db = dbUtils.createConnexion()
        db.insert('categories', category=category)
        return 0
    except IndexError:
        return -1

