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
from os       import (listdir as os_listdir,
                      path    as os_path   ,
                      remove  as os_remove ,
                      replace as os_replace )
import re 


#=============================================================================
class CopyrightDatesModification:
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
        self.base_directory       = base_directory
        self.excluded_directories = excluded_directories + ['__pycache__']
        self.reset() 

    #-------------------------------------------------------------------------
    def modify(self, count    : int  = -1   ,
                     verbose  : bool = False,
                     max_chars: int  = 54    ) -> None:
        '''Runs the script of modifying files content.
        
        Args:
            count: the stop number.  Once number of found copyright texts
                is  equal  to this stop-number,  file modification stops.
                Set this to -1 to run through the whole content of files.
                Defaults to -1.
            verbose: bool
                Set this to True to  get  prints  on  console  while  the
                script  runs through directories.  Set it to False to not
                get prints. Defaults to False (i.e. silent mode).
            max_chars: int
                The maximum number of chars in  file paths  that  will  be 
                printed  on  verbose  mode.   Ellipsis  are  automatically
                inserted in paths when length of  file path  exceeds  this
                limit. Defaults to 54, which has been chosen at random ;-)
        '''
        if not self.already_evaluated:
            self._run_directory( self.base_directory, count, verbose, max_chars )
    
    #-------------------------------------------------------------------------
    def reset(self) -> None:
        '''Prepares the modification of copyright dates.
        '''
        self.already_evaluated = False
        self.current_year = str( date.today().year )
        self.reg_exp = re.compile( '(1|2)[0-9]{3}' )

    #-------------------------------------------------------------------------
    def _run_directory(self, dir_path : str ,
                             count    : int ,
                             verbose  : bool,
                             max_chars: int  ) -> None:
        '''Recursively runs through directories to modify dates of copyright.
        
        Args:
            dir_path: str
                The path to the directory to be parsed.
            count: int
                The  stop number.  Once number of found copyright texts is
                equal to this stop-number,  file modification stops.  Runs
                through the whole content of files if count = -1.
            verbose: bool
                Set this to True to get prints on console while the script
                runs  through  directories.  Set  it  to  False to not get 
                prints. Defaults to False (i.e. silent mode).
            max_chars: int
                The maximum number of chars in  file paths  that  will  be 
                printed  on  verbose  mode.   Ellipsis  are  automatically
                inserted in paths when length of  file path  exceeds  this
                limit.
        '''
        the_format = f"{max_chars:d}s" 

        #-----------------------------------------------------------------
        def _get_substring(match) -> str:
            return match.string[ match.start():match.end() ]
        
        #-----------------------------------------------------------------
        def _print_verbose(src_filename: str) -> None:
            if len(src_filename) <= max_chars:
                file_name = src_filename
            else:
                file_name = '...' + src_filename[3-max_chars:]

            print( f"{file_name:{the_format}}", end='  ', flush=True )
        
        #-----------------------------------------------------------------
        
        # evaluates the content of current directory
        my_dir_content = [ os_path.join(dir_path, filename) for filename in os_listdir(dir_path) ]
        
        # extracts the contained sub-directories
        my_subdirs     = [ dirpath  for dirpath  in my_dir_content \
                            if os_path.isdir(dirpath) and os_path.basename(dirpath) not in self.excluded_directories ]
        
        # and extracts the contained files
        my_python_srcs = [ filepath for filepath in my_dir_content \
                            if (filepath.endswith('.py') or filepath.endswith('.pyw')) and os_path.isfile(filepath) ]
        
        # recursively runs down (left deep first) into the directories tree
        for subdir_path in my_subdirs:
            self._run_directory( subdir_path, count, verbose, max_chars )
        
        # and finally runs through the whole files that are contained in current directory 
        for python_src_path in my_python_srcs:
            
            if verbose:
                _print_verbose( python_src_path )
            
            b_modified = False
            
            # opens current file
            with open( python_src_path, 'r' ) as fp:
                
                # reads the whole lines
                file_content = fp.readlines()
                
                # runs through each line
                for num_line, line in enumerate(file_content):
                    if 'Copyright ' in line:
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
                                count += 1
                        
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
                                count += 1

                        count -= 1
                        if count == 0:
                            # ok, let's stop modifying copyright dates in this file
                            break
                        
            if b_modified:
                # some copyright dates have been modified,
                # so we have to modify file
                try:
                    if verbose:
                        print( 'modified' )
                    # save modified file
                    new_name = python_src_path+'~'
                    with open( new_name, 'w' ) as fp:
                        fp.writelines( file_content )
                        
                    # remove former one and rename new one
                    os_remove( python_src_path )
                    os_replace( new_name, python_src_path )
                    
                except Exception as e:
                    print( f"!!! Exception raised while modifying file'{python_src_path:s}\n  -- {str(e):s}" )
            else:
                if verbose:
                    print( 'ok' )


        self.already_evaluated = True

#=====   end of   Utils.copyright_dates_modification   =====#
