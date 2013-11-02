#!/usr/bin/env python
"""
A class for parsing set of files containig nntp posts
"""
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os
import sys

class Parser:
    
    __filelist = []
    __file_no = 0

    def __init__(self, path):
        """
        initializes filelist
        """
        if not os.path.isdir(path):
            sys.exit(path + ' is not a valid directory path')
        f = self.__getFiles(path)
        self.__file_no = len(f)
        self.__filelist = f
        
        with file(f[10]) as msg:
            s = msg.read()
            print self.__getContent(s)
           

    def __getFiles(self, path):
        """
        returns a list of files under the path
        """
        result = []
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                if f.endswith('.msg'):
                    result.append(os.path.join(dirpath, f))
        return result

    def __countFiles(self, filelist):
        """
        returns an integer reperesenting the total number of files
        """
        pass

    def __parseFile(self, a_file):
        """
        for a given file returns a tuple with Message-ID, author, date, previous post and content
        """
        header = self.__getHeader(a_file)
        content = self.__getContent(a_file)
        content = sefl.__clearCitations(content)
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

    def __clearCitations(self, content):
        """
        returns a string with all the lines begining with '>' deleted
        """
        pass

    def __getID(self, header):
        """
        returns a string with the value of Message-ID field from the header
        """
        pass

    def __getLastReference(self, header):
        """
        returns the Message-ID of the imediate predecessor of the post, or an empty string for the root
        """
        pass

    def __getDate(self, header):
        """
        returns the creation date of the post
        """
        pass

    def __getAuthor(self, header):
        """
        returns a string with the author's name
        """
    pass



nntp_parser = Parser(sys.argv[1])
