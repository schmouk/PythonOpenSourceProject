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
## This module defines decorators:
#
#   - abstract
#


#=============================================================================
from typing import Callable


#=============================================================================

#-------------------------------------------------------------------------
def abstract(method: Callable) -> Callable:
    '''Raises exception NotImplementedfError.
    
    This decorator automatically raises a NotImplementedError
    exception  when the decorated method is called,  whatever
    its implementation is.
    
    This is finally simpler than using the  built-in  library
    abc (see https://docs.python.org/3/library/abc.html)  and 
    its decorator '@abstractmethod'.
    
    Args:
        method: Callable
            A reference to the decorated method.
    
    Returns:
        A reference to the internal  wrapper,  the  one  that
        raises the NotImplemetnedError exceptinon.
        
    Raises:
        NotImplementedError:  the decorated method is  to  be
        considered as not implemented.
    '''
    #---------------------------------------------------------------------
    def _wrapper(*args, **kwargs) -> None:
        '''The internal decorator function. Raises the exception.
        '''
        def _msg_txt() -> str:
            return f"method '{method.__name__}()' must be implemented"
        
        try:
            type_name = str(args[0]).split()
            if type_name[0] == '<class':
                class_name = type_name[1].split('.')[-1][:-2]
            else:
                class_name = args[0].__class__.__name__
        
        except:
            try:
                class_name = args[0]
            except:
                raise NotImplementedError( f"{_msg_txt()}." )
        
        raise NotImplementedError( f"{_msg_txt()} in class '{class_name}'." )
    #---------------------------------------------------------------------

    return _wrapper

#=====   end of   Utils.decorators   =====#
