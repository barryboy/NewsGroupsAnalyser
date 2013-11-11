#!/usr/bin/env python2
"""
A class for parsing set of files containig nntp posts
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
dictionary = nntp_parser.getParsedDict()


print 'THREAD\tID\tAUTHOR\tREFERENCES\tTAIL'
for ID in dictionary.keys():
    msg = dictionary.get(ID)
    if 'tag' in msg:
        print str(msg.get('tag')) + '\t',
        print str(msg.get('id')) + '\t',
        print str(msg.get('author')) + '\t',
        print str(msg.get('date')) + '\t',
        print str(msg.get('references')) + '\t',
        print str(msg.get('tail'))
