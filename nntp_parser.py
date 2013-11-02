#!/usr/bin/env python
"""
A class for parsing set of files containig nntp posts
"""
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os
import sys
import re

class Parser:
    
    __file_no = 0
    __filelist = []

    def __init__(self, path):
        """
        initializes filelist
        """
        if not os.path.isdir(path):
            sys.exit(path + ' is not a valid directory path')
        
        self.__filelist = self.__getFiles(path)
           

    def __getFiles(self, path):
        """
        returns a list of files under the path and sets the __file_no variable
        """
        result = []
        i = 0
        sys.stdout.write('\rProcessing files in ' + path + '\n')
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                if f.endswith('.msg'):
                    i += 1
                    result.append(os.path.join(dirpath, f))
                    sys.stdout.write('\rRead ' + str(i) + ' files')
                    sys.stdout.flush()
        self.__file_no = len(result)
        sys.stdout.write('\n')
                
        return result


    def __parseFile(self, a_file):
        """
        for a given file returns a dict with Message-ID, author, date, previous post and content
        """        
        header = self.__getHeader(a_file)
        content = self.__getContent(a_file)
        content = self.__clearContent(content)
        ID = self.__getID(header)
        author = self.__getAuthor(header)
        date = self.__getDate(header)
        ref = self.__getLastReference(header)

        result = {}

        result['id'] = ID
        result['author'] = author
        result['date'] = date
        result['references'] = ref
        result['content'] = content
        return result

    def parse(self):
        result = {}
        if self.__file_no < 1:
            sys.stdout.write('\rNothing to parse.\n')
            sys.exit('\rSTOPPING.')
        
        i = 0
        for f in self.__filelist:
            i += 1
            percent = int((float(i) / self.__file_no) * 100)
            sys.stdout.write('\rParsing: ' + str(percent) + '% done.')
            parsed = self.__parseFile(f)
            ID = parsed.pop('id')
            result[ID] = parsed
        sys.stdout.write('\n')

        return result


    def __getHeader(self, message):
        """
        returns the string containig the header
        """
        end = message.find('\n'+ "" + '\n')
        return message[:end]
            

    def __getContent(self, message):
        """
        returns a string containing everything from the post except the header
        """
        start = message.find('\n\n') + 2
        return message[start:]

    def __clearContent(self, content):
        """
        returns a string with all the lines begining with '>' deleted
        """
        sig = content.find('-- \n')
        content = content[:sig]
        
        lines = re.split('\n+', content)
        cleared = []
        for l in lines:
            if not '>' in l:
                cleared.append(l)
        content = '\n'.join(cleared)

        return content

    def __findStr(self, txt, startStr, endStr):
        """
        returns substring of txt starting with startStr and ending with endStr
        """
        start = txt.find(startStr) + len(startStr)
        end = txt.find(endStr, start)

        return txt[start:end]
    
    def __getID(self, header):
        """
        returns a string with the value of Message-ID field from the header
        """
        return self.__findStr(header, 'Message-ID: <', '>\n')

    def __getLastReference(self, header):
        """
        returns the Message-ID of the imediate predecessor of the post, or an empty string for the root
        """
        return self.__findStr(header, 'References: ', '\n')

    def __getDate(self, header):
        """
        returns the creation date of the post
        """
        return self.__findStr(header, 'Date: ', '\n')

    def __getAuthor(self, header):
        """
        returns a string with the author's name
        """
        return self.__findStr(header, 'From: ', '\n')

    def __getSubject(self, header):
        """
        returns a string with the subject
        """
        return self.__findStr(header, 'Subject: ', '\n')


nntp_parser = Parser(sys.argv[1])
dictionary = nntp_parser.parse()
