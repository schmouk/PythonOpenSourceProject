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
from typing  import Optional
from time    import sleep

from Utils.repeated_timer import internal_decorator, RepeatedTimer


#=============================================================================

#-------------------------------------------------------------------------
class MyRepeatedTimer( RepeatedTimer ):
    '''The testing class.
    '''
    
    #-------------------------------------------------------------------------
    def __init__(self, period_ms  : int,
                       name       : Optional[str] = None,
                       start_count: Optional[int] = 0   ,
                       increment  : Optional[int] = 1    ) -> None:
        '''Constructor.
        
        Args:
            period_ms: int
                The interval of time,  expressed as  an  int
                value  o f milliseconds,  to wait before the
                watchdog will be "awaken".
            name: str
                The name of this watchdog.  May be None,  in
                which  case  the  underlying  OS will give a
                default, unique one to it. Defaults to None.
            start_count: int
                The starting value for counting.
            increment: int
                The step to increment counting.
        '''
        super().__init__( period_ms, name )
        self._count = start_count
        self._incr = increment

    #-------------------------------------------------------------------------
    def process(self) -> None:
        '''The instructions to be run when watchdog is awaken.
        '''
        self._count += self._incr
        print( f"{self._count:4d}", end='', flush=True )


#-------------------------------------------------------------------------
def test():
    '''The test core.
    '''
    repeated_timer = MyRepeatedTimer( 1.200 )
    repeated_timer.start()
    sleep( 10.0 )
    repeated_timer.set_period( 0.480 )
    sleep( 3.0 )
    repeated_timer.stop()
    print( '\n--' )
    
    repeated_timer = MyRepeatedTimer( 1.200, start_count=13, increment=3 )
    repeated_timer.start()
    sleep( 10.0 )
    repeated_timer.set_period( 0.480 )
    sleep( 3.0 )
    repeated_timer.stop()
    print( '\n' )


#=============================================================================
if __name__ == '__main__':
    """Script description.
    """
    #-------------------------------------------------------------------------
    test()
    print( '\n-- done!')


#=====   end of   Utils._tests.test_repeated_timer   =====#
