#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Rudolf De Geijter
#
#  main.py
#

from app.app import EventListener

if __name__ == "__main__":
    eventListener = EventListener()
    eventListener.start()
