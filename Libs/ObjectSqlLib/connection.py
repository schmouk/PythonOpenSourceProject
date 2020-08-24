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
from typing import Optional

from Utils.decorators import abstract
from .                import Cursor, warning


#=============================================================================
class Connection:
    """Class of connection objects.
    
    This is an interface, i.e. an abstract class.
    It declares the methods that must be implemented  in  inheriting 
    classes.  Every  declarations here are abstract but next methods
    which may be overwritten or overloaded in implementing classes:
      - .__init__()
      - .__del__()
      - .cursor()
    
    It conforms to PEP 249 - Python Database API Specification v2.0.
    The docstrings are copies of text published at:
    https://www.python.org/dev/peps/pep-0249
    """
    
    #-------------------------------------------------------------------------
    @abstract
    def __init__(self, _dsn     : str,
                       _user    : Optional[str] = None,
                       _password: Optional[str] = None,
                       _host    : Optional[str] = None,
                       _database: Optional[str] = None ) -> None:
        '''Constructor.
        
        Creates a new connection to the specified DB.
        
        MUST BE IMPLEMENTED in inheriting classes.
        
        Note from PEP 249:
        As a guideline the connection constructor parameters should 
        be implemented as keyword parameters for more intuitive use 
        and follow this order of parameters:
            Parameter     Meaning
            dsn          Data source name as string
            user         User name as string (optional)
            password     Password as string (optional)
            host         Hostname (optional)
            database     Database name (optional)
        '''
        ...
    
    #-------------------------------------------------------------------------
    def __del__(self) -> None:
        '''Destructor.
        
        Definitively closes this connection.
        Notice: this method is not part of PEP 249.
        '''
        self.close()

    #-------------------------------------------------------------------------
    @abstract
    def close(self) -> None:
        '''Close the connection now (rather than whenever .__del__() is called).
    
        The connection will be unusable from  this  point  forward;
        an  Error  (or  subclass )  exception will be raised if any 
        operation  is  attempted  with  the  connection.  The  same 
        applies to all cursor objects trying to use the connection. 
        Note that  closing  a  connection  without  committing  the 
        changes  first  will cause an implicit rollback to be perf-
        ormed.
        
        Caution (PEP 249): Closing a connection without  committing 
        the  changes  first  will  cause an implicit rollback to be 
        performed.
        '''
        ...
    
    #-------------------------------------------------------------------------
    @abstract
    def commit(self) -> None:
        '''Commit any pending transaction to the database.
    
        Note that if the database supports an auto-commit  feature, 
        this  must  be  initially  off.  An interface method may be 
        provided to turn it back on.
    
        Database modules that do not  support  transactions  should 
        implement this method with void functionality.
        '''
        ...

    #-------------------------------------------------------------------------
    def cursor(self) -> Cursor:
        '''Return a new Cursor Object using the connection.
    
        If the database does not provide a direct  cursor  concept, 
        the  module  will have to emulate cursors using other means 
        to the extent needed by this specification.
        
        Note (PEP 249):  A database interface may choose to support 
        named cursors by allowing a string argument to the  method. 
        This feature is not part of  the  specification,  since  it 
        complicates semantics of the .fetch*() methods.
        (this feature is NOT implemented in this base interface. It
        may be implemented in inheriting classes via overloading).
        '''
        return Cursor( self )

    #-------------------------------------------------------------------------
    @abstract
    def rollback(self) -> None:
        '''This method is optional since not all databases provide transaction support. [3]
    
        In case a database does provide  transactions  this  method 
        causes  the database to roll back to the start of any pend-
        ing transaction.  Closing a connection  without  committing 
        the  changes  first  will  cause an implicit rollback to be 
        performed.
        
        Note (PEP 249):  If  the  database  does  not  support  the 
        functionality  required by the method, the interface should 
        throw an exception in case the method is used.
        The preferred approach is to not implement the  method  and 
        thus  have  Python  generate  an AttributeError in case the 
        method is requested. This allows the  programmer  to  check 
        for  database  capabilities  using  the  standard hasattr() 
        function. For some dynamically configured interfaces it may 
        not be appropriate to require dynamically making the method 
        available.   These   interfaces   should   then   raise   a 
        NotSupportedError  to  indicate  the non-ability to perform 
        the roll back when the method is invoked.
        '''
        ...


#=============================================================================
## PEP 249: Optional DB API Extensions
#
#    Next exceptions definitions are part of the Connection
#    class to conform with PEP 249 DB-API Extensions.  They
#    are set as their originals are  in module exceptions.
#

    class Error( Exception ):
        '''Exception that is the base class of all other error exceptions.
        
        You can use this to catch all errors with one single 
        except statement. Warnings are not considered errors 
        and thus should not use this class as base.
        '''
        warning( "DB-API extension Connection.Error used" )
        
        
    class InterfaceError( Error ):
        '''Exception raised for errors that are related to the database interface rather than the database itself.
        '''
        warning( "DB-API extension Connection.InterfaceError used" )
    
    
    class DatabaseError( Error ):
        '''Exception raised for errors that are related to the database.
        '''
        warning( "DB-API extension Connection.DatabaseError used" )
    
    
    class DataError( DatabaseError ):
        '''Exception raised for errors that are due to problems with the processed data.
        
         e.g. division by zero, numeric value out of range, etc.
        '''
        warning( "DB-API extension Connection.DataError used" )
    
    
    class OperationalError( DatabaseError ):
        '''Exception raised for errors that are related to the database's operation.
        
        These errors are not necessarily under the control of the programmer, e.g. 
        an  unexpected  disconnect  occurs,  the data source name is not found,  a 
        transaction could not be processed,  a memory  allocation  error  occurred 
        during processing, etc.
        '''
        warning( "DB-API extension Connection.OperationalError used" )
    
    
    class IntegrityError( DatabaseError ):
        '''Exception raised when the relational integrity of the database is affected.
        
        e.g. a foreign key check fails.
        '''
        warning( "DB-API extension Connection.IntegrityError used" )
    
    
    class InternalError( DatabaseError ):
        '''Exception raised when the database encounters an internal error.
        
        e.g. the cursor is not valid anymore, the transaction is out of sync, etc.
        '''
        warning( "DB-API extension Connection.InternalError used" )
    
    
    class ProgrammingError( DatabaseError ):
        '''Exception raised for programming errors.
        
        e.g. table not found or already exists, syntax error in the SQL statement, 
        wrong number of parameters specified, etc.
        '''
        warning( "DB-API extension Connection.ProgrammingError used" )
    
    
    class NotSupportedError( DatabaseError ):
        '''Exception raised in case a method or database API was used which is not supported by the database.
        
         e.g. requesting a .rollback() on a connection that does not support 
         transaction or has transactions turned off. 
        '''
        warning( "DB-API extension Connection.NotSupportedError used" )


#=====   end of   Libs.ObjectSqlLib.connection   =====#
