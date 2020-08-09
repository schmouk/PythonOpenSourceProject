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
from csv import reader, Sniffer


#=============================================================================
class FirstAnalytics:
    '''The class of simple analytics on jobs keywords.
    
    This class sorts keywords according to their respective
    frequencies,  and prints their associations with  other
    keywords according  to  their  respective  associations
    frequencies also.
    '''
    
    #---------------------------------------------------------------------
    def __init__(self, filepath: str) -> None:
        '''
       Opens the data file and loads its content.
       
        Args:
            filepath: str
                The path to the data file that contains  keywords
                associated with the collected jobs descriptions.
    
        Raises:
            FileNotFoundError: filepath is not correct or related
                file cannot be found.
            PermissionError: read access to  the  specified  file
                cannot be granted 
        '''
        with open( filepath, 'r' ) as csv_f:
            
            # automatically detects separators and internal format of the CSV file
            csv_dialect = Sniffer().sniff( csv_f.read(1024) )
            
            # rewinds it
            csv_f.seek( 0 )
            
            # and reads its content
            self.entries = [ row for row in reader( csv_f, csv_dialect ) ]
            
    #---------------------------------------------------------------------
    def evaluate(self) -> None:
        '''Evaluates the stats on keywords content.
        '''
        # prepares analytics
        self.kw_counts = dict()
        self.kw_associations = dict()
        
        # and 'parses' it
        for entry in self.entries:
            for kw in entry:
                # counts the occurences of keywords
                if kw != '':
                    try:
                        self.kw_counts[ kw ] += 1
                    except:
                        self.kw_counts[ kw ] = 1

            nb = len( entry )
            for i, kw in enumerate( entry[:-1] ):
                if kw != '':
                    for j in range(i+1, nb):
                        kw_a = entry[ j ]
                        if kw_a != '':
                            # adds the association kw/kw_a in dict
                            self._associate( kw, kw_a )
                            # and adds the association kw_a/kw in dict
                            self._associate( kw_a, kw )

    #---------------------------------------------------------------------
    def print_stats(self) -> None:
        '''Finally prints statistics on keywords.
        '''
        # sorts keywords according to their frequency
        final_counts = self._get_sorted_counts( self.kw_counts )
        
        max_kw_length = max( [ len(kw.kw) for kw in final_counts ] )
        kw_format = f'<{max_kw_length+1}s'
        
        prev_key_count = -1
        prev_rank = -1
        for rank, key_count in enumerate(final_counts):
            #-- First, prints ranking and count of every sorted keyword
            # is this a same ranking btw keywords?
            if key_count.count == prev_key_count:
                rank = prev_rank
            else:
                prev_rank = rank
                prev_key_count = key_count.count
            
            # let's print then the keyword, its ranking and its count
            print( f"\n{rank+1:3d}. {key_count.kw:{kw_format}} - {key_count.count:4d}" )
            
            #-- Then, prints its ranked associations
            assoc_counts = self._get_sorted_counts( self.kw_associations[key_count.kw] )
            
            for kc in assoc_counts:
                print( f"            - {kc.kw:{kw_format}} - {kc.count:4d}" )

    #---------------------------------------------------------------------
    def _associate(self, kw1: str, kw2: str) -> None:
        '''Private method for the association of keywords.
        '''
        if kw1 in self.kw_associations:
            if kw2 in self.kw_associations[kw1]:
                self.kw_associations[kw1][kw2] += 1
            else:
                self.kw_associations[kw1][kw2] = 1
        else:
            self.kw_associations[kw1] = dict()
            self.kw_associations[kw1][kw2] = 1

    #---------------------------------------------------------------------
    def _get_sorted_counts(self, kw_dict: dict) -> list:
        '''Returns a list sorted on keywords and on their counts.
        '''
        counts = ( [ self._KwCountEntry(k,v) for k,v in sorted(kw_dict.items()) ] )
        counts.sort( reverse=True )
        return counts
        

    #---------------------------------------------------------------------
    class _KwCountEntry:
        def __init__(self, kw: str, count: int) -> None:
            self.kw = kw
            self.count = count
            
        def __lt__(self, other) -> bool:
            return self.count < other.count

#=====   end of   SubProjects.JobsAnalysis.first_analytics   =====#
