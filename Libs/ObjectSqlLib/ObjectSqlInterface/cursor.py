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
from typing import ForwardRef, List, Optional, Tuple, Union

from Utils.decorators import abstract
from . import Type as DBType


#=============================================================================
ConnectionRef = ForwardRef( "Connection" )


#=============================================================================
class Cursor:
    """The class of DB cursors.
    
    Copy from PEP 249:
    These objects represent a database cursor,  which  is  used  to 
    manage  the context of a fetch operation.  Cursors created from 
    the same connection are not isolated, i.e., any changes done to 
    the  database  by a cursor are immediately visible by the other 
    cursors.  Cursors created from different connections can or can 
    not  be  isolated,  depending on how the transaction support is 
    implemented  (see  also  the  connection's  '.rollback()'   and 
    '.commit()' methods).
    """
    
    #-------------------------------------------------------------------------
    def __init__(self, parent_connection: ConnectionRef) -> None:
        '''Constructor.
        
        Args:
            parent_connection: ConnectionRef
                A reference  to  the  connection  from  which  this
                cursor  has  been instantiated. Notice: this is not
                part of PEP 249 and is provided as a convenience to
                get easy access to initializing connections.
        '''
        self.connection = parent_connection
        self._reset_row_descr()
        self._row_count = self.NO_ROW_COUNT
        self._array_size = 1

    
    #-------------------------------------------------------------------------
    def __del__(self) -> None:
        '''Destructor.
        
        This is not part of PEP 249.
        '''
        self.close()
        

    #-------------------------------------------------------------------------
    @property
    def arraysize(self) -> int:
        '''Specifies the number of rows to fetch at a time with .fetchmany().
        
        It defaults to 1 meaning to fetch a single row at a time.
    
        Implementations must observe this value with respect to the 
        '.fetchmany()'  method,  but  are free to interact with the 
        database a single row at a time. It may also be used in the 
        implementation of .executemany().
        '''
        return self._array_size
        
    @arraysize.setter
    def arraysize(self, size: int) -> None:
        '''Specifies the number of rows to fetch at a time with .fetchmany().
        
        It defaults to 1 meaning to fetch a single row at a time.
    
        Implementations must observe this value with respect to the 
        '.fetchmany()'  method,  but  are free to interact with the 
        database a single row at a time. It may also be used in the 
        implementation of .executemany().
        '''
        assert size > 0
        self._array_size = size
        
        
    #-------------------------------------------------------------------------
    @property
    def description(self) -> Tuple[str, DBType, Optional[int], Optional[int], Optional[int], Optional[int], Optional[bool]]:
        '''This read-only attribute is a sequence of 7-item sequences.
        
        From PEP 249:
        Each of these sequences contains information describing one result column:
        
            name
            type_code
            display_size
            internal_size
            precision
            scale
            null_ok

        The first two items (name and type_code) are mandatory, the 
        other five are optional and are set to None if no mean-
        ingful values can be provided.
        
        This attribute will be None  for  operations  that  do  not 
        return  rows or if the cursor has not had an operation inv-
        oked via the .execute*() method yet.
        
        The type_code can be interpreted by comparing it to the 
        Type Objects specified in module 'types'
        '''
        return (self.row_name,
                self.row_type,
                self.row_display_size,
                self.row_internal_size,
                self.row_precision,
                self.row_scale,
                self.row_null_ok)


    #-------------------------------------------------------------------------
    @property
    def rowcount(self) -> int:
        '''Specifies the number of rows that the last .execute*() produced (for DQL statements like SELECT) or affected (for DML statements like UPDATE or INSERT).

        From PEP 249:
        This read-only attribute is implemented here as a property.
        It  is  based  on  protected  attribute '._row_count' which
        should be set in '.execute*()' methods.It is the responsib-
        ility  of  the implementor of this base interface to ensure 
        that this protected attribute  will  be  correctly  set  in 
        there. Notice: the default value of this attribute is -1 in 
        case no .execute*() has been performed on the  ursor or the 
        rowcount  of  the last operation is cannot be determined by 
        the interface (as per PEP 249 in its  version 2.0).  Future 
        versions  of  the DB API specification (i.e. PEP 249) could 
        redefine it as None instead of -1.
        
        From PEP 249:
        
        The attribute is -1 in case no .execute*() has  been  perf-
        ormed  on  the cursor or the rowcount of the last operation 
        is cannot be determined by the interface.
        
        The term number of affected rows generally  refers  to  the 
        number  of  rows  deleted,  updated or inserted by the last 
        statement run on the database cursor.  Most databases  will 
        return  the  total  number  of  rows that were found by the 
        corresponding WHERE clause of the statement. Some databases 
        use  a different interpretation for UPDATEs and only return 
        the number of rows that were changed by  the  UPDATE,  even 
        though  the  WHERE  clause  of the statement may have found 
        more matching rows.  Database module authors should try  to 
        implement  the  more common interpretation of returning the 
        total number of rows found by the WHERE clause,  or clearly 
        document   a  different  interpretation  of  the  .rowcount 
        attribute.
        '''
        return self._row_count


    #-------------------------------------------------------------------------
    @abstract
    def callproc(self, proc_name: str, *parameters) -> Optional:
        '''Calls a stored database procedure with the given name.
        
        From PEP 249:
        (This method is optional since not  all  databases  provide 
         stored procedures.)

        The sequence of parameters must contain one entry for  each 
        argument that the procedure expects. The result of the call 
        is returned as modified copy of the input  sequence.  Input 
        parameters  are  left  untouched,  output  and input/output 
        parameters replaced with possibly new values.

        The procedure may also provide a result set as output. This 
        must  then be made available through the standard .fetch*() 
        methods.

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
        
        Args:
            proc_name: str
                The name of the stored database procedure to call.
            parameters: tuple
                A reference to the parameters  values  to  pass  as 
                arguments of the stored database procedure.
        
        Returns:
            A reference to some output as set by standard .fetch*() 
            methods, or nothing at the wish of the implementor.
        '''
        ...


    #-------------------------------------------------------------------------
    @abstract
    def close(self) -> None:
        '''Closes the cursor now (rather than whenever __del__ is called).

        From PEP 249:
        The cursor will be unusable from  this  point  forward;  an 
        Error  (or  subclass)  exception  will  be  raised  if  any 
        operation is attempted with the cursor.
        '''
        ...
    

    #-------------------------------------------------------------------------
    @abstract
    def execute(self, operation: str , *parameters) -> Optional:
        '''Prepares and executes a database operation (query or command).
    
        From PEP 249:
        Parameters may be provided as sequence or mapping and  will 
        be bound to variables in the operation. Variables are spec-
        ified in a database-specific notation (see the module's 
        paramstyle attribute for details). [5]
    
        A reference to  the  operation  will  be  retained  by  the 
        cursor.  If  the  same operation object is passed in again, 
        then the cursor can optimize its  behavior.  This  is  most 
        effective  for algorithms where the same operation is used, 
        but different parameters are bound to it (many times).
    
        For maximum efficiency when reusing  an  operation,  it  is 
        best  to  use  the  .setinputsizes()  method to specify the 
        parameter types and sizes ahead of time.  It is legal for a 
        parameter  to  not  match  the  predefined information; the 
        implementation should compensate,  possibly with a loss  of 
        efficiency.
    
        The parameters may also be specified as list of  tuples  to 
        e.g.  insert multiple rows in a single operation,  but this 
        kind of usage is deprecated: .executemany() should be  used 
        instead.
    
        Return values are not defined.
        
        Note [5]:
        The module will use the __getitem__ method of the 
        parameters object to map  either  positions  (integers)  or 
        names  (strings)  to parameter values. This allows for both 
        sequences and mappings to be used as input.
        The term bound refers to the process of  binding  an  input 
        value  to  a database execution buffer. In practical terms, 
        this means that the input value is directly used as a value 
        in  the  operation.  The  client  should not be required to 
        "escape" the value so that it  can  be  used  —  the  value 
        should be equal to the actual database value.
        
        Args:
            operation: str
                The operation to execute.
            parameters:
                the arguments to pass to the operation.
        '''
        ...
    

    #-------------------------------------------------------------------------
    @abstract
    def executemany(self, operation: str, seq_of_parameters: tuple ) -> Optional:
        '''Prepares a database operation (query or command) and then execute it against all parameter sequences or mappings found in the sequence seq_of_parameters.
    
        From PEP 249:
        Modules are free to implement this  method  using  multiple 
        calls to the .execute() method or by using array operations 
        to have the database process the sequence as a whole in one 
        call.
    
        Use of this method for an operation which produces  one  or 
        more  result  sets  constitutes undefined behavior, and the 
        implementation is permitted (but not required) to raise  an 
        exception  when  it  detects  that  a  result  set has been 
        created by an invocation of the operation.
    
        The same comments as for .execute() also apply  accordingly 
        to this method.
    
        Return values are not defined.
        
        Args:
            operation: str
                The operation to execute.
            parameters: tuple
                A sequence of arguments to pass to the operation.
        '''
        ...


    #-------------------------------------------------------------------------
    @abstract
    def fetchall(self) -> List[Tuple]:
        '''Fetch all (remaining) rows of a query result.
        
        From PEP 249:
        Returns rows as a sequence of sequences  (e.g.  a  list  of 
        tuples).  Note  that  the  cursor's arraysize attribute can 
        affect the performance of this operation.
    
        An Error (or subclass) exception should be  raised  if  the 
        previous call to .execute*() did not produce any result set 
        or no call was issued yet.
        '''
        ...

    #-------------------------------------------------------------------------
    @abstract
    def fetchmany(self, size: Optional[int] = None) -> List[Tuple]:
        '''Fetch the next set of rows of a query result.
        
        From PEP 249:
        Returns a sequence of sequences (e.g. a list of tuples). An 
        empty sequence is returned when no more rows are available.
    
        The number of rows to fetch per call is  specified  by  the 
        parameter.  If  it  is  not  given,  the cursor's arraysize 
        determines the number of rows to  be  fetched.  The  method 
        should  try  to fetch as many rows as indicated by the size 
        parameter.  If this is not possible due  to  the  specified 
        number  of  rows  not  being  available,  fewer rows may be 
        returned.
    
        An Error (or subclass) exception is raised if the  previous 
        call  to '.execute*()' did not produce any result set or no 
        call was issued yet.
    
        Note there are  performance  considerations  involved  with 
        the size parameter.  For optimal performance, it is usually 
        best to use the .arraysize attribute. If the size parameter 
        is  used,  then  it is best for it to retain the same value 
        from one .fetchmany() call to the next.
        '''
        ...


    #-------------------------------------------------------------------------
    @abstract
    def fetchone(self) -> Tuple:
        '''Fetch the next row of a query result set.
        
        From PEP 249:
        Returns a single sequence,  or None when no  more  data  is 
        available.
        Note that the interface may implement  row  fetching  using 
        arrays and other optimizations. It is not guaranteed that a 
        call to this method will only move  the  associated  cursor 
        forward by one row.
        
        An Error (or subclass) exception is raised if the  previous 
        call  to '.execute*()' did not produce any result set or no 
        call was issued yet.
        '''
        ...
    

    #-------------------------------------------------------------------------
    @abstract
    def nextset(self) -> Optional[bool]:
        '''Makes the cursor skip to the next available set.
    
        From PEP 249:
        This method is optional since not  all  databases  support 
        multiple result sets.
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

    
        This method will make the cursor skip to the next available 
        set, discarding any remaining rows from the current set.
    
        If there  are  no  more  sets,  the  method  returns  None. 
        Otherwise,  it returns a true value and subsequent calls to 
        the .fetch*() methods will return rows from the next result 
        set.
    
        An Error (or subclass) exception is raised if the  previous 
        call  to '.execute*()' did not produce any result set or no 
        all was issued yet.
        '''
        ...
        

    #-------------------------------------------------------------------------
    @abstract
    def setinputsizes(self, sizes: Tuple[Union[int,DBType]]) -> None:
        '''This can be used before a call to .execute*() to predefine memory areas for the operation's parameters.
    
        From PEP 249:
        Sizes is specified as a sequence — one item for each  input 
        parameter.  The  item should be a Type Object that corresp-
        onds to the input that will be used,  or it  should  be  an 
        integer  specifying  the  maximum length of a string param-
        eter.  If the item is None,  then no predefined memory area 
        will  be  reserved for that column (this is useful to avoid 
        predefined areas for large inputs).
    
        This method would be used before the .execute*() method  is 
        invoked.
    
        Implementations are free to have this method do nothing and 
        users are free to not use it.
        '''
        ...


    #-------------------------------------------------------------------------
    @abstract
    def setoutputsize(self, size: int, column_index: Optional[int] = None) -> None:
        '''Sets a column buffer size for fetches of large columns (e.g. LONGs, BLOBs, etc.).
        
        From PEP 249:
        The column  is  specified  as  an  index  into  the  result 
        sequence.  Not  specifying  the column will set the default 
        size for all large columns in the cursor.
    
        This method would be used before the .execute*() method  is 
        invoked.
    
        Implementations are free to have this method do nothing and 
        users are free to not use it.
        '''
        ...


    #-------------------------------------------------------------------------
    def _reset_raw_descr(self) -> None:
        '''Resets the fetched last row description.
        
        This is not part of PEP 249. It is provided as a convenience
        for the reset of property '.description'.
        '''
        self.row_name = None
        self.row_type = None
        self.row_display_size = None
        self.row_internal_size = None
        self.row_precision = None
        self.row_scale = None
        self.row_null_ok = None


    #-------------------------------------------------------------------------
    # Class data
    NO_ROW_COUNT = -1  # Future versions of the DB API specification (i.e. PEP 249) could redefine None instead of -1.
    
#=====   end of   Libs.ObjectSqlLib.ObjectSqlInterface.cursor   =====#
