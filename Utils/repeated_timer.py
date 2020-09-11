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
from threading   import Event, Thread
from typing      import Optional

from .decorators import abstract


#=============================================================================
class RepeatedTimer( Thread ):
    """The class of repeated timers.
    
    ===-------------------------------------------------===
    CAUTION: 
    When running this code over a non RTOS  (for  Real-Time 
    Operating System),  there  is  NO  WAY  to  ensure that 
    periods of time will be  correctly  respected.  It  MAY 
    and  it WILL be that counts of milliseconds will not be
    respected by the underlying operating  system.  Theref-
    ore,  you  SHOULD NOT USE THIS  CODE  FOR  APPLICATIONS 
    DEALING  WITH  PEOPLE  SAFETY AND FOR ANY OTHER KIND OF 
    APPLICATIONS FOR WHICH REAL TIME OPERATING IS MANDATORY 
    IF THIS CODE IS NOT RUN OVER A TRUE RTOS.
    Notice: MS-Windows is NOT an  RTOS.  Most  versions  of
    Linux are not also,  which includes MacOS versions too.
    ===-------------------------------------------------===
    
    A repeated timer is a specific timer which repeats  its 
    processing  function  after  a fixed period of time has 
    elapsed.
    
    Repeated timers must be explicitly started with a  call 
    to their  method  '.start()'.  They  cannot  be started 
    twice, since they inherit from threading.Threads.
    
    Repeated timers can be definitively stopped by  calling
    their method '.stop()'.
    
    Inheriting classes must implement method  '.process()'.
    This  method  contains  the  whole  stuff that is to be 
    processed every time the watchdog is "awaken".
    
    Users are encouraged to add attributes to  this  class.
    These  will then be accessible into method '.process()'
    when they might be needed for this processing.
    """
    
    #-------------------------------------------------------------------------
    def __init__(self, period_s: float               ,
                       name    : Optional[str] = None,
                       *args, **kwargs                ) -> None:
        '''Constructor.
        
        Args:
            period_s: float
                The interval of time,  expressed as a fract-
                ional  value of seconds,  to wait before the
                timer will repeat.
            name: str
                The name of this  timer.  May  be  None,  in
                which  case  the  underlying  OS will give a
                default, unique one to it. Defaults to None.
            *args, **kwargs:
                Arguments to be  passed  to  the  processing
                function.
        '''
        self.stop_event= Event()
        
        self.set_period( period_s )
        self.args = args
        self.kwargs = kwargs
        
        super().__init__( name=name )

    #-------------------------------------------------------------------------
    @abstract
    def process(self) -> None:
        '''The instructions to be run when timer is repeated.
        
        'self.args'  and  'self.kwargs'  are available in 
        this method.
        
        Raises:
            NotImplementedError: This method has not been
                implemented in inheriting class.
        '''
        ...

    #-------------------------------------------------------------------------
    def run(self) -> None:
        '''This method is automatically called by method '.start()'.
        
        Notice: method '.start()' is inherited from class
            'threading.Thread'.
        '''
        self.stop_event.clear()  ## just to be sure that associate internal flag is set to False
        while not self.stop_event.wait( self.period_s ):
            self.process()

    #-------------------------------------------------------------------------
    def set_period(self, period_s: int) -> None:
        '''Modifies/sets the period of time used for repeating this timer.
        
        Args:
            period_s: float
                The interval of time, expressed as a fract-
                ional value of seconds, to wait before the
                timer will repeat.
        '''
        assert period_s > 0.0
        self.period_s = period_s

    #-------------------------------------------------------------------------
    def stop(self) -> None:
        '''Definitively stops this repeated timer.
        '''
        self.stop_event.set()

#=====   end of   Utils.repeated_timer   =====#
