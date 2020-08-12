#!/usr/bin/env python
"""
Copyright (c) 2020 Philippe Schmouker

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
from datetime import  date
from os       import (remove  as os_remove ,
                      replace as os_replace )
from pathlib  import  Path

import re

from .directories_walker import DirectoriesWalker


#=============================================================================
class CopyrightDatesModification( DirectoriesWalker ):
    """Helps the automation for modifying the dates of copyrights.
    """
    
    #-------------------------------------------------------------------------
    def __init__(self, base_directory: str,
                       excluded_directories: list = []) -> None:
        '''Constructor.
        
        Args:
            base_directory: str
                The path to the base directory from which the version, 
                revision and date of last modification of the software 
                will be evaluated down to the directories tree.
            excluded_directories: list
                A list of excluded directories. Defaults to empty.
        '''
        super().__init__( base_directory, excluded_directories + ['__pycache__'] )

    #-------------------------------------------------------------------------
    def initialize(self) -> None:
        '''Prepares the modification of copyright dates.
        '''
        self.current_year = str( date.today().year )
        self.reg_exp = re.compile( '(1|2)[0-9]{3}' )

    #-------------------------------------------------------------------------
    def process(self, filepath: str) -> str:
        '''The files processing step.
        
        Args:
            filepath: str
                The path to the file to process.

        Returns:
            A message to be printed as the result of the processing.
            This message will be printed only in verbose mode.
        '''
        #-----------------------------------------------------------------
        def _get_substring(match) -> str:
            return match.string[ match.start():match.end() ]
        #-----------------------------------------------------------------
        
        ret_msg = ''
        
        try:
            # opens current file
            with open( filepath, 'r' ) as fp:
                
                b_modified = False
                
                # reads the whole lines
                file_content = fp.readlines()
                
                # runs through each line
                for num_line, line in enumerate(file_content):
                    if 'Copyright ' in line or 'copyright' in line:
                        # ok, copyright has been found
                        dates_match = [ d for d in self.reg_exp.finditer( line ) ]
                        
                        if len(dates_match) == 1:
                            try:
                                # only one date. Is it current year?
                                the_year = _get_substring( dates_match[0] )
                                if the_year != self.current_year:
                                    # well, no. So let's append current year in between
                                    my_start_index, my_end_index = dates_match[0].start(), dates_match[0].end()
                                    file_content[ num_line ] = f"{line[:my_end_index]}-{self.current_year}{line[my_end_index:]}"
                                    b_modified = True
                            except:
                                pass
                        
                        else:
                            try:
                                # two dates (and no more according to our copyright conventions)
                                end_year = _get_substring( dates_match[1] )
                                # does last year equals current one? 
                                if end_year != self.current_year:
                                    # well, no. So, let's change ending year with current one
                                    my_start_index, my_end_index = dates_match[1].start(), dates_match[1].end()
                                    file_content[ num_line ] = f"{line[:my_start_index]}{self.current_year}{line[my_end_index:]}"
                                    b_modified = True
                            except:
                                pass
                        
            if b_modified:
                # some copyright dates have been modified,
                # so we have to modify file
                try:
                    ret_msg = '--> modified <--'
                        
                    # save modified file
                    new_name = filepath + '~'
                    with open( new_name, 'w' ) as fp:
                        fp.writelines( file_content )
                        
                    # remove former one and rename new one
                    os_remove( filepath )
                    os_replace( new_name, filepath )
                    
                except Exception as e:
                    ret_msg = f"!!! Exception raised while modifying file '{filepath:s}\n  -- {str(e):s}"
            else:
                ret_msg = 'already ok'
        
        except Exception as e:
            ret_msg = f"!!! Exception raised while accessing file\n  -- {str(e):s}"
        
        finally:
            return ret_msg

    #-------------------------------------------------------------------------
    def select(self, filepath: str) -> bool:
        '''Indicates the files that must be processed.
        
        Args:
            filepath: str
                The path to the file to process.
        
        Returns:
            True it the specified file must be processed, or 
            False otherwise.
        '''
        try:
            suffix = Path( filepath ).suffix.lower()
            return suffix in [ '.py', '.pyw', 
                               '.htm', '.html', '.js', '.css',
                               '.txt', '.md',
                               '.cpp', '.php', '.java', '.go' ]
        except:
            return False

#=====   end of   Utils.copyright_dates_modification   =====#
