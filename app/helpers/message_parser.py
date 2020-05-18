#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Rudolf De Geijter
#
#  app/helpers/message_parser.py
#

import lxml.etree as etree


def get_message_root_tag(message):
    root = etree.fromstring(message)
    root_tag = etree.QName(root).localname
    return root_tag
