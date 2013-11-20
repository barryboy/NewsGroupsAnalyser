#!/usr/bin/env python2
"""
A runner for Parser class from nntp_parser.py
"""
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import nntp_parser 
import sys

largv = len(sys.argv)

if largv < 2:
    sys.exit('No argument given.\nSTOPPING.\n')
infile = sys.argv[1]
splitted = infile.split('/') 
outfile = splitted[len(splitted)-1] + '.csv'
outfile2 = splitted[len(splitted)-1] + '_content'

nntp_parser= nntp_parser.Parser(infile)
nntp_parser.parse()
nntp_parser.populateThreadTags()
nntp_parser.anonimizeUsers()
nntp_parser.getTail()
nntp_parser.parseTails()
dictionary = nntp_parser.getParsedDict()

f = open(outfile, 'w')
line_count = 0
file_count = 0
current_outfile = outfile2 + '_' + str(file_count) + '.csv'
f2 = open(current_outfile, 'w')

f.write('THREAD\tID\tTRUE_ROOT\tAUTHOR\tREFERENCES\tDATE\tEPOCH\ttail_length\tABA\tABC\tABAB\tABAC\tABCA\tABCB\tABCD\tnABA\tnABC\tnABAB\tnABAC\tnABCA\tnABCB\tnABCD\tTAIL\tSUBJECT\n')
for ID in dictionary.keys():
    msg = dictionary.get(ID)
    line = ''
    line += str(msg.get('tag')) + '\t'
    line += str(msg.get('id')) + '\t'
    line += str(msg.get('true_root')) + '\t'
    line += str(msg.get('author')) + '\t'
    line += str(msg.get('references')) + '\t'
    line += str(msg.get('date')) + '\t'
    line += str(msg.get('epoch_time')) + '\t'
    line += str(msg.get('tail_length')) + '\t'
    line += str(msg.get('ABA')) + '\t'
    line += str(msg.get('ABC')) + '\t'
    line += str(msg.get('ABAB')) + '\t'
    line += str(msg.get('ABAC')) + '\t'
    line += str(msg.get('ABCA')) + '\t'
    line += str(msg.get('ABCB')) + '\t'
    line += str(msg.get('ABCD')) + '\t'
    line += str(msg.get('nABA')) + '\t'
    line += str(msg.get('nABC')) + '\t'
    line += str(msg.get('nABAB')) + '\t'
    line += str(msg.get('nABAC')) + '\t'
    line += str(msg.get('nABCA')) + '\t'
    line += str(msg.get('nABCB')) + '\t'
    line += str(msg.get('nABCD')) + '\t'
    line += str(msg.get('tail')) + '\t'
    line += str(msg.get('subject'))
    f.write(line + '\n')
    line_count += 1
    if line_count > 10000:
        file_count += 1
        current_outfile = outfile2 + '_' + str(file_count) + '.csv'
        line_count = 0
        f2.close()
        f2 = open(current_outfile, 'w')

    f2.write('[' + str(msg.get('id')) + '] '  + str(msg.get('content')) + '\n')

f.close()
f2.close()
