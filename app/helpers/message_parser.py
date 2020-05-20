#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Rudolf De Geijter
#
#  app/helpers/message_parser.py
#

import lxml.etree as etree


def get_message_root_tag(message):
    try:
        root = etree.fromstring(message)
    except etree.XMLSyntaxError as syntaxError:
        raise syntaxError

    # We need the root tag without any namespaces.
    root_tag = etree.QName(root).localname

    return root_tag
