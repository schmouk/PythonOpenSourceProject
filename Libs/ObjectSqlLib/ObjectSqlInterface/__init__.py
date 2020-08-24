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
## This module contains:
#
#    - global definitions as specified in PEP 249 (https://www.python.org/dev/peps/pep-0249)
#    - imports of this interface classes
#

#=============================================================================
from typing import Final


#=============================================================================
from .connect    import Connect
from .cursor     import Cursor
from .db_types   import *
from .exceptions import *


#=============================================================================
## PEP 249 mandatory Globals

#-------------------------------------------------------------------------
apilevel: Final[str] = '2.0'  # or '1.0'

threadsafety: Final[int] = 1
#===============================================================================
# threadsafety     Meaning
#     0         Threads may not share the module.
#     1         Threads may share the module, but not connections.
#     2         Threads may share the module and connections.
#     3         Threads may share the module, connections and cursors.
#===============================================================================

paramstyle: Final[str] = 'format'
#===============================================================================
# paramstyle       Meaning
#   qmark       Question mark style, e.g. ...WHERE name=?
#   numeric     Numeric, positional style, e.g. ...WHERE name=:1
#   named       Named style, e.g. ...WHERE name=:name
#   format      ANSI C printf format codes, e.g. ...WHERE name=%s
#   pyformat    Python extended format codes, e.g. ...WHERE name=%(name)s
#===============================================================================
