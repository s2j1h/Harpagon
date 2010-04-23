#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
File: dbUtils.py
Author: Julien Raigneau <julien@tifauve.net>
Date: 2009-12-31 20:04:44 CET
Version: 

Description: Gére la base de donnée
'''
import web


def createConnexion():
    return web.database(dbn='sqlite', db='harpagon.db')
