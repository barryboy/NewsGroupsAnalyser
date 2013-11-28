#!/usr/bin/env python2
'''
A class for preparing Pajek net file. It is initialized with parsed dictionary.
'''
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys

class NetMaker:
    __dict = {}

    def __init__(self, dictionary):
        sys.stdout.write('\n\rSTARTING NET-MAKER')
        i = 0
        n = len(dictionary.keys())
        for d in dictionary.keys():
            i += 1
            percent = int((float(i) / n) * 100)
            sys.stdout.write('\rGetting data from parsed dictionary: ' + '\t\t\t' + str(percent) + '% done.')
            msg = dictionary.get(d)
            from_vert = msg.get('author')
            ref = msg.get('references')
            
            if from_vert in self.__dict.keys():
                author_dict = self.__dict.get(from_vert)
            else:
                author_dict = {}

            if ref != 'root':
                to_msg = dictionary.get(ref)
                to_vert = to_msg.get('author')
                if to_vert in author_dict.keys():
                    author_dict[to_vert] += 1
                else:
                    author_dict[to_vert] = 1
            self.__dict[from_vert] = author_dict
        sys.stdout.write('\n')
        

    def prepareFile(self):
        dictionary = self.__dict
        content = ''
        i = 0
        n = len(dictionary.keys())
        content += '*Vertices ' + str(n) + '\n'
        for v in range(1,n+1):
            content += str(v) + ' \"' + str(v) + '\"\n'
        
        content += '*Arcs\n'

        for d in dictionary.keys():
            i += 1
            percent = int((float(i) / n) * 100)
            sys.stdout.write('\r\tPreparing net file: ' + '\t\t\t' + str(percent) + '% done.')
            vertex = dictionary.get(d)
            if len(vertex) > 0:
                for arc in vertex.keys():
                    content += str(d) + ' ' + str(arc) + ' ' + str(vertex.get(arc)) + '\n'

        sys.stdout.write('\n')
        
        return content

