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

from .decorators     import abstract
from .repeated_timer import RepeatedTimer


#=============================================================================
class WatchDog:
    """The class of watchdogs.
    
    ===--------------------------------------------------===
    CAUTION: 
    When running this code over a non  RTOS  (for  Real-Time 
    Operating System),  there  is  NO  WAY  to  ensure  that 
    periods of time will  be  correctly  respected.  It  MAY 
    and  it  WILL be that counts of milliseconds will not be
    respected by the underlying  operating  system.  Theref-
    ore,  you  SHOULD  NOT  USE THIS  CODE  FOR APPLICATIONS 
    DEALING  WITH  PEOPLE  SAFETY  AND FOR ANY OTHER KIND OF 
    APPLICATIONS FOR WHICH REAL TIME OPERATING IS  MANDATORY 
    IF THIS CODE IS NOT RUN OVER A TRUE RTOS.
    Notice:  MS-Windows is NOT an  RTOS.  Most  versions  of
    Linux  are not also,  which includes MacOS versions too.
    ===--------------------------------------------------===
    
    A watchdog is a specific timer which is awaken  after  a 
    period of time  and which runs its own code each time it 
    is awaken.  It may be reset at any  time,  avoiding  the 
    running  of  its own code by restoring a new full period 
    of waiting time. Most of the time, watchdogs are used to 
    implement and run a recovery function when some blocking 
    error occurred.
    
    Watchdogs must be explicitly  started  with  a  call  to
    their  method '.start()'.  They cannot be started twice. 
    Notice: Watchdogs are threading.Threads.
    
    Watchdogs may be definitively stopped by  calling  their 
    method '.stop()'.
    
    Inheriting classes must implement  method  '.process()'.
    This method contains the whole stuff that is to be proc-
    essed every time the watchdog is "awaken". This method
    is declared in internal class '._RepeatedTimer'.
    
    Watchdogs may be used as repeated  timers,  as  long  as 
    their method '.reset()' is never called.
    """
    
    #-------------------------------------------------------------------------
    def __init__(self, period_s: int,
                       name    : Optional[str] = None) -> None:
        '''Constructor.
        
        Args:
            period_s: int
                The interval of time,  expressed as a fract-
                ional  value of seconds,  to wait before the
                watchdog will be "awaken".
            name: str
                The name of this watchdog.  May be None,  in
                which  case  the  underlying  OS will give a
                default, unique one to it. Defaults to None.
        '''
        self._period_s = period_s
        self._name     = name
        
        self.repeat_timer = self._RepeatedTimer( period_s, name )

    #-------------------------------------------------------------------------
    def reset(self) -> None:
        '''Resets the waiting time before being awaken.
        '''
        try:
            self.repeat_timer.stop()
            self.repeat_timer = self._RepeatedTimer( self._period_s, self._name )
            self.start()
        except:
            pass
        
    #-------------------------------------------------------------------------
    def set_period(self, period_s: int) -> None:
        '''Modifies/sets the period of time before awakening this watchdog.
        
        Args:
            period_s: float
                The interval of time, expressed as a fract-
                ional value of seconds, to wait before the
                timer will repeat.
        '''
        self.repeat_timer.set_period( period_s )

    #-------------------------------------------------------------------------
    def start(self) -> None:
        '''Starts this watchdog.
        
        Should be called only once.
        
        Raises:
            RunTimeError: this method has been called more than once.
        '''
        try:
            self.repeat_timer.start()
        except:
            raise
        
    #-------------------------------------------------------------------------
    def stop(self) -> None:
        '''Definitively stops this watchdog.
        '''
        self.repeat_timer.stop()
        
    #-------------------------------------------------------------------------
    class _RepeatedTimer( RepeatedTimer ):
        '''The internal repeated timer.
        '''
        #-------------------------------------------------------------------------
        @abstract
        def process(self) -> None:
            '''The instructions to be run when watchdog is awaken.
            
            Raises:
                NotImplementedError:  This method has  not  been
                    implemented in inheriting class.
            '''
            ...

#=====   end of   Utils.watchdog   =====#
