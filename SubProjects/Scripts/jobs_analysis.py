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
from SubProjects.JobsAnalysis.first_analytics import FirstAnalytics


#=============================================================================
if __name__ == '__main__':
    """
    This is the very first and simplest analytics application applied to  the 
    collected keywords that are associated with a collected of jobs descript-
    ions on StackOverflow.
    """
    #-------------------------------------------------------------------------
    analytics = FirstAnalytics(
                    '../JobsAnalysis/data/jobs-keywords-2020-08-06.csv'
                )
    
    analytics.evaluate()
    
    analytics.print_stats()
  
#=====   end of   SubProjects.Scripts.jobs_analysis   =====#
