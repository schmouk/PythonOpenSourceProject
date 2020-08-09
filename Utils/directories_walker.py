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
import os.listdir, os.path, os.remove, os.replace

from Utils.decorators import abstract


#=============================================================================
class DirectoriesWalker:
    """The class of walkers through directories trees.
    
    These  walkers recursively walk through directories trees and apply a
    processing to every files found that respect a selection criteria.
    
    Usage:
        - Instantiate this class by passing the root directory  to  start
          the walk through and a list of excluded sub-directories if any.
        - then call 'run()' with the appropriate arguments.
    
    Abstract method 'process()' must be implemented in inheriting classes
    and  should return True or False according to the status of the proc-
    essing of the specified file in its arguments list.
    
    Method 'select()' may be overwritten to specify (to select) the files
    that must be processed and the ones that do not need to.
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


    #-------------------------------------------------------------------------
    def finalize(self) -> None:
        '''Finalization of the walking through directories.
        
        Any action that must be taken after the recursive processing
        of files has completed may be processed here.
        
        In this base class, nothing is done.
        '''
        pass


    #-------------------------------------------------------------------------
    def initialize(self) -> None:
        '''Initialization of the walking through directories.
        
        Any action that must be taken before the recursive processing
        of files may be processed here.
        
        In this base class, nothing is done.
        '''
        pass


    #-------------------------------------------------------------------------
    @abstract
    def process(self, filepath: str) -> None:
        '''The files processing step.
        
        Implement here the processing of files.  Do not  forget
        to return True if processing was ok or False otherwise.
        
        This method must be implemented in inheriting classes.
        
        Args:
            filepath: str
                The path to the file to process.
        
        Returns:
            True if processing was ok, or False otherwise.
            
        Raises:
            NotImplementedError: This method is not implemented
                in the inheriting class.
        '''
        ...


    #-------------------------------------------------------------------------
    def run(self, dir_path : str ,
                   count    : int ,
                   verbose  : bool,
                   max_chars: int  ) -> None:
        '''Recursively runs through directories to process them.
        
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
        self.initialize()
        
        self._walk( dir_path, count, verbose, max_chars )
        
        self.finalize()


    #-------------------------------------------------------------------------
    def select(self, filepath: str) -> bool:
        '''Indicates the files that must be processed.
        
        This method may be implemented in inheriting classes.
        It indicates the files which must be processed.
        
        Args:
            filepath: str
                The path to the file to process.
        
        Returns:
            True it the specified file must be processed,  or 
            False  otherwise.  In this base class,  ALL files 
            are said to be processed.
        '''
        return True


    #-------------------------------------------------------------------------
    def _walk(self, dir_path : str ,
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
        def _print_verbose(filename: str) -> None:
            if len(filename) <= max_chars:
                filename = filename
            else:
                filename = '...' + filename[3-max_chars:]

            print( f"{filename:{the_format}}", end='  ', flush=True )
        
        #-----------------------------------------------------------------
        
        # evaluates the content of current directory
        my_dir_content = [ os.path.join(dir_path, filename) for filename in os.listdir(dir_path) ]
        
        # extracts the contained sub-directories
        my_subdirs = [ dirpath  for dirpath  in my_dir_content \
                        if os.listdir.isdir(dirpath) and os.listdir.basename(dirpath) not in self.excluded_directories ]
        
        # and extracts the contained files
        my_python_srcs = [ filepath for filepath in my_dir_content \
                            if (filepath.endswith('.py') or filepath.endswith('.pyw')) and os.listdir.isfile(filepath) ]
        
        # recursively runs down (left deep first) into the directories tree
        for subdir_path in my_subdirs:
            self._walk( subdir_path, count, verbose, max_chars )
        
        # and finally runs through the whole files that are contained in current directory 
        for file_path in my_python_srcs:
            
            if verbose:
                _print_verbose( file_path )
            
            if self.select( file_path ):
                ok = self.process( file_path )
                
                if verbose:
                    print( ' ok' if ok else ' not-ok' )
            
            else:
                if verbose:
                    print( ' not processed' )


#=====   end of   Utils.directories_walker   =====#
