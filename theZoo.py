#!/usr/bin/env python

    #Malware DB - the most awesome free malware database on the air
    #Copyright (C) 2014, Yuval Nativ, Lahad Ludar, 5Fingers

    #This program is free software: you can redistribute it and/or modify
    #it under the terms of the GNU General Public License as published by
    #the Free Software Foundation, either version 3 of the License, or
    #(at your option) any later version.

    #This program is distributed in the hope that it will be useful,
    #but WITHOUT ANY WARRANTY; without even the implied warranty of
    #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #GNU General Public License for more details.

    #You should have received a copy of the GNU General Public License
    #along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import csv
import os
from optparse import OptionParser
from imports.updatehandler import Updater
from imports import muchmuchstrings
from imports.eula_handler import EULA
from imports.globals import vars
from imports.terminal_handler import Controller

__version__ = "0.5.0 Citadel"
__codename__ = "Citadel"
__appname__ = "theZoo"
__authors__ = ["Yuval Nativ", "Lahad Ludar", "5Fingers"]
__licensev__ = "GPL v3.0"
__maintainer = "Yuval Nativ"
__status__ = "Beta"


def main():

    # Much much imports :)
    updateHandler = Updater
    eulaHandler = EULA()
    bannerHandler = muchmuchstrings.banners()
    terminalHandler = Controller()

    def filter_array(array, colum, value):
        ret_array = [row for row in array if value in row[colum]]
        return ret_array

    def getArgvs():
        parser = OptionParser()
        parser = OptionParser()
        parser.add_option("-t", "--type", dest="type_of_mal", default='', help="Type of malware to search. \ne.g. botnet,trojan,virus,etc...")
        parser.add_option("-l", "--language", dest="lang_of_mal", default='', help="Language of the version of the malware which is in the databse.\e.g. vbs,vb,c,cpp,bin,etc...")
        parser.add_option("-a", "--architecture", dest="arch_of_mal", default='', help="The architecture the malware is intended for.\ne.g. x86,x64,arm7,etc...")
        parser.add_option("-p", "--platform", dest="plat_of_mal", default="", help="Platform the malware is inteded for.\ne.g. win32,win64,ios,android,etc...")
        parser.add_option("-u", "--update", dest="update_bol", default=0, help="Updates the DB of theZoo.", action="store_true")
        parser.add_option("-v", "--version" , dest="ver_bol", default=0, help="Shows version and licensing information.", action="store_true")
        parser.add_option("-w", "--license", dest="license_bol", default=0, help="Prints the GPLv3 license information.", action="store_true")
        (options, args) = parser.parse_args()
        return options


    # Here actually starts Main()

    # Zeroing everything
    m = []

    arguments = getArgvs()

    # Checking for EULA Agreement
    a = eulaHandler.check_eula_file()
    if a == 0:
        eulaHandler.prompt_eula()

    # Get arguments
    
    # Check if update flag is on
    if arguments.update_bol == 1:
        a = Updater()
        a.update_db()
        sys.exit(1)

    # Check if version flag is on
    if arguments.ver_bol == 1:
        print vars.maldb_banner
        sys.exit(1)

    # Check if license flag is on
    if arguments.license_bol == 1:
        bannerHandler.print_license()
        sys.exit(1)

    if (len(arguments.type_of_mal) > 0) or (len(arguments.arch_of_mal) > 0) or (len(arguments.lang_of_mal) > 0) or (len(arguments.plat_of_mal) > 0):

        # Take index.csv and convert into array m
        csvreader = csv.reader(open(vars.main_csv_file, 'rb'), delimiter=',')
        for row in csvreader:
            m.append(row)

        # Filter by type
        if len(arguments.type_of_mal) > 0:
            m = filter_array(m, vars.column_for_type, arguments.type_of_mal)

        # Filter by programming language
        if len(arguments.lang_of_mal) > 0:
            m = filter_array(m, vars.column_for_plat, arguments.lang_of_mal)

        # Filter by architecture
        if len(arguments.arch_of_mal) > 0:
            m = filter_array(m, vars.column_for_arch, arguments.arch_of_mal)

        # Filter by Platform
        if len(arguments.plat_of_mal) > 0:
            m = filter_array(m, vars.column_for_plat, arguments.plat_of_mal)

        i=0
        print vars.maldb_banner
        print 'ID\tName\t\tType\t\tVersion\t\tLanguage'
        print '--\t----\t\t----\t\t-------\t\t--------'
        for g in m:
            #print 'now'
            answer = m[i][vars.column_for_uid]
            answer += '\t%s' % ('{0: <12}'.format(m[i][vars.column_for_name]))
            answer += '\t%s' % ('{0: <12}'.format(m[i][vars.column_for_type]))
            answer += '\t%s' % ('{0: <12}'.format(m[i][vars.column_for_version]))
            answer += '\t%s' % ('{0: <12}'.format(m[i][vars.column_for_pl]))
            print answer
            i += 1

        sys.exit(1)

    # Initiate normal run. No arguments given. 
    os.system('clear')
    print vars.maldb_banner
    while 1:
        terminalHandler.MainMenu()
    sys.exit(1)


if __name__ == "__main__":
    main()