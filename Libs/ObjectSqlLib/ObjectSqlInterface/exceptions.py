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
## This module defines all exceptions that are specified by PEP-249.
#
# According to PEP-249,  built-in exception Warning may be used,  as
# well as base class Error for all other exceptions.
#
# Documentation comments associated with each error class are copies
# of the text published with PEP-249.
# See: https://www.python.org/dev/peps/pep-0249
#

#=============================================================================
# no imports.

#=============================================================================
class Error( Exception ):
    '''Exception that is the base class of all other error exceptions.
    
    You can use this to catch all errors with one single 
    except statement. Warnings are not considered errors 
    and thus should not use this class as base.
    '''
    pass
    
    
class InterfaceError( Error ):
    '''Exception raised for errors that are related to the database interface rather than the database itself.
    '''
    pass


class DatabaseError( Error ):
    '''Exception raised for errors that are related to the database.
    '''
    pass


class DataError( DatabaseError ):
    '''Exception raised for errors that are due to problems with the processed data.
    
     e.g. division by zero, numeric value out of range, etc.
    '''
    pass


class OperationalError( DatabaseError ):
    '''Exception raised for errors that are related to the database's operation.
    
    These errors are not necessarily under the control of the programmer, e.g. 
    an  unexpected  disconnect  occurs,  the data source name is not found,  a 
    transaction could not be processed,  a memory  allocation  error  occurred 
    during processing, etc.
    '''
    pass


class IntegrityError( DatabaseError ):
    '''Exception raised when the relational integrity of the database is affected.
    
    e.g. a foreign key check fails.
    '''
    pass


class InternalError( DatabaseError ):
    '''Exception raised when the database encounters an internal error.
    
    e.g. the cursor is not valid anymore, the transaction is out of sync, etc.
    '''
    pass


class ProgrammingError( DatabaseError ):
    '''Exception raised for programming errors.
    
    e.g. table not found or already exists, syntax error in the SQL statement, 
    wrong number of parameters specified, etc.
    '''
    pass


class NotSupportedError( DatabaseError ):
    '''Exception raised in case a method or database API was used which is not supported by the database.
    
     e.g. requesting a .rollback() on a connection that does not support 
     transaction or has transactions turned off. 
    '''
    pass


#=====   end of   Libs.ObjectSqlLib.ObjectSqlInterface.exceptions   =====#
