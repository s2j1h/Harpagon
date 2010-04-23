#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
File: webapp.py
Author: Julien Raigneau <julien@tifauve.net>
Date: 2009-12-12 15:26:47 CET
Version: 0.1

Description: Harpagon - outil comptable simplifié
'''

#
# Modules import.
import web, controller
import sqlite3
#
# App definition, via URL to class mapping.
def runApp():

    web.config.debug = True

    urls = (
    '/', 'app.controller.Index',
    '/upload','app.controller.Upload', #Gére l'upload d'une liste de transacition GET + POST
    '/transaction/(\d+)/edit','app.controller.Transaction',  #Affiche la transaction pour modification (GET)
    '/transaction/(\d+)/put','app.controller.Transaction', #Modifie la transaction (POST / PUT émulé)
    '/transaction','app.controller.Transaction', #Affiche la liste des transactions (GET)
    '/transaction/sortby/([a-zA-Z]*)','app.controller.Transaction', #Lister la liste des transactions (GET) classé
    '/admin','app.controller.Admin', #Affiche les categories + regles de modif (GET)
    '/category/(\d+)/edit','app.controller.Category', #Affiche une categorie pour édition (GET)
    '/category/(\d+)/put','app.controller.Category', #Modifie une categorie via POST/PUT
    '/category/(\d+)/delete','app.controller.Category', #supprime une categorie via delete (DELETE)
    '/category/new','app.controller.Category', #Affiche une categorie pour création (GET)
    '/category','app.controller.Category', #Ajoute une categorie (POST)
    '/rule/(\d+)/edit','app.controller.Rule', #Affiche une règle pour édition (GET)
    '/rule/(\d+)/put','app.controller.Rule', #Modifie une règle via POST/PUT
    '/rule/(\d+)/delete','app.controller.Rule', #supprime une règle via delete (DELETE)
    '/rule/new','app.controller.Rule', #Affiche une règle pour création (GET)
    '/rule','app.controller.Rule', #Ajoute une règle (POST)
    '/rule/commit','app.controller.Rules' #rejoue les règles
    )

    # App execution.
    webApp = web.application(urls, globals())
    global session
    session = web.session.Session(webApp, web.session.DiskStore('sessions'),initializer = {'listSortedBy': 'dated'}) #utiliser pour la config temporaire de l'utilisateur
    return webApp
