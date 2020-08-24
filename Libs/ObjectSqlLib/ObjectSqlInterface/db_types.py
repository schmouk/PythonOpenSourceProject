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
import datetime

from Utils.decorators import abstract


#=============================================================================

NULL = None  # PEP 249: SQL NULL values are represented by the Python None singleton on input and output.


class TYPE:
    '''The base class for all other types declared below.
    '''
    pass


class BINARY( TYPE ):
    '''This type object is used to describe (long) binary columns in a database (e.g. LONG, RAW, BLOBs).
    '''
    pass


class DATETIME ( TYPE ):
    '''This type object is used to describe date/time columns in a database.
    '''
    pass


class NUMBER( TYPE ):
    '''This type object is used to describe numeric columns in a database.
    '''
    pass


class ROWID( TYPE ):
    '''This type object is used to describe the "Row ID" column in a database.
    '''
    pass


class STRING( TYPE ):
    '''This type object is used to describe columns in a database that are string-based (e.g. CHAR)'''
    pass


#------------------------------------------------------------------------------
def Binary(string) -> bytes:
    '''Constructs an object capable of holding a binary (long) string value.
    '''
    return string.encode()  ## notice: defautls encoding is 'utf-8'


def Date(year: int, month: int, day: int) -> datetime.date:
    '''Constructs an object holding a date value.
    '''
    return datetime.date(year, month, day)
    

def DateFromTicks(self, ticks: float) -> datetime.date:
    '''Constructs an object holding a date value from the given ticks value.
    
    Args:
        ticks: float
            The number of seconds since the epoch - i.e. 1970-01-01.
    '''
    return datetime.date.fromtimestamp( ticks )


def Time(hour: int, minute: int, second: int) -> datetime.time:
    '''Constructs an object holding a time value.
    '''
    return datetime.time( hour, minute, second )


def TimeFromTicks(self, ticks: float) -> datetime.time:
    '''Constructs an object holding a time value from the given ticks value.
    
    Args:
        ticks: float
            The number of seconds since the epoch - i.e. 1970-01-01.
    '''
    return datetime.time.fromtimestamp( ticks )


def Timestamp(year: int, month: int, day,
              hour: int, minute: int, second: int) -> datetime.datetime:
    '''Constructs an object holding a time stamp value.
    '''
    return  datetime.datetime( year, month, day, hour, minute, second )


def TimestampFromTicks(self, ticks: float) -> datetime.datetime:
    '''Constructs an object holding a time stamp value from the given ticks value.
    
    Args:
        ticks: float
            The number of seconds since the epoch - i.e. 1970-01-01.
    '''
    return datetime.datetime.fromtimestamp( ticks )


#=====   end of   Libs.ObjectSqlLib.ObjectSqlInterface.db_types   =====#
