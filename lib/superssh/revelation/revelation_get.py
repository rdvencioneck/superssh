#!/usr/bin/python
#-*- coding: utf-8 -*-

from revelation.datahandler import detect_handler
from revelation.io import DataFile
import getpass
import sys

class RevelationGet(object):

    # Reads a given file and returns its contents.  Parameter: the file
    def read_file(self, thefile):

        flow = open(thefile)
        data = flow.read()
        flow.close()
        return data

    # Decrypts the revelation data and returns the passwords
    def decrypt_revelation_file(self, thedata):

        pwd = getpass.getpass()
        handler = detect_handler(thedata)
        dafi = DataFile(handler)
        thepasswords = dafi.load(self.revelationfile, password=pwd)
        return thepasswords

    def main(self):

        self.revelationfile = sys.argv[1]
        self.path = sys.argv[2]
        try:
            self.revelationdata = self.read_file(self.revelationfile)
            self.passwords = self.decrypt_revelation_file(self.revelationdata)
        except IOError:
            print "File not found"
            sys.exit(1)
        except Exception, e:
            print "Wrong password"
            sys.exit(2)

        splt = self.path.split("/")
        options = []
        cont = 0
        itera = self.passwords.get_iter_first()
        while cont < len(splt):
            entry = self.passwords.get_value(itera, 2)
            if entry.name == splt[cont] and entry.typename != 'Folder':
                for fields in entry.fields:
                    if fields.name == "Password":
                        asx = "%s%s" %(" "*abs(len(fields.name) - 15), fields)
                        print asx.strip()
                        break
                break
            if entry.name == splt[cont] and entry.typename == 'Folder':
                cont = cont + 1
                itera = self.passwords.iter_children(itera)
            else:
                itera = self.passwords.iter_next(itera)

if __name__ == "__main__":
    RevelationGet().main()
