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
    __parsed_dict = {}
    __stats_dict = {}

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
        s = ""
        with file(a_file) as f:
            s = f.read()

        header = self.__getHeader(s)
        content = self.__getContent(s)
        content = self.__clearContent(content)
        ID = self.__getID(header)
        author = self.__getAuthor(header)
        date = self.__getDate(header)
        ref = self.__getLastReference(header)
        subject = self.__getSubject(header)

        result = {}

        result['id'] = ID
        result['author'] = author
        result['date'] = date
        result['references'] = ref
        result['content'] = content
        result['subject'] = subject

        #print result

        return result

    def parse(self):
        """
        the main loop, iterates over __filelist calling __parseFile on each file;
        returns a dictionary, with key = Message-ID and value = dictionary of other fields
        """
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
            ID = parsed.get('id')
            result[ID] = parsed
        sys.stdout.write('\n')
        self.__parsed_dict = result


    def __getHeader(self, message):
        """
        returns the string containig the header
        """
        end = message.find('\n\n')
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
        start = txt.find(startStr)
        if start == -1:
            return ""
        else:
            start += len(startStr)
        end = txt.find(endStr, start)
        return txt[start:end]
   
    def __getID(self, header):
        """
        returns a string with the value of Message-ID field from the header
        """
        return self.__findStr(header, 'Message-ID: <', '>\n')

    def __getSubject(self, header):
        """
        returns a string with the value of Subject field from the header
        """
        return self.__findStr(header, 'Subject: ', '\n')

    def __getLastReference(self, header):
        """
        returns the Message-ID of the imediate predecessor of the post, or an empty string for the root
        """
        ref = self.__findStr(header, 'References: ', '\n')
        if len(ref) < 1:
            ref = 'root'
        else:
            entries = ref.split()
            ref = entries[len(entries) - 1]
            ref = self.__findStr(ref, '<', '>')
        return ref

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

    def getParsedDict(self):
        """
        returns the dict with parsed files
        """
        if len(self.__parsed_dict) < 1:
            sys.exit('Cannot get the dictionary, the dictionary is empty, run parse() first\nSTOPPING.')
        else:
            return self.__parsed_dict


    def populateThreadTags(self):
        """
        run recursively __tagThread() to add 'tag' fields to the dictionary
        """
        dictionary = self.getParsedDict()
        currentTag = 1  
        
        i = 0
        for d in dictionary.keys():
            i += 1
            percent = int((float(i) / self.__file_no) * 100)
            sys.stdout.write('\rTagging roots: ' + str(percent) + '% done.')
            msgDict = dictionary.get(d)
            ref = msgDict.get('references')
            if not ref in dictionary.keys():
                msgDict['references'] = 'root'
                ref = 'root'
            if ref == 'root':
                msgDict['tag'] = currentTag
                currentTag += 1
            else:
                msgDict['tag'] = 0

        sys.stdout.write('\n')

        i = 0
        for d in dictionary.keys():
            i += 1
            percent = int((float(i) / self.__file_no) * 100)
            sys.stdout.write('\rTagging threads: ' + str(percent) + '% done.')
            msgDict = dictionary.get(d)
            self.__tagThread(msgDict)
        sys.stdout.write('\n')


    def __tagThread(self, msgDict):
        tag = msgDict.get('tag')
        if tag == 0:
            dictionary = self.getParsedDict()
            ref = msgDict.get('references')
            path = []
            path.append(msgDict.get('id'))
            newTag = 0
            while newTag == 0:
                newMsg = dictionary.get(ref)
                ref = newMsg.get('references')
                newTag = newMsg.get('tag')
                path.append(newMsg.get('id'))

            for ID in path:
                msg = dictionary.get(ID)
                msg['tag'] = newTag

