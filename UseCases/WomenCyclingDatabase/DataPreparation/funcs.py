#!/usr/bin/env python
"""
Copyright (c) 2020 Philippe Schmouker

Project: 

Permission is hereby granted,  free of charge,  to any person obtaining a copy
of this software and associated documentation files (the "Software"),  to deal
in the Software without restriction, including  without  limitation the rights
to use,  copy,  modify,  merge,  publish,  distribute, sublicense, and/or sell
copies of the Software,  and  to  permit  persons  to  whom  the  Software  is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS",  WITHOUT WARRANTY OF ANY  KIND,  EXPRESS  OR
IMPLIED,  INCLUDING  BUT  NOT  LIMITED  TO  THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT  SHALL  THE
AUTHORS  OR  COPYRIGHT  HOLDERS  BE  LIABLE  FOR  ANY CLAIM,  DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT,  TORT OR OTHERWISE, ARISING FROM,
OUT  OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#=============================================================================
## This module defines functions:
#
#   - xslsToCsvTranslator()
#


#=============================================================================
import csv
import os.path


#=============================================================================
def xslsToCsvTranslator(base_dirpath: str,
                        csv_sep     : str = ',',
                        verbose     : bool = False) -> None:
        '''Translates files from .xslx format to .csv format.
        
        This translator starts its running on  a  specified  root
        directory  and translates every '.xslx' files into '.csv' 
        ones by recursively walking through the directories tree.
        
        Args:
            base_dirpath: str
                The path to the root directory from which transl-
                ationshould be recursively applied to the direct-
                ories tree.
            csv_sep: str
                The character that is  to  be  used  to  separate 
                fields in the final '.csv' files.
                Defaults to comma.
            verbose: bool
                Set this to True to get  rints while  translation 
                is applied to every files,  or set it to False to 
                not get those prints.
                Defaults to None (i.e. quiet mode).
        '''
        ...

#=====   end of   UseCases.WomenCyclingDatabase.DataPreparation.funcs   =====#
