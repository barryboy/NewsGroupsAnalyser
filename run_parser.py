#!/usr/bin/env python
"""
A class for parsing set of files containig nntp posts
"""
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import nntp_parser 
import sys

nntp_parser= nntp_parser.Parser(sys.argv[1])
nntp_parser.parse()
dictionary = nntp_parser.getParsedDict()
for ID in dictionary.keys():
    msg = dictionary.get(ID)
    print ID,
    print msg.get('author') + '\n'
