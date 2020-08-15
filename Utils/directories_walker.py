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
from os import listdir as os_listdir, path as os_path

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
    def process(self, filepath: str) -> str:
        '''The files processing step.
        
        Implement here the processing of  files.  Mind  the  returned
        message, which might be of interest for your application.
        
        This method must be implemented in inheriting classes.
        
        Args:
            filepath: str
                The path to the file to process.

        Returns:
            A message to be printed as the result of the  processing.
            This message will be printed only in verbose mode.
            
        Raises:
            NotImplementedError: This method has not been implemented 
                in the inheriting class.
        '''
        return False

    #-------------------------------------------------------------------------
    def run(self, verbose  : bool,
                  max_chars: int = 54 ) -> None:
        '''Recursively runs through directories to process them.
        
        Args:
            verbose: bool
                Set this to True to get prints on console while the script
                runs  through  directories.  Set  it  to  False to not get 
                prints. Defaults to False (i.e. silent mode).
            max_chars: int
                The maximum number of chars in  file paths  that  will  be 
                printed  on  verbose  mode.   Ellipsis  are  automatically
                inserted in paths when length of  file path  exceeds  this
                limit. Defaults to 54, which is a random value...
        '''
        self.initialize()
        
        self._walk( self.base_directory, verbose, max_chars )
        
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
                    verbose  : bool,
                    max_chars: int  ) -> None:
        '''Recursively runs through directories to modify dates of copyright.
        
        Args:
            dir_path: str
                The path to the directory to be parsed.
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
        def _print_filepath(filename: str) -> None:
            if len(filename) <= max_chars:
                filename = filename
            else:
                filename = '...' + filename[3-max_chars:]

            print( f"{filename:{the_format}}", end='  ', flush=True )
        
        #-----------------------------------------------------------------
        
        # evaluates the content of current directory
        my_dir_content = [ os_path.join(dir_path, filename) for filename in os_listdir(dir_path) ]
        
        # extracts the contained sub-directories
        my_subdirs = [ dirpath  for dirpath  in my_dir_content \
                        if os_path.isdir(dirpath) and os_path.basename(dirpath) not in self.excluded_directories ]
        
        # and extracts the contained files
        my_python_srcs = [ filepath for filepath in my_dir_content if os_path.isfile(filepath) ]
        
        # recursively runs down (left deep first) into the directories tree
        for subdir_path in my_subdirs:
            self._walk( subdir_path, verbose, max_chars )
        
        # and finally runs through the whole files that are contained in current directory 
        for file_path in my_python_srcs:
            
            if verbose:
                _print_filepath( file_path )
            
            if self.select( file_path ):
                msg = self.process( file_path )
                
                if verbose:
                    print( msg )
            
            else:
                if verbose:
                    print( 'not processed' )

#=====   end of   Utils.directories_walker   =====#
