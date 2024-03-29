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
import csv
from pathlib  import Path
import pandas as pd


from Utils.directories_walker import DirectoriesWalker


#=============================================================================
class XslxToCsvTranslator( DirectoriesWalker ):
    """The class of translators of files from .xslx to .csv formats.
    
    Note: see https://pylightxl.readthedocs.io/en/latest/sourcecode/index.html
    """   
    #-------------------------------------------------------------------------
    def __init__(self, basedir_path        : str      ,
                       excluded_directories: list = [],
                       csv_separator       : str = ',' ) -> None:
        '''Constructor.
        
        Args:
            base_directory: str
                The path to the base directory from which the version, 
                revision and date of last modification of the software 
                will be evaluated down to the directories tree.
            excluded_directories: list
                A list of excluded directories. Defaults to empty.
            csv_separator: str
                The character to use for the separation of  fields  in
                the final CSV files. Defaults to comma.
        '''
        super().__init__( basedir_path, excluded_directories )
        
        csv.register_dialect( self._UCI_CSV_DIALECT,
                              delimiter=csv_separator,
                              quoting=csv.QUOTE_NONE)

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
        ret_msg = ''
        
        try:
            # reads the XLS file
            excel_file = pd.ExcelFile( filepath )
            
            # gets the first work sheet (contains the data to prepare)
            work_sheet = excel_file.parse()
            ##work_sheet = excel_file.parse( work_sheets_names[ 0 ] )

            # prepares and opens the related CSV file
            try:
                csv_filepath = Path( filepath ).with_suffix( '.csv' )
                work_sheet.to_csv( csv_filepath )
                ret_msg = "ok"
                
            except Exception as e:
                # exception raised while creating the CSV file
                ret_msg = f"!!! Exception raised while creating CSV file '{csv_filepath:s}\n  -- {str(e):s}"
        
        except Exception as e:
            # exception raised while opening the Excel file for its reading
            ret_msg = f"!!! Exception raised while accessing Excel file\n  -- {str(e):s}"
        
        finally:
            return ret_msg

    #-------------------------------------------------------------------------
    def select(self, filepath: str) -> bool:
        '''Indicates the files that must be processed.
        
        Args:
            filepath: str
                The path to the file to process.
        
        Returns:
            True it the specified file must be processed,
            or False otherwise.
        '''
        try:
            suffix = Path( filepath ).suffix.lower()
            return suffix in [ '.xlsx', '.xls' ]
        except:
            return False

    #-------------------------------------------------------------------------
    # class data
    _UCI_CSV_DIALECT = 'uci_csv_dialect'
    
#=====   end of   UseCases.WomenCyclingDatabase.DataPreparation.xlsx_to_csv_translator   =====#
