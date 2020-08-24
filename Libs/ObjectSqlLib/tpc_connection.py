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
from typing import List, Optional, Tuple

from Utils.decorators import abstract
from . import Connection, warning


#=============================================================================
XID = Tuple[ int, bytes, bytes ]


#=============================================================================
class TPCConnection( Connection ):
    """The class of Two-Phase Commit, extension of Connection.
    
    From PEP 249 DB-API Extension:
    Many databases have support for two-phase  commit  (TPC)  which 
    allows  managing transactions across multiple database connect-
    ions and other resources.

    If a database backend provides support for two-phase commit and 
    the database module author wishes to expose this  support,  the 
    following  API  should be implemented. NotSupportedError should 
    be raised, if the database backend support for two-phase commit 
    can only be checked at run-time.
    
    
    -- TPC Transaction IDs
    As many databases follow the XA specification,  transaction IDs 
    are formed from three components:
    
        a format ID
        a global transaction ID
        a branch qualifier
    
    For a particular global transaction,  the first two  components 
    should  be  the  same  for all resources.  Each resource in the 
    global  transaction  should  be  assigned  a  different  branch 
    qualifier.
    
    The various components must satisfy the following criteria:
    
        format ID: a non-negative 32-bit integer.
        global transaction ID and branch qualifier: byte strings no 
        longer than 64 characters.
    
    Transaction IDs are created with the .xid() Connection method.
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
    @abstract
    def tpc_begin(self, _xid: XID) -> None:
        '''Begins a TPC transaction with the given transaction ID xid.

        From PEP 249:
        This method should  be  called  outside  of  a  transaction
        (i.e.  nothing may have executed since the last '.commit()' 
        or '.rollback()').
    
        Furthermore,   it  is  an  error  to  call  '.commit()'  or 
        .rollback() within the TPC transaction.  A ProgrammingError 
        is  raised,   if  the  application  calls  '.commit()'   or 
        '.rollback()' during an active TPC transaction.
    
        If  the  database  connection  does  not  support  TPC,   a 
        NotSupportedError is raised.
        '''
        ...


    #-------------------------------------------------------------------------
    @abstract
    def tpc_commit(self, _xid: Optional[XID] = None) -> None:
        '''TPC transactions committing.
        
        From PEP 249:
        When called with no arguments,  .tpc_commit() commits a TPC 
        transaction previously prepared with .tpc_prepare().
    
        If '.tpc_commit()' is called prior to  '.tpc_prepare()',  a 
        single phase commit is performed. A transaction manager may 
        choose to do this if only a single resource is  participat-
        ing in the global transaction.
    
        When called with a transaction ID xid, the database commits 
        the  given  transaction.  If  an  invalid transaction ID is 
        provided, a ProgrammingError  will  be  raised.  This  form 
        should be called outside of a transaction,  and is intended 
        for use in recovery.
    
        On return, the TPC transaction is ended.
        '''
        ...


    #-------------------------------------------------------------------------
    @abstract
    def tpc_prepare(self) -> None:
        '''Performs the first phase of a transaction started with .tpc_begin().
        
        From PEP 249:
        A ProgrammingError should be raised if this method  outside 
        of a TPC transaction.

        After calling .tpc_prepare(), no statements can be executed 
        until .tpc_commit() or .tpc_rollback() have been called.
        '''
        ...
        

    #-------------------------------------------------------------------------
    @abstract
    def tpc_recover(self) -> List[XID]:
        '''Returns a list of pending transaction IDs suitable for use with .tpc_commit(xid) or .tpc_rollback(xid).

        From PEP 249:
        If the database does not support transaction  recovery,  it 
        may return an empty list or raise NotSupportedError.
        '''
        ...
        

    #-------------------------------------------------------------------------
    @abstract
    def tpc_rollback(self, _xid: Optional[XID] = None) -> None:
        '''Rolls back a TPC transaction.
        
        From PEP 249:
        When called with no arguments, .tpc_rollback() rolls back a 
        TPC   transaction.   It  may  be  called  before  or  after 
        .tpc_prepare().
    
        When called with a transaction ID xid,  it rolls  back  the 
        given transaction.  If an invalid transaction ID is provid-
        ed,  a ProgrammingError is  raised.  This  form  should  be 
        called outside of a transaction, and is intended for use in 
        recovery.
    
        On return, the TPC transaction is ended.
        '''
        ...
        

    #-------------------------------------------------------------------------
    def xid(self, format_id            : int,
                  global_transaction_id: bytes,
                  branch_qualifier     : bytes ) -> XID:
        '''Returns a transaction ID object suitable for passing to the .tpc_*() methods of this connection.

        From PEP 249:
        If  the  database  connection  does  not  support  TPC,   a 
        NotSupportedError is raised.
    
        The type of the object returned by .xid() is  not  defined, 
        but it must provide sequence behaviour,  allowing access to 
        the three components.  A conforming database  module  could 
        choose to represent transaction IDs with tuples rather than 
        a custom object.
    
        format ID: a non-negative 32-bit integer.
        global transaction ID and branch qualifier: byte strings no longer than 64 characters.
        '''
        warning( "DB-API extension TPC Connection.xid used")
        assert 0 <= format_id <= 0xffff_ffff
        assert len( global_transaction_id ) <= 64
        assert len( branch_qualifier ) <= 64
        
        return (format_id, global_transaction_id, branch_qualifier )


#=====   end of   Libs.ObjectSqlLib.tpc_connection   =====#
