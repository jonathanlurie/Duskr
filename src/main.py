'''
BLANK_PY
=============
Copyright (c) 2015, Jonathan LURIE, All rights reserved.
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3.0 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library.
'''

import os
from SettingFileReader import *

import re

from XmpManager import *




# main
if __name__ == '__main__':

    # cleaning terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    print("________________________________________________________________________________")
    print("\t  ____            _         ")
    print("\t |  _ \ _   _ ___| | ___ __ ")
    print("\t | | | | | | / __| |/ / '__|")
    print("\t | |_| | |_| \__ \   <| |   ")
    print("\t |____/ \__,_|___/_|\_\_|   ")
    print("\n\t  Timelaspe interpolation")
    print("________________________________________________________________________________")

    #firstRawImage = "/Users/jonathanlurie/Documents/code/data/NEFpictures/_NIK4337.NEF"

    notDefined = True
    while(notDefined):
        firstRawImage = str.strip(raw_input('\n1- Drag and drop the first raw image of your sequence, then press Enter:\n> '))

        if(not os.path.isfile(firstRawImage)):
            print("ERROR: this file does not exist.")
        else:
            print("\n")
            notDefined = False


    xmpMngr = XmpManager(firstRawImage)
    xmpMngr.process()
