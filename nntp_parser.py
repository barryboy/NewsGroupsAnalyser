#!/usr/bin/env python2
'''
A class for parsing set of files containig nntp posts
'''
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os
import sys
import re
from dateutil import parser
import calendar

class Parser:
    
    __file_no = 0
    __filelist = []
    __parsed_dict = {}

    def __init__(self, path):
        '''
        initializes filelist
        '''
        if not os.path.isdir(path):
            sys.exit(path + ' is not a valid directory path')
        
        self.__filelist = self.__getFiles(path)
           

    def __getFiles(self, path):
        '''
        returns a list of files under the path and sets the __file_no variable
        '''
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
        '''
        for a given file returns a dict with Message-ID, author, date, previous post and content
        '''  
        s = ""
        with file(a_file) as f:
            s = f.read()

        header = self.__getHeader(s)
        content = self.__getContent(s)
        content = self.__clearContent(content)
        ID = self.__getID(header)
        author = self.__getAuthor(header)
        date = self.__getDate(header)
        epoch = self.__parseDate(date)
        ref = self.__getLastReference(header)
        subject = self.__getSubject(header)

        result = {}

        result['id'] = ID
        result['author'] = author
        result['date'] = date
        result['epoch_time'] = epoch
        result['references'] = ref
        result['content'] = content
        result['subject'] = subject
        if ref == 'root':
            result['true_root'] = 1
        else:
            result['true_root'] = 0

        return result

    
    def parse(self):
        '''
        the main loop, iterates over __filelist calling __parseFile on each file;
        returns a dictionary, with key = Message-ID and value = dictionary of other fields
        '''
        result = {}
        if self.__file_no < 1:
            sys.stdout.write('\rNothing to parse.\n')
            sys.exit('\rSTOPPING.')
        
        i = 0
        for f in self.__filelist:
            i += 1
            percent = int((float(i) / self.__file_no) * 100)
            sys.stdout.write('\rParsing messages: ' + '\t\t\t\t' + str(percent) + '% done.')
            parsed = self.__parseFile(f)
            ID = parsed.get('id')
            result[ID] = parsed
        sys.stdout.write('\n')
        self.__parsed_dict = result


    def __getHeader(self, message):
        '''
        returns the string containig the header
        '''
        end = message.find('\n\n')
        return message[:end]
            

    def __getContent(self, message):
        '''
        returns a string containing everything from the post except the header
        '''
        start = message.find('\n\n') + 2
        return message[start:]

    def __clearContent(self, content):
        '''
        returns a string with all the lines begining with '>' deleted
        '''
        sig = content.find('-- \n')
        content = content[:sig]
        
        lines = re.split('\n+', content)
        cleared = []
        for l in lines:
            if not '>' in l:
                cleared.append(l)
        content = ' '.join(cleared)
        content = content.replace('\n', ' ')
        content = content.replace('\r', ' ')
        return content

    def __findStr(self, txt, startStr, endStr):
        '''
        returns substring of txt starting with startStr and ending with endStr
        '''
        start = txt.find(startStr)
        if start == -1:
            return ""
        else:
            start += len(startStr)
        end = txt.find(endStr, start)
        return txt[start:end]
   
    def __getID(self, header):
        '''
        returns a string with the value of Message-ID field from the header
        '''
        return self.__findStr(header, 'Message-ID: <', '>\n')

    def __getSubject(self, header):
        '''
        returns a string with the value of Subject field from the header
        '''
        return self.__findStr(header, 'Subject: ', '\n')

    def __getLastReference(self, header):
        '''
        returns the Message-ID of the imediate predecessor of the post, or an empty string for the root
        '''
        ref = self.__findStr(header, 'References: ', '\n')
        if len(ref) < 1:
            ref = 'root'
        else:
            entries = ref.split()
            ref = entries[len(entries) - 1]
            ref = self.__findStr(ref, '<', '>')
        return ref

    def __getDate(self, header):
        '''
        returns the creation date of the post
        '''
        return self.__findStr(header, 'Date: ', '\n')

    def __parseDate(self, date_string):
       '''
       method takes timestaamp string and returns POSIX epoch time
       '''
       parsed = parser.parse(date_string)
       return calendar.timegm(parsed.timetuple())

    def __getAuthor(self, header):
        '''
        returns a string with the author's name
        '''
        return self.__findStr(header, 'From: ', '\n')

    def __getSubject(self, header):
        '''
        returns a string with the subject
        '''
        return self.__findStr(header, 'Subject: ', '\n')

    def getParsedDict(self):
        '''
        returns the dict with parsed files
        '''
        if len(self.__parsed_dict) < 1:
            sys.exit('Cannot get the dictionary, the dictionary is empty, run parse() first\nSTOPPING.')
        else:
            return self.__parsed_dict


    def populateThreadTags(self):
        '''
        run recursively __tagThread() to add 'tag' fields to the dictionary
        '''
        dictionary = self.getParsedDict()
        currentTag = 1  
        
        i = 0
        for d in dictionary.keys():
            i += 1
            percent = int((float(i) / self.__file_no) * 100)
            sys.stdout.write('\rTagging roots: ' +  '\t\t\t\t\t' + str(percent) + '% done.')
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
            sys.stdout.write('\rTagging threads: ' + '\t\t\t\t' + str(percent) + '% done.')
            msgDict = dictionary.get(d)
            self.__tagThread(msgDict)
        sys.stdout.write('\n')


    def __tagThread(self, msgDict):
        '''
        this method assigns distinct numbers to threads and stores it in a field "tag" in each thread
        '''
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


    def anonimizeUsers(self):
        '''
        replaces Message-ID and author ID with numbers
        '''
        dictionary = self.getParsedDict()
        msgID_dict = {'root':'root'}
        authorID_dict = {}
        current_UID = 1
        current_MID = 1

        sys.stdout.write('ANONYMIZING:\n')
        i = 0
        for d in dictionary.keys():
            i += 1
            percent = int((float(i) / self.__file_no) * 100)
            sys.stdout.write('\r\tAssigning new IDs: ' + '\t\t\t' + str(percent) + '% done.')
            msg = dictionary.get(d)
            if d not in msgID_dict:
                msgID_dict[d] = current_MID
                current_MID += 1
            UID = msg.get('author');
            if UID not in authorID_dict:
                authorID_dict[UID] = current_UID
                current_UID += 1
        sys.stdout.write('\n')
        
        i = 0
        new_dict = {}
        for d in dictionary:
            i += 1
            percent = int((float(i) / self.__file_no) * 100)
            sys.stdout.write('\r\tReplacing current IDs: ' + '\t\t\t' + str(percent) + '% done.')
            msg = dictionary.get(d)
            msg['author'] = authorID_dict[msg.get('author')]
            msg['id'] = msgID_dict[msg.get('id')]
            msg['references'] = msgID_dict[msg.get('references')]
            new_dict[msg.get('id')] = msg 
        sys.stdout.write('\n')
        
        
        self.__parsed_dict = new_dict


    def getTail(self):
        '''
        crawls a thread backwards from current message and records its tail of previous authors
        '''
        dictionary = self.getParsedDict()
        i = 0
        for d in dictionary:
            i += 1
            percent = int((float(i) / self.__file_no) * 100)
            sys.stdout.write('\rGetting message tails: ' + '\t\t\t\t' + str(percent) + '% done.')

            tail = []
            message = dictionary.get(d)
            authorID = message.get('author')
            tail.append(authorID)
            ref = message.get('references')
            while ref != 'root':
                currentMsg = dictionary.get(ref)
                authorID = currentMsg.get('author')
                tail.append(authorID)
                ref = currentMsg.get('references')
            message['tail'] = tail

        sys.stdout.write('\n')


    def parseTails(self):
        '''
        for each tail runs parseTail() and stores the result in the massage's dict
        '''
        dictionary = self.getParsedDict()
        i = 0
        for d in dictionary:
            i += 1
            percent = int((float(i) / self.__file_no) * 100)
            sys.stdout.write('\rParsing message tails: ' + '\t\t\t\t' + str(percent) + '% done.')
            message = dictionary.get(d)
            tail =message.get('tail')
            parsedTail = self.__parseTail(tail)
            for field in parsedTail:
                message[field] = parsedTail.get(field)
        sys.stdout.write('\n')



    def __parseTail(self, tail):
        '''
        counts the occurences of each sequence in the tail and stores it in the entry: 'nSEQUENCE'
        it stores also the immediate predecessor sequence of a current message and stores it in the entry: 'SEQUENCE'
        '''
        parsedTail = {'ABA':0, 'ABC':0, 'ABCA':0, 'ABCB':0, 'ABCD':0, 'ABAB':0, 'ABAC':0, 'nABA':0, 'nABC':0, 'nABCA':0, 'nABCB':0, 'nABCD':0, 'nABAB':0, 'nABAC':0, 'tail_length':0}
        l = len(tail)
        parsedTail['tail_length'] = l
        n3 = l - 2 
        if n3 < 0: n3 = 0
        n4 = l - 3
        if n4 < 0: n4 = 0

        for i in range(n3):
            frag = tail[i:i+3]
            if (frag[0] == frag[2]) and (frag[2] != frag[1]):
                if i == 0:
                    parsedTail['ABA'] = 1
                parsedTail['nABA'] += 1
            else:
                if i == 0:
                    parsedTail['ABC'] = 1
                parsedTail['nABC'] += 1

        for i in range(n4):
            frag = tail[i:i+4]
            if (frag[0] != frag[1]) and (frag[1] != frag[2]) and (frag[0] != frag[2]):
                if (frag[3] == frag[0]):
                    if i == 0:
                        parsedTail['ABCA'] = 1
                    parsedTail['nABCA'] += 1
                if (frag[3] == frag[1]):
                    if i == 0:
                        parsedTail['ABCB'] = 1
                    parsedTail['nABCB'] += 1
                if (frag[3] != frag[1]) and (frag[3] != frag[2]) and (frag[3] != frag[2]):
                    if i == 0:
                        parsedTail['ABCD'] = 1
                    parsedTail['nABCD'] += 1
            if (frag[0] == frag[2]) and (frag[2] != frag[1]):
                if (frag[3] == frag[1]):
                    if i == 0:
                        parsedTail['ABAB'] = 1
                    parsedTail['nABAB'] += 1
                if (frag[3] != frag[0]) and (frag[3] != frag[1]):
                    if i == 0:
                        parsedTail['ABAC'] = 1
                    parsedTail['nABAC'] += 1

        return parsedTail

