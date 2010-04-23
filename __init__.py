#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
File: __init__.py
Author: Julien Raigneau <julien@tifauve.net>
Date: 2009-12-12 15:26:47 CET
Version: 0.1

Description: Harpagon - outil comptable simplifié
'''

import app.webapp


# App execution.
if __name__ == '__main__':
    app = app.webapp.runApp()
    app.run()
