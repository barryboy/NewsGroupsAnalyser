#!/usr/bin/env python
"""
A class for parsing set of files containig nntp posts
"""
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# A path to the directory containing the files
class Parser:

    def __init__(self, path):
        """
        returns a dictionary of parsed files where key = Message-ID and value = tuple 
        """
        print path
        pass

    def __getFiles(self, path):
        """
        returns a list of files under the path
        """
        pass

    def __parseFile(self, a_file):
        """
        for a given file returns a tuple with Message-ID, author, date, previous post and content
        """
        pass

    def __getHeader(self, message):
        """
        returns a string with the whole header
        """
        pass

    def __getContent(self, message):
        """
        returns a string containing everything from the post except the header
        """
        pass

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



nntp_parser = Parser("~/jakas_sciezka")
