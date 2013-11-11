#!/usr/bin/env python2
"""
A runner for Parser class from nntp_parser.py
"""
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import nntp_parser 
import sys

if len(sys.argv) < 2:
    sys.exit('No argument given.\nSTOPPING.\n')

nntp_parser= nntp_parser.Parser(sys.argv[1])
nntp_parser.parse()
nntp_parser.populateThreadTags()
nntp_parser.anonimizeUsers()
nntp_parser.getTail()
nntp_parser.parseTails()
dictionary = nntp_parser.getParsedDict()


print 'THREAD\tID\tAUTHOR\tREF\tABA\tABC\tABAB\tABAC\tABCA\tABCB\tABCD\tTAIL'
for ID in dictionary.keys():
    msg = dictionary.get(ID)
    if 'tag' in msg:
        print str(msg.get('tag')) + '\t',
        print str(msg.get('id')) + '\t',
        print str(msg.get('author')) + '\t',
        #print str(msg.get('date')) + '\t',
        print str(msg.get('references')) + '\t',
        print str(msg.get('ABA')) + '\t',
        print str(msg.get('ABC')) + '\t',
        print str(msg.get('ABAB')) + '\t',
        print str(msg.get('ABAC')) + '\t',
        print str(msg.get('ABCA')) + '\t',
        print str(msg.get('ABCB')) + '\t',
        print str(msg.get('ABCD')) + '\t',
        print str(msg.get('tail'))
