#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
File: controller.py
Author: Julien Raigneau <julien@tifauve.net>
Date: 2009-12-12 15:29:52 CET
Version: 0.1

Description: controlleur pour Harpagon
'''
#
# Modules import.
import web, model.transaction, model.stats
import webapp,dashboardUtils
from datetime import date,timedelta
import datetime
import time
import calendar
import locale
locale.setlocale(locale.LC_ALL, '')
#
# Views directory definition.
view = web.template.render('views/', base='base')

# RESTful class definition.
class Index:
    """Afficher la Page de Dashboard (premiere page)"""
    def GET(self):
        'Render the index page.'
        tStart = time.time()
        today = date.today()
        firstDayOfMonth = datetime.date(today.year,today.month,1)
        todayMinus30 = today - timedelta(days=30)
        todayMinus100 = today - timedelta(days=100)

        statsOutComesCurrentMonth = model.stats.getTransactionsStats(firstDayOfMonth.isoformat(),today.isoformat())[0]
        statsOutComesAllMonthsButCurrent = model.stats.getTransactionsStatsByMonth("2009-01-01",(firstDayOfMonth - timedelta(days=1)).isoformat())[0]
        thisMonthSum,allMonthsMean,allMonthsProrata = dashboardUtils.monthlyStatsProrata(statsOutComesCurrentMonth,statsOutComesAllMonthsButCurrent,today)
        graphBar = dashboardUtils.makeBarChartStatsURL(thisMonthSum,allMonthsMean,allMonthsProrata)

        graphCategoriesIncomesAll =  dashboardUtils.makePieChartStatsURL(model.stats.getCategoriesStats(todayMinus100.isoformat(),today.isoformat())[1],"p",u"Revenus+par+catégorie|Tous mois confondus")
        graphIncomesAll =  dashboardUtils.makeLineChartStatsURL(model.stats.getTransactionsStatsByMonth("2009-01-01",today.isoformat())[1],"bvs",u"Montant+des+revenus+par+mois|Tous mois confondus")

        graphCategoriesAll =  dashboardUtils.makePieChartStatsURL(model.stats.getCategoriesStats("2009-01-01",today.isoformat())[0],"p",u"Dépenses+par+catégorie|Tous mois confondus")
        graphOutcomesAll =  dashboardUtils.makeLineChartStatsURL(model.stats.getTransactionsStatsByMonth("2009-01-01",today.isoformat())[0],"bvs",u"Montant+des+dépenses+par+mois|Tous mois confondus")
        tEnd = time.time()
        responseTime = "Calcul du dashboard en %ims" % ((tEnd-tStart)*1000)
        return view.index(graphBar,graphCategoriesIncomesAll,graphIncomesAll,graphCategoriesAll,graphOutcomesAll,responseTime)

class Upload:
    """Télécharger le fichier"""
    def GET(self):
        'Render the page.'
        flash={}
        return view.upload(flash)

    def POST(self):
        x = web.input(myfile={})
        if x['myfile'].filename.split(".")[-1] != 'qif':
            flash={"erreur":"Merci de spécifier un fichier avec l'extension .qif"}
            return view.upload(flash)
        else:
            tStart = time.time()
            myTransactions,newTrans,existingTrans=model.transaction.insertTransactions(x['myfile'].file.readlines())
            tEnd = time.time()
            flash={"notice":"%s transactions insérées dans la base, %s transactions déjà existantes en %ims" % (newTrans,existingTrans,((tEnd-tStart)*1000))}
            return view.list(model.transaction.getAllTransactions(),flash)


class Transaction:
    """Gérer les transactions: liste ou mise à jour"""
    def GET(self, transactionID="dated"):
        flash={}
        if transactionID in ("dated","comment","categoryID"):
            orderby = transactionID
            tStart = time.time()
            webapp.session.listOrderBy = orderby
            transactions = model.transaction.getAllTransactions(orderby)
            tEnd = time.time()
            flash={"notice":"La liste a été créée en %ims" % ((tEnd-tStart)*1000)}
            return view.list(transactions,flash)

        myTransaction=model.transaction.getTransaction(transactionID)
        if myTransaction == -1:
            flash={"erreur":"Transaction inexistante!"}
            return view.list(model.transaction.getAllTransactions(webapp.session.listOrderBy),flash)
        else:
            return view.transaction(myTransaction,model.category.getAllCategories(),flash)

    def POST(self,id):
        i = web.input()
        if i._method == "PUT":
            flash = self.PUT(id,i)
            return view.list(model.transaction.getAllTransactions(webapp.session.listOrderBy),flash)

        else:
            web.notfound()

    def PUT(self, id, i):
        if model.transaction.updateTransaction(id,i.comment,i.category) ==-1:
            flash={"erreur":"Impossible de modifier la transaction"}
        else:
            flash={"notice":"La transaction a été modifiée avec succès"}
        return flash


class Category:
    """Gérer les catégories: liste ou mise à jour"""
    def GET(self, categoryID=-1):
        flash={}
        if categoryID == -1:
            return view.new_category(flash)
        else:
            myCategory=model.category.getCategory(categoryID)
            if myCategory == -1:
                flash={"erreur":"Categorie inexistante!"}
                return view.admin(model.category.getAllCategories(),model.searchString.getAllSearchStrings(),flash)
            else:
                return view.category(myCategory,flash)

    def POST(self,id=-1):
        i = web.input()
        if i._method == "PUT":
            flash = self.PUT(id,i)
        elif i._method == "DELETE":
            flash = self.DELETE(id,i)
        else:#un post normal pour créer la categorie !
            if model.category.addCategory(i.category) ==-1:
                flash={"erreur":"Impossible de créer la catégorie"}
            else:
                flash={"notice":"La catégorie a été créée avec succès"} 
        return view.admin(model.category.getAllCategories(),model.searchString.getAllSearchStrings(),flash)

    def PUT(self, id, i):
        if model.category.updateCategory(id,i.category) ==-1:
            flash={"erreur":"Impossible de modifier la catégorie"}
        else:
            flash={"notice":"La catégorie a été modifiée avec succès"}
        return flash
   
    def DELETE(self,id,i):
        if model.category.deleteCategory(id) == -1:
            flash={"erreur":"Impossible de supprimer la catégorie"}
        else:
            flash={"notice":"La catégorie a été supprimée avec succès"}
        return flash

class Rule:
    """Gérer les règles: liste/création ou mise à jour"""
    def GET(self, searchStringID=-1):
        flash={}
        if searchStringID == -1:
            return view.new_rule(model.category.getAllCategories(),flash)
        else:
            myRule=model.searchString.getSearchString(searchStringID)
            if myRule == -1:
                flash={"erreur1":"Règle inexistante!"}
                return view.admin(model.category.getAllCategories(),model.searchString.getAllSearchStrings(),flash)
            else:
                return view.rule(myRule,model.category.getAllCategories(),flash)

    def POST(self,id=-1):
        i = web.input()
        if i._method == "PUT":
            flash = self.PUT(id,i)
        elif i._method == "DELETE":
            flash = self.DELETE(id,i)
        else:#un post normal pour créer la règle !
            if model.searchString.addSearchString(i.searchString,i.category) ==-1:
                flash={"erreur1":"Impossible de créer la règle"}
            else:
                flash={"notice1":"La règle a été créée avec succès"}
        return view.admin(model.category.getAllCategories(),model.searchString.getAllSearchStrings(),flash)

    def PUT(self, id, i):
        print i
        if model.searchString.updateSearchString(id,i.searchString,i.category) ==-1:
            flash={"erreur1":"Impossible de modifier la règle"}
        else:
            flash={"notice1":"La régle a été modifiée avec succès"}
        return flash
   
    def DELETE(self,id,i):
        if model.searchString.deleteSearchString(id) == -1:
            flash={"erreur1":"Impossible de supprimer la règle"}
        else:
            flash={"notice1":"La règle a été supprimée avec succès"}
        return flash

class Rules:
    """Permet de rejouer les règles"""
    def GET(self):
        flash={}
        tStart = time.time()
        if model.searchString.commitRules():
            tEnd = time.time()
            flash = {"notice1":"Mise à jour des règles avec succès en %ims" % ((tEnd-tStart)*1000)}
        return view.admin(model.category.getAllCategories(),model.searchString.getAllSearchStrings(),flash)

class Admin:
    """Administrer les catégories"""
    def GET(self):
        flash={}
        return view.admin(model.category.getAllCategories(),model.searchString.getAllSearchStrings(),flash)
